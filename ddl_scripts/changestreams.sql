CREATE CHANGE STREAM SubscribersChangeStream
FOR Subscriber
OPTIONS ( value_capture_type = 'OLD_AND_NEW_VALUES' );

SELECT ChangeRecord
FROM SubscribersChangeStream (
    start_timestamp,
    end_timestamp,
    partition_token,
    heartbeat_milliseconds,
    read_options
)

SELECT ChangeRecord
FROM READ_SubscribersChangeStream (
    start_timestamp => "2024-10-11T12:10:00.123456Z",
    heartbeat_milliseconds => 300000
) unest

"2022-09-27T12:30:00.123456Z"


INSERT INTO Subscriber (UEid, AuthProvisioningProfileId, PlmnProfileId, SubscriptionProfileId) VALUES
('UE-samet5', 'AuthProvisioningProfileId 1', 'plmn-profile-1', 'Subscription Profile 1');

update Subscriber set AuthProvisioningProfileId = 'AuthProvisioningProfileId 2' where UEid = 'UE-samet5';