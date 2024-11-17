USE ClinicSystemDB;

-- Define number of records
SET @total_branches = 5;
SET @users_per_branch = 205;
SET @total_specialties = 20;
SET @total_bookings = 1000;
SET @patients_per_branch = 150;
SET @doctors_per_branch = 50;
SET @admins_per_branch = 5;

DROP PROCEDURE IF EXISTS InsertDummyMedicalHistory;
DROP PROCEDURE IF EXISTS InsertDummyDoctorSchedules;
DROP PROCEDURE IF EXISTS InsertDummyBookings;
DROP PROCEDURE IF EXISTS InsertDummyUsers;
DROP PROCEDURE IF EXISTS InsertDummySpecialties;
DROP PROCEDURE IF EXISTS InsertDummyBranches;

-- Insert 5 branches
DELIMITER $$
CREATE PROCEDURE InsertDummyBranches()
BEGIN
    DECLARE i INT DEFAULT 1;
    WHILE i <= @total_branches DO
        INSERT INTO ClinicBranch (BranchNo, BranchName, BranchLocation)
        VALUES (i, CONCAT('Branch ', i), CONCAT('Location ', i));
        SET i = i + 1;
    END WHILE;
END$$
DELIMITER ;
CALL InsertDummyBranches();

select * from ClinicBranch;

-- Insert 20 specialties with SpecialtyId format SP{number}
DELIMITER $$
CREATE PROCEDURE InsertDummySpecialties()
BEGIN
    DECLARE i INT DEFAULT 1;
    WHILE i <= 20 DO
        INSERT INTO Specialty (SpecialtyId, SpecialtyName, SpecialtyDescription)
        VALUES (CONCAT('SP', LPAD(i, 7, '0')), CONCAT('Specialty ', i), CONCAT('Description of Specialty ', i));
        SET i = i + 1;
    END WHILE;
END$$
DELIMITER ;
CALL InsertDummySpecialties();

select * from specialty;

DROP PROCEDURE IF EXISTS InsertDummyUsers;
-- Insert 205 users per branch
DELIMITER $$
CREATE PROCEDURE InsertDummyUsers()
BEGIN
    DECLARE branch_id INT DEFAULT 1;
    DECLARE patient_id INT DEFAULT 1;
    DECLARE doctor_id INT DEFAULT 1;
    DECLARE admin_id INT DEFAULT 1;
    WHILE branch_id <= @total_branches DO
        -- Insert patients
        WHILE patient_id <= branch_id * @patients_per_branch DO
            INSERT INTO `User` (UserId, Email, `Password`, FirstName, LastName, PhoneNumber, RoleName, City, AddressDetail)
            VALUES (CONCAT('PAT', LPAD(patient_id, 7, '0')), CONCAT('user', patient_id, '@example.com'), 'password', 
                    CONCAT('FirstName', patient_id), CONCAT('LastName', patient_id), 
                    CONCAT('081234567', patient_id), 'Patient', CONCAT('City', branch_id), 
                    CONCAT('Branch ', branch_id, ' Address'));
                    
			INSERT INTO Patient (PatientId, DateOfBirth, ProfilePicture)
            VALUES (CONCAT('PAT', LPAD(patient_id, 7, '0')), 
                    DATE_ADD('1980-01-01', INTERVAL FLOOR(RAND() * 14610) DAY),  -- randomize dob
                    NULL);
            SET patient_id = patient_id + 1;
        END WHILE;

        -- Insert doctors
        WHILE doctor_id <= branch_id * @doctors_per_branch DO
            INSERT INTO `User` (UserId, Email, `Password`, FirstName, LastName, PhoneNumber, RoleName, City, AddressDetail)
            VALUES (CONCAT('DOC', LPAD(doctor_id, 7, '0')), CONCAT('user', doctor_id, '@example.com'), 'password', 
                    CONCAT('FirstName', doctor_id), CONCAT('LastName', doctor_id), 
                    CONCAT('081234567', doctor_id), 'Doctor', CONCAT('City', branch_id), 
                    CONCAT('Branch ', branch_id, ' Address'));
            INSERT INTO Doctor (DoctorId, SpecialtyID, ProfilePicture, `Description`, BranchNo)
            VALUES (CONCAT('DOC', LPAD(doctor_id, 7, '0')), 
                    CONCAT('SP', LPAD(FLOOR(1 + RAND() * 20), 7, '0')),  -- Ensure valid SpecialtyId
                    NULL, CONCAT('Doctor description ', doctor_id), branch_id);
            SET doctor_id = doctor_id + 1;
        END WHILE;

        -- Insert admins
        WHILE admin_id <= branch_id * @admins_per_branch DO
            INSERT INTO `User` (UserId, Email, `Password`, FirstName, LastName, PhoneNumber, RoleName, City, AddressDetail)
            VALUES (CONCAT('ADM', LPAD(admin_id, 7, '0')), CONCAT('user', admin_id, '@example.com'), 'password', 
                    CONCAT('FirstName', admin_id), CONCAT('LastName', admin_id), 
                    CONCAT('081234567', admin_id), 'Admin', CONCAT('City', branch_id), 
                    CONCAT('Branch ', branch_id, ' Address'));
            INSERT INTO `Admin` (AdminId, BranchNo)
            VALUES (CONCAT('ADM', LPAD(admin_id, 7, '0')), branch_id);
            SET admin_id = admin_id + 1;
        END WHILE;

        SET branch_id = branch_id + 1;
    END WHILE;
