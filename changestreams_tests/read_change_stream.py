from google.cloud import spanner
import datetime

def read_change_stream(instance_id, database_id, start_timestamp):
    # Initialize the Spanner client
    spanner_client = spanner.Client()

    # Get a reference to the instance and database
    instance = spanner_client.instance(instance_id)
    database = instance.database(database_id)

    # SQL query to read from the change stream
    query = f"""
    SELECT *
    FROM READ_SubscribersChangeStream(
        start_timestamp => '{start_timestamp}',
        heartbeat_milliseconds => 300000
    )
    """

    # Execute the query
    with database.snapshot() as snapshot:
        results = snapshot.execute_sql(query)

        for row in results:
            print("Change detected:", row)


if __name__ == "__main__":
    # Replace these with your Spanner instance and database IDs
    instance_id = "perf-multi"
    database_id = "perftest"

    # Specify the start timestamp for the change stream query
    start_timestamp = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(minutes=10)
    start_timestamp = start_timestamp.strftime('%Y-%m-%dT%H:%M:%S.%fZ')

    # Call the function to read from the change stream
    read_change_stream(instance_id, database_id, start_timestamp)
