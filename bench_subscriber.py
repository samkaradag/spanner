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
num_rows = 1000000
num_rows_in_table = 1000000
read_batch_size = 10
num_threads = 10  # Adjust the number of threads as needed


class MyCustomPool(AbstractSessionPool):
    def __init__(self, size, default_timeout=30): # Takes size like FixedSizePool
        super().__init__()  # Important to call super().__init__()
        self._size = size
        self._sessions = []
        self._default_timeout = default_timeout

    def bind(self, database):
        for _ in range(self._size):
            self._sessions.append(database.session())
            self._sessions[-1].create() # Pre-create the session

    def get(self, read_only=False):
        if read_only:
            raise NotImplementedError("Read-only sessions not implemented in this example.")  # You can add this later if needed
        return self._sessions.pop()  # Get a session from the pool

    def put(self, session, discard_if_full=True):
        if len(self._sessions) < self._size:
            self._sessions.append(session) # Return session to the pool



def perform_single_read(session):  # Corrected: session, not snapshot
    results = session.execute_sql(
        "SELECT * FROM Subscriber s JOIN PlmnProfile p ON s.PlmnProfileId = p.PlmnProfileId WHERE s.UEid = @UEid", 
        params={"UEid": str(random.randint(1, num_rows_in_table))},
        param_types={"UEid": spanner.param_types.STRING},
    )
    list(results) # Consume the iterator (important for the query to actually execute)



def run_benchmark(database, num_iterations, pool):
    read_latencies = []

    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        for _ in range(num_iterations):
            start_time = time.time()
            futures = []

            for _ in range(read_batch_size):
                session = pool.get()
                futures.append(executor.submit(perform_single_read, session))  # Pass the session

            for future in futures:  # Wait for all reads to complete
                future.result()
            
            for future in futures: # Iterate through futures and return sessions.
                session = future.result() # future.result() in this case will return the session passed into perform_single_read()
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
    
    pool = MyCustomPool(size=num_threads) # Initialize pool before binding to db

    database = instance.database(database_id, pool=pool) # Bind custom pool
    pool.bind(database) # Bind the pool to the database.


    read_latencies = run_benchmark(database, num_rows, pool)  # Pass database and pool
    print("Single Read Latencies:", calculate_percentiles(read_latencies))



if __name__ == "__main__":
    main(instance_id, database_id)