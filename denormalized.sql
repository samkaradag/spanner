CREATE TABLE DenormalizedSubscriber (
    UEid STRING(256) NOT NULL,
    AuthProvisioningProfileId STRING(256) NOT NULL,
    PlmnProfileId STRING(256) NOT NULL,
    SubscriptionProfileId STRING(256) NOT NULL,
    PlmnId STRING(256),
    OtherPlmnData STRING(MAX),
) PRIMARY KEY (UEid);