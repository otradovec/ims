INSERT INTO ims."user" (user_role,user_first_name) VALUES (1,'Joseph');

ALTER TABLE new_database.ims.incident ALTER COLUMN incident_created_at SET DEFAULT NOW()::timestamptz;
ALTER TABLE new_database.ims.incident ALTER COLUMN incident_updated_at SET DEFAULT NOW()::timestamptz;
ALTER TABLE new_database.ims.comment ALTER COLUMN comment_created_at SET DEFAULT NOW()::timestamptz;
ALTER TABLE new_database.ims.comment ALTER COLUMN comment_updated_at SET DEFAULT NOW()::timestamptz;


INSERT INTO ims.incident (incident_name,incident_description,incident_created_at,incident_updated_at,incident_priority,reporter_id,resolver_id,incident_status) 
VALUES ('Infected door camera','The front door camera of building C is infected with malicious code and is used for scanning the network.','2022-11-08T10:32:54+00:00','2022-11-08T10:32:54+00:00',
1,1,1,1);

INSERT INTO ims.incident (incident_name,incident_description,incident_created_at,incident_updated_at,incident_priority,reporter_id,resolver_id,incident_status) 
VALUES ('Infected manager laptop','The manager laptos is used for scanning the network.',NOW()::timestamptz,NOW()::timestamptz,
3,1,1,1);

INSERT INTO ims.incident (incident_name,incident_description,incident_priority,reporter_id,resolver_id,incident_status) 
VALUES ('Cryptocurrency Mining on a server','The ip address 192.168.70.2 of the log server is reported to be used for cryptocurrency mining.',
2,1,1,1);

INSERT INTO ims.event_incident (event_id,incident_id) VALUES (376255,6);

INSERT INTO ims.comment (comment_text,incident_id,author_id)
 VALUES ('cryprocurrency Web Mining detected by Flowmon',6,1);
 
INSERT INTO ims.attachment (attachment_path,comment_id) VALUES ('data.json',1);
