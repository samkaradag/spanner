from google.cloud import spanner
import uuid
import random
from concurrent.futures import ThreadPoolExecutor

# Your Spanner project, instance, and database IDs
project_id = "sametsplayground"
instance_id = "perf-multi"
database_id = "perftest"

# Number of Subscriber records to generate
num_subscribers = 1000000
num_plmn_profiles = 10
num_subscription_profiles = 20
batch_size = 1000  # Adjust batch size as needed

# Sample Plmn Profile Data (adjust as needed)
plmn_profiles = {
    f"plmn-profile-{i}": {
        "PlmnId": f"plmn-id-{i}",
        "OtherPlmnData": f"other-data-{i}"
    }
    for i in range(1, num_plmn_profiles + 1)
}

def insert_denormalized_subscriber_data(transaction, ueid, auth_profile_id, plmn_profile_id, subscription_profile_id):
    """Inserts a single denormalized Subscriber record within a transaction."""
    
    plmn_profile = plmn_profiles[plmn_profile_id]

    values = (
        ueid,
        auth_profile_id,
        plmn_profile_id,
        subscription_profile_id,
        plmn_profile["PlmnId"],
        plmn_profile["OtherPlmnData"]
    )
    transaction.insert(
        "DenormalizedSubscriber",
        columns=["UEid", "AuthProvisioningProfileId", "PlmnProfileId", "SubscriptionProfileId", "PlmnId", "OtherPlmnData"],
        values=[values]
    )


def generate_and_insert_batch(database, batch_num):
    """Generates and inserts a batch of denormalized Subscriber data."""

    def insert_data(transaction):  # Define a transaction callback
        for i in range(batch_num * batch_size + 1, (batch_num + 1) * batch_size + 1):
            ueid = f"UE-{i}"
            auth_profile_id = f"auth-profile-{i}"
            plmn_profile_id = f"plmn-profile-{random.randint(1, num_plmn_profiles)}"
            subscription_profile_id = f"{(i % num_subscription_profiles) + 1}"

            insert_denormalized_subscriber_data(transaction, ueid, auth_profile_id, plmn_profile_id, subscription_profile_id)

    database.run_in_transaction(insert_data)  # Pass the transaction callback
    print(f"Inserted batch {batch_num + 1}")



def main():
    spanner_client = spanner.Client(project=project_id)
    instance = spanner_client.instance(instance_id)
    database = instance.database(database_id)
    # Get the database object

    num_batches = num_subscribers // batch_size

    with ThreadPoolExecutor() as batch_executor:
        batch_futures = [batch_executor.submit(generate_and_insert_batch, database, batch_num) for batch_num in range(num_batches)]
        for future in batch_futures:
            future.result()  # Handle any exceptions


if __name__ == "__main__":
    main()
    print(f"Inserted {num_subscribers} denormalized Subscriber records into Spanner.")
