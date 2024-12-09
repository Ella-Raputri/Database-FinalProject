USE ClinicSystemDB;

select * from user ;
select * from User where UserId LIKE 'PAT%' order by UserID desc limit 10;
select * from patient;
select * from admin;

select count(DoctorId) from Doctor where BranchNo = 1;
select * from Booking where DoctorId in 
	(select DoctorId from Doctor where BranchNo = 2) order by appointmentdate desc;

-- SET SQL_SAFE_UPDATES = 0;

-- UPDATE Booking
-- SET AppointmentStatus = 'Pending'
-- WHERE AppointmentDate > CURDATE();

-- UPDATE Booking
-- SET AppointmentStatus = 'Completed'
-- WHERE AppointmentDate < CURDATE();

-- SET SQL_SAFE_UPDATES = 1; -- Re-enable safe update mode

SELECT 
    DATE_FORMAT(AppointmentDate, '%Y-%m') AS BookingMonth, -- Formats the date as "YYYY-MM"
    COUNT(*) AS TotalBookings
FROM BranchBookings
WHERE BranchNo = 2
GROUP BY BookingMonth
ORDER BY BookingMonth;

SELECT DISTINCT
	b.DoctorId,
	b.DoctorName, 
	ds.StartHour, 
	ds.EndHour
FROM DoctorSchedule ds
INNER JOIN BranchBookings b ON ds.DoctorId = b.DoctorId
WHERE ds.DayOfWeek = 'Saturday' AND b.BranchNo = 1;

SELECT DoctorName, PatientName, DATE_FORMAT(AppointmentHour, '%H:%i') AS AppointmentTime
FROM BranchBookings 
WHERE BranchNo = 1 AND AppointmentDate = '2024/11/23';

SELECT 
    d.DoctorId,
    s.SpecialtyName AS Specialty,
    u.Email,
    CONCAT(u.FirstName, ' ', u.LastName) AS Name,
    CASE u.Gender 
        WHEN 0 THEN 'Male'
        ELSE 'Female'
    END AS Gender,
    u.PhoneNumber,
    u.City,
    u.AddressDetail AS Address,
    COUNT(b.BookingId) AS TotalBookings,
    SUM(
        CASE 
            WHEN MONTH(b.AppointmentDate) = MONTH(CURRENT_DATE) 
                 AND YEAR(b.AppointmentDate) = YEAR(CURRENT_DATE)
            THEN 1 
            ELSE 0 
        END
    ) AS ThisMonthsBookings
FROM 
    Doctor d
LEFT JOIN 
    Specialty s ON d.SpecialtyID = s.SpecialtyID
LEFT JOIN 
    `User` u ON d.DoctorId = u.UserId
LEFT JOIN 
    Booking b ON d.DoctorId = b.DoctorId
WHERE d.BranchNo = 1
GROUP BY 
    d.DoctorId, s.SpecialtyName, u.Email, u.FirstName, u.LastName,
    u.Gender, u.PhoneNumber, u.City, u.AddressDetail
ORDER BY 
    d.DoctorId;

SELECT 
    p.PatientId,
    p.DateOfBirth,
    u.Email,
    CONCAT(u.FirstName, ' ', u.LastName) AS Name,
    CASE u.Gender 
        WHEN 0 THEN 'Male'
        ELSE 'Female'
    END AS Gender,
    u.PhoneNumber,
    u.City,
    u.AddressDetail AS Address,
    COUNT(b.BookingId) AS TotalBookings
FROM 
    Patient p
LEFT JOIN 
    `User` u ON p.PatientId = u.UserId
LEFT JOIN 
    Booking b ON p.PatientId = b.PatientId
INNER JOIN 
    Doctor d ON b.DoctorId = d.DoctorId  -- Join Doctor table to get BranchNo
WHERE 
    d.IsDeleted = 0
    AND d.BranchNo = 1  -- Filter by BranchNo
GROUP BY 
    p.PatientId, u.Email, u.FirstName, u.LastName,
    u.Gender, u.PhoneNumber, u.City, u.AddressDetail
ORDER BY 
    p.PatientId;

USE ClinicSystemDB;
select * from medicalhistory where patientid = 'PAT0000001' ;
SELECT 
CONCAT(DiseaseName, ': ', 
CASE Status 
	WHEN 0 THEN 'Ongoing'
	ELSE 'Recovered'
END
) AS MedHistory,
PatientId
FROM MedicalHistory
WHERE PatientId = 'PAT0000001'
ORDER BY Status ASC;

select * from user order by userid desc;
select * from patient order by patientid desc;
select * from doctor ;
select * from admin;

select * from branchbookings where appointmentstatus = 'Cancelled' order by bookingid desc;
SELECT 
    BookingId, PatientName, DoctorName, AppointmentDate, AppointmentHour,
    AppointmentStatus, CheckUpType, ReasonOfVisit
FROM BranchBookings 
WHERE BranchNo = 1
ORDER BY AppointmentDate DESC, STR_TO_DATE(AppointmentHour, '%H:%i') DESC;


SELECT * FROM Specialty;
SELECT * FROM BranchBookings where DoctorId = 'DOC0000001';
SELECT * FROM DoctorSchedule where DoctorId = 'DOC0000001' order by scheduleid desc;
SELECT COUNT(DoctorId) FROM Doctor WHERE SpecialtyId = 'SP0000020';
        
select * from doctor order by doctorid desc;
select * from user where userid like "DOC%" order by userid desc;
select * from booking order by appointmentdate desc;

start transaction;
DELETE FROM Booking WHERE DoctorId = 'DOC0000001';
DELETE FROM Doctor WHERE DoctorId = 'DOC0000001';
commit;
rollback;

select * from user;

SELECT 
CONCAT(d.DiseaseName, ': ', 
		CASE m.Status 
			WHEN 0 THEN 'Ongoing'
			ELSE 'Recovered'
		END
	) AS MedHistory
FROM MedicalHistory m JOIN Disease d 
ON m.DiseaseId = d.DiseaseId
WHERE m.PatientId = 'PAT0000002'
ORDER BY m.Status ASC;

select * from user where rolename = "doctor";
update user set isdeleted = 1 where userid = 'DOC0000001';
select * from doctor;
-- Step 1: Create a temporary table to assign the new emails
-- Step 1: Create a temporary table with unique numbers for each doctor
-- CREATE TEMPORARY TABLE TempEmails AS
-- SELECT 
--     UserId, 
--     CONCAT('pat', ROW_NUMBER() OVER (ORDER BY UserId), '@example.com') AS NewEmail
-- FROM `User`
-- WHERE UserId LIKE '%PAT%';

-- -- Step 2: Update the User table using the temporary table
-- UPDATE `User` u
-- JOIN TempEmails t ON u.UserId = t.UserId
-- SET u.Email = t.NewEmail;

-- -- Step 3: Clean up the temporary table
-- DROP TEMPORARY TABLE TempEmails;




