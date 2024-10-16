# Cloud Spanner Benchmark: Single Read Performance

This script benchmarks the single read performance of a Cloud Spanner database. It measures the latency of individual read operations against a `Subscriber` table, retrieving rows based on a randomly selected `UEid`.

## Prerequisites

* **Google Cloud Project:** A Google Cloud project with the Cloud Spanner API enabled.
* **Cloud Spanner Instance and Database:** A Cloud Spanner instance and database must exist with a table named `Subscriber` (and optionally `TestData` for write benchmarks, which are currently commented out). The `Subscriber` table should have a column named `UEid` used for querying. The `UEid` column should be indexed for optimal read performance.
* **Google Cloud SDK:** The Google Cloud SDK must be installed and configured with authentication.
* **Python:** Python 3.7 or higher with the `google-cloud-spanner` library installed: `pip install google-cloud-spanner`


## Usage

1. **Modify parameters:** Update `instance_id` and `database_id` variables at the top of the script to match your Cloud Spanner instance and database IDs. Adjust `num_rows` to control the number of read operations performed.

2. **Run the script:** Execute the script using the following command:

```bash
python spanner_benchmark.py <your_instance_id> <your_database_id>
```

Replace `<your_instance_id>` and `<your_database_id>` with your actual instance and database IDs.

3. **Review results:** The script outputs the percentiles (p50, p90, p95, p99) of the read latencies.


## Script Explanation

The script performs the following actions:

1. **Initializes the Spanner client:** Connects to your Cloud Spanner instance and database.
2. **Defines benchmark parameters:** Sets the number of rows to process, batch size (currently unused because only single reads are performed), and other relevant parameters.
3. **`perform_single_read()` function:** Executes a single read operation using a random `UEid`. The query currently selects all columns from the `Subscriber` table for a given `UEid`. Consider optimizing the query by only selecting the necessary columns for your use case. Note: The comment shows how to join with another table, `PlmnProfile`, you'll need to uncomment and adjust if needed.
4. **`perform_single_write()` function (commented out):** A function to perform a single write operation (currently commented out). This could be uncommented to perform write benchmarks in conjunction with reads.
5. **`calculate_percentiles()` function:** Calculates the p50, p90, p95, and p99 percentiles of a latency list.
6. **Benchmarking loop:** Iterates through `num_rows`, performing a single read operation in each iteration and recording the latency.
7. **Output:** Prints the calculated percentiles for read latencies.


## To add Write and Mixed Workload Benchmarks:

Uncomment the relevant sections of the code to include write operations and a mixed workload benchmark. Remember to create the `TestData` table in your Spanner database if you uncomment the write operations. Adjust the `read_batch_size` variable to control the ratio of reads to writes in the mixed workload.


## Important Considerations

* **Database Schema:** Ensure your `Subscriber` table is properly indexed (especially the `UEid` column) for optimal performance.
* **Network Latency:** Network latency can significantly impact benchmark results. Run the benchmark from a location geographically close to your Spanner instance.
* **Resource Contention:** If running multiple benchmarks concurrently, or under high database load, results may not be representative of peak performance.
* **Data Size:** The size of the data returned by the read query will affect performance.


This benchmark provides a basic measurement of single read performance. For more comprehensive testing, consider exploring more sophisticated benchmarking tools and methodologies.