DROP DATABASE IF EXISTS ClinicSystemDB;

CREATE DATABASE ClinicSystemDB;
USE ClinicSystemDB;

CREATE TABLE ClinicBranch(
    BranchNo		INT					NOT NULL,
    BranchName		VARCHAR(255)		NOT NULL,
    BranchLocation	VARCHAR(255)		NOT NULL,
    PRIMARY KEY (BranchNo)
);

CREATE TABLE `User`(
    UserId				VARCHAR(10)			NOT NULL,
    Email 				VARCHAR(255) 		NOT NULL,
    `Password` 			VARCHAR(100)		NOT NULL,
    FirstName			VARCHAR(100)		NOT NULL,
    LastName			VARCHAR(200)		NOT NULL,
    Gender				BIT					NOT NULL,
    PhoneNumber			VARCHAR(50)   		NOT NULL,
    RoleName			VARCHAR(50)			NOT NULL,
    City				VARCHAR(50)			NOT NULL,
    AddressDetail		TEXT		 		NOT NULL,
    IsDeleted           BIT                 DEFAULT 0,
    PRIMARY KEY (UserId)
);

CREATE TABLE Specialty(
    SpecialtyId				VARCHAR(10)			NOT NULL,
    SpecialtyName 			VARCHAR(255) 		NOT NULL,
    SpecialtyDescription	TEXT,
    PRIMARY KEY (SpecialtyId)
);

CREATE TABLE Doctor (
    DoctorId        VARCHAR(10)   	NOT NULL,
    SpecialtyId     VARCHAR(10)   	NOT NULL,   
    ProfilePicture  VARCHAR(500), 
    `Description`   TEXT,
    BranchNo        INT   			NOT NULL,  
    PRIMARY KEY (DoctorId),
    FOREIGN KEY (DoctorId) REFERENCES `User`(UserId) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (SpecialtyId) REFERENCES Specialty(SpecialtyId),
    FOREIGN KEY (BranchNo) REFERENCES ClinicBranch(BranchNo) 
);

CREATE TABLE DoctorSchedule (
	ScheduleId      VARCHAR(10)   	NOT NULL,
    DoctorId        VARCHAR(10)   	NOT NULL,
    DayOfWeek	    VARCHAR(20)   	NOT NULL,   
    StartHour		TIME 			NOT NULL,
    EndHour			TIME 			NOT NULL,   
    PRIMARY KEY (ScheduleId),
    FOREIGN KEY (DoctorId) REFERENCES Doctor(DoctorId) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE Patient (
    PatientId       VARCHAR(10)   	NOT NULL,
    DateOfBirth     DATE   			NOT NULL,   
    ProfilePicture  VARCHAR(500), 
    PRIMARY KEY (PatientId),
    FOREIGN KEY (PatientId) REFERENCES `User`(UserId) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE Disease (
    DiseaseId       VARCHAR(10)   	NOT NULL,
    DiseaseName     VARCHAR(200)	NOT NULL,   
    PRIMARY KEY (DiseaseId)
);

CREATE TABLE MedicalHistory (
    PatientId       VARCHAR(10)   		NOT NULL,
    DiseaseId     	VARCHAR(200)		NOT NULL,   
    `Status`		BIT					NOT NULL, 
    PRIMARY KEY (PatientId, DiseaseId),
    FOREIGN KEY (PatientId) REFERENCES Patient(PatientId) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (DiseaseId) REFERENCES Disease(DiseaseId)
);

CREATE TABLE `Admin` (
    AdminId       	VARCHAR(10)   	NOT NULL,
    BranchNo        INT   			NOT NULL, 
    PRIMARY KEY (AdminId),
    FOREIGN KEY (AdminId) REFERENCES `User`(UserId) ON DELETE CASCADE ON UPDATE CASCADE,
	FOREIGN KEY (BranchNo) REFERENCES ClinicBranch(BranchNo) 
);

CREATE TABLE Booking (
    BookingId       	VARCHAR(10)   	NOT NULL,
    PatientId        	VARCHAR(10)		NOT NULL, 
    DoctorId        	VARCHAR(10)		NOT NULL,
    AppointmentDate		DATE			NOT NULL,
    AppointmentHour		TIME			NOT NULL,
    AppointmentStatus	VARCHAR(20)		NOT NULL,
    CheckUpType			VARCHAR(200)	NOT NULL,
    ReasonOfVisit		TEXT			NOT NULL,    
    PRIMARY KEY (BookingId),
    FOREIGN KEY (PatientId) REFERENCES Patient(PatientId),
    FOREIGN KEY (DoctorId) REFERENCES Doctor(DoctorId) 
);

CREATE VIEW BranchBookings AS
SELECT 
    b.BookingId,
    b.PatientId,
    CONCAT(pu.FirstName, ' ', pu.LastName) AS PatientName,
    b.DoctorId,
    CONCAT(du.FirstName, ' ', du.LastName) AS DoctorName,
    b.AppointmentDate,
    b.AppointmentHour,
    b.AppointmentStatus,
    b.CheckUpType,
    b.ReasonOfVisit,
    d.BranchNo
FROM  
    Booking b
INNER JOIN 
    Doctor d ON b.DoctorId = d.DoctorId
INNER JOIN 
    `User` du ON d.DoctorId = du.UserId
INNER JOIN 
    `User` pu ON b.PatientId = pu.UserId;

-- ALTER TABLE `User` ADD COLUMN IsDeleted BIT DEFAULT 0;
-- start transaction;
-- ALTER TABLE MedicalHistory 
-- DROP FOREIGN KEY medicalhistory_ibfk_1;

-- ALTER TABLE MedicalHistory 
-- ADD CONSTRAINT medicalhistory_ibfk_1 
-- FOREIGN KEY (PatientId) 
-- REFERENCES Patient(PatientId) 
-- ON UPDATE CASCADE 
-- ON DELETE CASCADE;

-- commit;
-- rollback;


select coun