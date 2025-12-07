show databases;
use rfpdb;
SHOW TABLES FROM rfpdb;
select * from rfps;
drop database rfpdb;
SET SQL_SAFE_UPDATES = 0;
truncate table rfps; 
SET SQL_SAFE_UPDATES = 1;

SET FOREIGN_KEY_CHECKS = 0;
truncate table proposals;   ----------------dont delete:
SET FOREIGN_KEY_CHECKS = 1;

SHOW BINARY LOGS;

select * from rfps;
select * from vendors;
select * from proposals;
select * from communication_logs;

show tables;