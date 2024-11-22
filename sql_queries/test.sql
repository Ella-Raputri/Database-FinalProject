USE ClinicSystemDB;

select * from patient order by PatientId desc limit 10;
select * from User where UserId LIKE 'PAT%' order by UserID desc limit 10;

DELETE FROM `User` WHERE PatientId = 'PAT0000751';