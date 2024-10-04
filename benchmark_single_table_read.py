import time
import random
import argparse
from google.cloud import spanner

# Initialize Spanner client
instance_id = "perf-multi"
database_id = "perftest"

def main(instance_id, database_id):
    spanner_client = spanner.Client()
    instance = spanner_client.instance(instance_id)
    database = instance.database(database_id)

    # Benchmark parameters
    num_rows = 2000  # Number of rows to process
    num_rows_in_table =1000000
    read_batch_size = 10  # Number of reads per write operation

    # Function to execute a single read operation
    def perform_single_read():
        with database.snapshot() as snapshot:
            results = snapshot.execute_sql(
                #  "SELECT * FROM Subscriber s JOIN PlmnProfile p ON s.PlmnProfileId = p.PlmnProfileId WHERE s.UEid = @UEid", 
                 "SELECT * FROM Subscriber s WHERE s.UEid = @UEid", 
                params={"UEid": str(random.randint(1, num_rows_in_table))},
                param_types={"UEid": spanner.param_types.STRING},
            )
            for row in results:
                pass  # Do something with the row if needed

    # Function to execute a single write operation
    def perform_single_write():
        with database.batch() as batch:
            batch.insert(
                table="TestData",
                columns=("Col1", "Col2", "Col3", "Col4", "Col5", "Col6"),
                values=[
                    (
                        "new_value1",
                        "new_value2",
                        "new_value3",
                        "new_value4",
                        "new_value5",
                        str(random.randint(num_rows + 1, num_rows + 1000)),
                    )
                ],
            )

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

    # Benchmarking logic
    read_latencies = []
    write_latencies = []
    mixed_latencies = []

    for i in range(num_rows):
        # Single read benchmark
        start_time = time.time()
        perform_single_read()
        end_time = time.time()
        read_latencies.append(end_time - start_time)

        # # Single write benchmark
        # start_time = time.time()
        # perform_single_write()
        # end_time = time.time()
        # write_latencies.append(end_time - start_time)

        # # Mixed workload benchmark (1 write for every 10 reads)
        # if i % read_batch_size == 0:
        #     start_time = time.time()
        #     perform_single_write()
        #     end_time = time.time()
        #     mixed_latencies.append(end_time - start_time)
    # Calculate and print percentiles
    
    # print("Single Write Latencies:", calculate_percentiles(write_latencies))
    # print("Mixed Workload Latencies:", calculate_percentiles(mixed_latencies))
    print("Single Read Latencies:", calculate_percentiles(read_latencies))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("instance_id", help="Your Cloud Spanner instance ID.")
    parser.add_argument("database_id", help="Your Cloud Spanner database ID.")

    args = parser.parse_args()
    main(args.instance_id, args.database_id)