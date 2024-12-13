USE ClinicSystemDB;
-- SET SQL_SAFE_UPDATES = 0;

-- UPDATE Booking
-- SET AppointmentStatus = 'Pending'
-- WHERE AppointmentDate > CURDATE();

-- UPDATE Booking
-- SET AppointmentStatus = 'Completed'
-- WHERE AppointmentDate < CURDATE();

-- SET SQL_SAFE_UPDATES = 1; -- Re-enable safe update mode


-- SELECT DISTINCT
-- 	b.DoctorId,
-- 	b.DoctorName, 
-- 	ds.StartHour, 
-- 	ds.EndHour
-- FROM DoctorSchedule ds
-- INNER JOIN BranchBookings b ON ds.DoctorId = b.DoctorId
-- WHERE ds.DayOfWeek = 'Saturday' AND b.BranchNo = 1;

-- SELECT DoctorName, PatientName, DATE_FORMAT(AppointmentHour, '%H:%i') AS AppointmentTime
-- FROM BranchBookings 
-- WHERE BranchNo = 1 AND AppointmentDate = '2024/11/23';


-- SELECT 
--     p.PatientId,
--     p.DateOfBirth,
--     u.Email,
--     CONCAT(u.FirstName, ' ', u.LastName) AS Name,
--     CASE u.Gender 
--         WHEN 0 THEN 'Male'
--         ELSE 'Female'
--     END AS Gender,
--     u.PhoneNumber,
--     u.City,
--     u.AddressDetail AS Address,
--     COUNT(b.BookingId) AS TotalBookings
-- FROM 
--     Patient p
-- LEFT JOIN 
--     `User` u ON p.PatientId = u.UserId
-- LEFT JOIN 
--     Booking b ON p.PatientId = b.PatientId
-- INNER JOIN 
--     Doctor d ON b.DoctorId = d.DoctorId  -- Join Doctor table to get BranchNo
-- WHERE 
--     d.IsDeleted = 0
--     AND d.BranchNo = 1  -- Filter by BranchNo
-- GROUP BY 
--     p.PatientId, u.Email, u.FirstName, u.LastName,
--     u.Gender, u.PhoneNumber, u.City, u.AddressDetail
-- ORDER BY 
--     p.PatientId;

USE ClinicSystemDB;

select * from user where userid like '%pat%';
select * from patient ;
SELECT ProfilePicture, DATE_FORMAT(DateOfBirth, '%Y-%m-%d') AS formatted_dob FROM Patient WHERE PatientId = 'PAT0000001';
select patientid from medicalhistory group by patientid order by counts desc limit 1;

select * from branchbookings WHERE patientId = 'PAT0000002';
SELECT Email, FirstName, LastName, Gender, PhoneNumber, City, AddressDetail FROM User WHERE UserId = 'PAT0000002';
-- SET SQL_SAFE_UPDATES = 0;
-- UPDATE Doctor d
-- JOIN `User` u ON d.DoctorId = u.UserId
-- SET d.ProfilePicture = CASE 
--     WHEN u.Gender = 0 THEN CONCAT('profile_pictures\\doctors\\doctor', FLOOR(1 + (RAND() * 5)), '.jpg')
--     WHEN u.Gender = 1 THEN CONCAT('profile_pictures\\doctors\\doctorf', FLOOR(1 + (RAND() * 5)), '.jpg')
-- END
-- WHERE u.RoleName = 'Doctor';
-- SET SQL_SAFE_UPDATES = 1;

-- SET SQL_SAFE_UPDATES = 0;
-- UPDATE Patient p
-- JOIN `User` u ON p.PatientId = u.UserId
-- SET p.ProfilePicture = CASE 
--     WHEN u.Gender = 0 THEN CONCAT('profile_pictures\\patients\\patient', FLOOR(1 + (RAND() * 5)), '.jpg')
--     WHEN u.Gender = 1 THEN CONCAT('profile_pictures\\patients\\patientf', FLOOR(1 + (RAND() * 5)), '.jpg')
-- END
-- WHERE u.RoleName = 'Patient';
-- SET SQL_SAFE_UPDATES = 1;

-- select * from branchbookings where appointmentstatus = 'Cancelled' order by bookingid desc;
SELECT 
	bb.BookingId, 
	bb.DoctorId, 
	DATE_FORMAT(bb.AppointmentDate, '%Y-%m-%d') AS AppointmentDate, 
	DATE_FORMAT(bb.AppointmentHour, '%H:%i') AS AppointmentHour,
	bb.DoctorName,
	u.Gender,
	s.SpecialtyName, 
    br.BranchName,
	bb.AppointmentStatus, 
	bb.CheckUpType, 
	bb.ReasonOfVisit
FROM BranchBookings bb
JOIN `User` u ON bb.DoctorId = u.UserId
LEFT JOIN Doctor d ON bb.DoctorId = d.DoctorId
LEFT JOIN Specialty s ON d.SpecialtyId = s.SpecialtyId
LEFT JOIN ClinicBranch br ON d.BranchNo = br.BranchNo
WHERE bb.PatientId = 'PAT0000003'
ORDER BY 
	CONCAT(AppointmentDate, ' ', STR_TO_DATE(bb.AppointmentHour, '%H:%i')) ASC; 

-- SELECT d.DoctorId, d.ProfilePicture, d.Description, s.SpecialtyName, u.FirstName, u.LastName, cb.BranchName
--         FROM Doctor d
--         JOIN Specialty s ON d.SpecialtyId = s.SpecialtyId
--         JOIN `User` u ON d.DoctorId = u.UserId
--         JOIN ClinicBranch cb ON d.BranchNo = cb.BranchNo
--         WHERE u.IsDeleted = 0;

SELECT * FROM Booking WHERE DoctorId = 'DOC0000002';

SELECT 
d.DiseaseName,  
(CASE m.Status 
	WHEN 0 THEN 'Ongoing'
	ELSE 'Recovered'
END) AS MedStatus
FROM MedicalHistory m JOIN Disease d 
ON m.DiseaseId = d.DiseaseId
WHERE m.PatientId = 'PAT0000003'
ORDER BY m.Status ASC;

SELECT 
    * FROM BranchBookings 
WHERE AppointmentDate >= CURDATE() order by patientId ;

SELECT
	d.ProfilePicture, d.SpecialtyId, s.SpecialtyName
FROM Doctor d JOIN Specialty s ON d.SpecialtyId = s.SpecialtyId
WHERE d.DoctorId = 'DOC0000004';

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




