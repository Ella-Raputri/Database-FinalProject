USE ClinicSystemDB;
-- SET SQL_SAFE_UPDATES = 0;

-- UPDATE Booking
-- SET AppointmentStatus = 'Pending'
-- WHERE AppointmentDate > CURDATE();

-- UPDATE Booking
-- SET AppointmentStatus = 'Completed'
-- WHERE AppointmentDate < CURDATE();

-- SET SQL_SAFE_UPDATES = 1; -- Re-enable safe update mode


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

select * from user order by userid desc;
select * from patient order by patientid desc;
select * from doctor ;
select * from admin;

select * from branchbookings where appointmentstatus = 'Cancelled' order by bookingid desc;
SELECT 
	bb.BookingId, 
	bb.PatientId, 
	u.Email, 
	bb.PatientName,
	u.Gender,
	u.PhoneNumber, 
	p.ProfilePicture,
	DATE_FORMAT(bb.AppointmentDate, '%Y-%m-%d') AS AppointmentDate, 
	DATE_FORMAT(bb.AppointmentHour, '%H:%i') AS AppointmentHour, 
	bb.AppointmentStatus, 
	bb.CheckUpType, 
	bb.ReasonOfVisit
FROM BranchBookings bb
JOIN `User` u ON bb.PatientId = u.UserId
LEFT JOIN Patient p ON bb.PatientId = p.PatientId
WHERE bb.DoctorId = 'DOC0000004' AND bb.AppointmentStatus = 'Pending'
ORDER BY bb.AppointmentDate ASC, STR_TO_DATE(bb.AppointmentHour, '%H:%i') ASC;


SELECT 
    COUNT(BookingId) FROM BranchBookings 
WHERE DoctorId = 'DOC0000004' AND AppointmentDate = CURDATE();



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