END$$
DELIMITER ;
CALL InsertDummyUsers();


select * from user;
select * from patient;
select * from doctor;
select * from admin;

-- Insert Medical History for each patient (1-5 records per patient)
DELIMITER $$
CREATE PROCEDURE InsertDummyMedicalHistory()
BEGIN
    DECLARE patient_id INT DEFAULT 1;
    DECLARE history_count INT;
    DECLARE disease_name VARCHAR(255);
    
    WHILE patient_id <= @total_branches * @patients_per_branch DO
        SET history_count = FLOOR(1 + RAND() * 5); -- 1 to 5 histories per patient
        WHILE history_count > 0 DO
            -- Generate a unique disease name
            SET disease_name = CONCAT('Disease ', FLOOR(1 + RAND() * 100));
            
            -- Check if the disease already exists for this patient, and regenerate if necessary
            WHILE EXISTS (SELECT 1 FROM MedicalHistory WHERE PatientId = CONCAT('PAT', LPAD(patient_id, 7, '0')) AND DiseaseName = disease_name) DO
                SET disease_name = CONCAT('Disease ', FLOOR(1 + RAND() * 100));
            END WHILE;
            
            -- Insert the medical history record
            INSERT INTO MedicalHistory (PatientId, DiseaseName, `Status`)
            VALUES (
                CONCAT('PAT', LPAD(patient_id, 7, '0')), -- Ensure PatientId format
                disease_name,
                RAND() < 0.5 -- Randomize status
            );
            
            SET history_count = history_count - 1;
        END WHILE;
        SET patient_id = patient_id + 1;
    END WHILE;
END$$
DELIMITER ;
CALL InsertDummyMedicalHistory();

select * from medicalhistory;

-- Insert Doctor Schedules (1-5 per doctor)
DELIMITER $$
CREATE PROCEDURE InsertDummyDoctorSchedules()
BEGIN
    DECLARE i INT DEFAULT 1;
    DECLARE schedule_count INT;
    DECLARE start_hour INT;
    DECLARE end_hour INT;
    DECLARE day_of_week VARCHAR(10);
    DECLARE schedule_id INT DEFAULT 1; -- Start schedule id from 1
    
    WHILE i <= @total_branches * @doctors_per_branch DO
        SET schedule_count = FLOOR(1 + RAND() * 5); -- 1 to 5 schedules per doctor
        
        WHILE schedule_count > 0 DO
            -- Generate random start hour between 9 and 21
            SET start_hour = FLOOR(9 + RAND() * 12); -- Random hour between 9 and 21
            -- Ensure end hour is later than start hour
            SET end_hour = start_hour + FLOOR(1 + RAND() * 4); -- Random end hour, between start and 21

            -- Random day of the week (Monday to Sunday)
            SET day_of_week = CASE 
                                WHEN RAND() < 0.14 THEN 'Monday'
                                WHEN RAND() < 0.28 THEN 'Tuesday'
                                WHEN RAND() < 0.42 THEN 'Wednesday'
                                WHEN RAND() < 0.57 THEN 'Thursday'
                                WHEN RAND() < 0.71 THEN 'Friday'
                                WHEN RAND() < 0.85 THEN 'Saturday'
                                ELSE 'Sunday'
                              END;

            -- Insert doctor schedule with unique schedule_id
            INSERT INTO DoctorSchedule (ScheduleId, DoctorId, DayOfWeek, StartHour, EndHour)
            VALUES (
                CONCAT('SCH', LPAD(schedule_id, 7, '0')),  -- ScheduleId format SCH0000001
                CONCAT('DOC', LPAD(i, 7, '0')),  -- DoctorId format DOC{num}
                day_of_week,  -- Randomized day of the week
                CONCAT(LPAD(start_hour, 2, '0'), ':00:00'),  -- Start hour in HH:00:00 format
                CONCAT(LPAD(end_hour, 2, '0'), ':00:00')  -- End hour in HH:00:00 format
            );

            -- Increment schedule_id for the next schedule
            SET schedule_id = schedule_id + 1;
            SET schedule_count = schedule_count - 1;
        END WHILE;
        
        SET i = i + 1;
    END WHILE;
END$$
DELIMITER ;
CALL InsertDummyDoctorSchedules();

-- truncate table doctorschedule; 
select * from doctorschedule;


-- Insert 1000 Bookings (Random Patient and Doctor Combination)
DELIMITER $$
CREATE PROCEDURE InsertDummyBookings()
BEGIN
    DECLARE i INT DEFAULT 1;
    WHILE i <= @total_bookings DO
        INSERT INTO Booking (BookingId, PatientId, DoctorId, AppointmentDate, AppointmentStatus, CheckUpType, ReasonOfVisit)
        VALUES (CONCAT('BOK', LPAD(i, 7, '0')), 
                CONCAT('PAT', LPAD(FLOOR(1 + RAND() * (@total_branches * @patients_per_branch)), 7, '0')), 
                CONCAT('DOC', LPAD(FLOOR(1 + RAND() * (@total_branches * @doctors_per_branch)), 7, '0')),
                DATE_ADD('2024-01-01', INTERVAL FLOOR(RAND() * 365) DAY),
                CASE WHEN RAND() < 0.5 THEN 'Completed' ELSE 'Pending' END,
                CONCAT('Type ', FLOOR(1 + RAND() * 5)), 
                CONCAT('Visit Reason ', i));
        SET i = i + 1;
    END WHILE;
END$$
DELIMITER ;
CALL InsertDummyBookings();

select * from booking;