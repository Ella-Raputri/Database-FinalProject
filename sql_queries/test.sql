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
