import time
import random
import argparse
from google.cloud import spanner
from google.cloud.spanner import AbstractSessionPool
from concurrent.futures import ThreadPoolExecutor

# Initialize Spanner client (outside the benchmark loop for efficiency)
instance_id = "perf-multi"  # Replace with your instance ID
database_id = "perftest"  # Replace with your database ID

spanner_client = spanner.Client()
instance = spanner_client.instance(instance_id)
database = instance.database(database_id)

# Benchmark parameters
num_rows = 3000
num_rows_in_table = 1000000
read_batch_size = 1
num_threads = 10  # Adjust the number of threads as needed


class MyCustomPool(AbstractSessionPool):
    def __init__(self, size, default_timeout=30):
        super().__init__()
        self._size = size
        self._sessions = []
        self._default_timeout = default_timeout

    def bind(self, database):
        for _ in range(self._size):
            session = database.session()
            session.create()  # Create the session
            self._sessions.append(session)

    def get(self, read_only=False):
        if read_only:
            raise NotImplementedError("Read-only sessions not implemented in this example.")
        if not self._sessions:
            raise RuntimeError("No available sessions in the pool.")
        return self._sessions.pop(0)  # Get a session from the pool

    def put(self, session, discard_if_full=True):
        if len(self._sessions) < self._size:
            self._sessions.append(session)  # Return session to the pool
        else:
            session.delete()  # Delete the session if pool is full


def perform_single_read(session):
    try:
        results = session.execute_sql(
            "SELECT * FROM Subscriber s JOIN PlmnProfile p ON s.PlmnProfileId = p.PlmnProfileId WHERE s.UEid = @UEid", 
            params={"UEid": "UE-" + str(random.randint(1, num_rows_in_table))},
            param_types={"UEid": spanner.param_types.STRING},
        )
        list(results)  # Consume the iterator to execute the query
    finally:
        return session  # Ensure the session is returned after the query


def run_benchmark(database, num_iterations, pool):
    read_latencies = []

    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        for _ in range(num_iterations):
            start_time = time.time()
            futures = []

            for _ in range(read_batch_size):
                session = pool.get()
                futures.append(executor.submit(perform_single_read, session))

            for future in futures:
                session = future.result()
                pool.put(session)

            end_time = time.time()
            read_latencies.append(end_time - start_time)

    return read_latencies


# Function to calculate percentiles
def calculate_percentiles(latencies):
    latencies.sort()
    n = len(latencies)
    percentiles = {
        "p50": latencies[int(n * 0.5)],
        "p90": latencies[int(n * 0.9)],
        "p95": latencies[int(n * 0.95)],
        "p99": latencies[int(n * 0.99)],
    }
    return percentiles


def main(instance_id, database_id):
    spanner_client = spanner.Client()
    instance = spanner_client.instance(instance_id)
    
    pool = MyCustomPool(size=num_threads)

    database = instance.database(database_id, pool=pool)
    pool.bind(database)

    read_latencies = run_benchmark(database, num_rows, pool)
    print("Single Read Latencies:", calculate_percentiles(read_latencies))


if __name__ == "__main__":
    main(instance_id, database_id)
