CREATE TABLE Subscriber (
    UEid STRING(256) NOT NULL,
    AuthProvisioningProfileId STRING(256) NOT NULL,
    PlmnProfileId STRING(256) NOT NULL,
    SubscriptionProfileId STRING(256) NOT NULL,
)     PRIMARY KEY (UEid);



INSERT INTO Subscriber (UEid, AuthProvisioningProfileId, PlmnProfileId, SubscriptionProfileId) VALUES
('UE-samet1', 'AuthProvisioningProfileId 1', 'plmn-profile-1', 'Subscription Profile 1');

CREATE TABLE PlmnProfile (
    PlmnProfileId STRING(256) NOT NULL,
    PlmnId STRING(256), 
    OtherPlmnData STRING(MAX),
) PRIMARY KEY (PlmnProfileId);


CREATE TABLE SubscriptionProfile (
    SubscriptionProfileId STRING(256) NOT NULL,
    Name STRING(256),
    Description STRING(256),
) PRIMARY KEY (SubscriptionProfileId);



INSERT INTO PlmnProfile (PlmnProfileId, PlmnId, OtherPlmnData) VALUES
('plmn-profile-1', '310260', '{"region": "North America", "operator": "T-Mobile"}'),
('plmn-profile-2', '310410', '{"region": "North America", "operator": "AT&T"}'),
('plmn-profile-3', '310120', '{"region": "North America", "operator": "Sprint"}'),
('plmn-profile-4', '27202', '{"region": "Europe", "operator": "Vodafone IE"}'),
('plmn-profile-5', '20810', '{"region": "Europe", "operator": "Orange F"}'),
('plmn-profile-6', '46000', '{"region": "Asia", "operator": "China Mobile"}'),
('plmn-profile-7', '46001', '{"region": "Asia", "operator": "China Unicom"}'),
('plmn-profile-8', '46003', '{"region": "Asia", "operator": "China Telecom"}'),
('plmn-profile-9', '44010', '{"region": "Asia", "operator": "NTT DoCoMo"}'),
('plmn-profile-10', '45201', '{"region": "Asia", "operator": "Viettel"}');


INSERT INTO SubscriptionProfile (SubscriptionProfileId, Name, Description) VALUES
('a179682f-1223-4852-9611-281425b335b2', 'Subscription Profile 1', 'Description for Subscription Profile 1');
INSERT INTO SubscriptionProfile (SubscriptionProfileId, Name, Description) VALUES
('66d10724-95f2-4e7d-b795-96c1039354a7', 'Subscription Profile 2', 'Description for Subscription Profile 2');
INSERT INTO SubscriptionProfile (SubscriptionProfileId, Name, Description) VALUES
('2227e65b-2265-4a63-844e-3e987d291003', 'Subscription Profile 3', 'Description for Subscription Profile 3');
INSERT INTO SubscriptionProfile (SubscriptionProfileId, Name, Description) VALUES
('7391c5a3-9c67-4836-a819-2a3f475b8242', 'Subscription Profile 4', 'Description for Subscription Profile 4');
INSERT INTO SubscriptionProfile (SubscriptionProfileId, Name, Description) VALUES
('59653c53-9026-4243-8a79-2e7f2291352f', 'Subscription Profile 5', 'Description for Subscription Profile 5');
INSERT INTO SubscriptionProfile (SubscriptionProfileId, Name, Description) VALUES
('0030096f-054d-41c7-a811-4a0924500330', 'Subscription Profile 6', 'Description for Subscription Profile 6');
INSERT INTO SubscriptionProfile (SubscriptionProfileId, Name, Description) VALUES
('f2306a5c-9c69-4c50-9a31-4c994033707b', 'Subscription Profile 7', 'Description for Subscription Profile 7');
INSERT INTO SubscriptionProfile (SubscriptionProfileId, Name, Description) VALUES
('5959865c-6169-4a73-b297-998121280573', 'Subscription Profile 8', 'Description for Subscription Profile 8');
INSERT INTO SubscriptionProfile (SubscriptionProfileId, Name, Description) VALUES
('4864199c-8389-4b94-8265-066612142656', 'Subscription Profile 9', 'Description for Subscription Profile 9');
INSERT INTO SubscriptionProfile (SubscriptionProfileId, Name, Description) VALUES
('974287a1-9611-4899-8316-696249941321', 'Subscription Profile 10', 'Description for Subscription Profile 10');
INSERT INTO SubscriptionProfile (SubscriptionProfileId, Name, Description) VALUES
('22116594-3107-4182-9905-288556524734', 'Subscription Profile 11', 'Description for Subscription Profile 11');
INSERT INTO SubscriptionProfile (SubscriptionProfileId, Name, Description) VALUES
('3a050545-3789-4c40-a356-100109325363', 'Subscription Profile 12', 'Description for Subscription Profile 12');
INSERT INTO SubscriptionProfile (SubscriptionProfileId, Name, Description) VALUES
('81020889-3145-4695-9760-814920920112', 'Subscription Profile 13', 'Description for Subscription Profile 13');
INSERT INTO SubscriptionProfile (SubscriptionProfileId, Name, Description) VALUES
('33756134-7618-4501-a986-987855436931', 'Subscription Profile 14', 'Description for Subscription Profile 14');
INSERT INTO SubscriptionProfile (SubscriptionProfileId, Name, Description) VALUES
('30160549-7404-4807-a351-212921113331', 'Subscription Profile 15', 'Description for Subscription Profile 15');
INSERT INTO SubscriptionProfile (SubscriptionProfileId, Name, Description) VALUES
('90956112-0553-4531-8179-896359452954', 'Subscription Profile 16', 'Description for Subscription Profile 16');
INSERT INTO SubscriptionProfile (SubscriptionProfileId, Name, Description) VALUES
('87222823-1070-4281-8015-160893858077', 'Subscription Profile 17', 'Description for Subscription Profile 17');
INSERT INTO SubscriptionProfile (SubscriptionProfileId, Name, Description) VALUES
('72574270-6976-4906-b781-954767978747', 'Subscription Profile 18', 'Description for Subscription Profile 18');
INSERT INTO SubscriptionProfile (SubscriptionProfileId, Name, Description) VALUES
('21317264-4694-4192-a332-840806368857', 'Subscription Profile 19', 'Description for Subscription Profile 19');
INSERT INTO SubscriptionProfile (SubscriptionProfileId, Name, Description) VALUES
('72233193-7481-4726-8959-460148199531', 'Subscription Profile 20', 'Description for Subscription Profile 20');

--hash joins
--index join
--interleave subscriber in plmnprofile
-- session pool