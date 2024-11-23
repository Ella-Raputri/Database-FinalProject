USE ClinicSystemDB;

select * from user ;
select * from User where UserId LIKE 'ADM%' order by UserID desc limit 10;
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
	CONCAT(DayOfWeek, ': ', 
	TIME_FORMAT(StartHour, '%H:%i'), '-', 
	TIME_FORMAT(EndHour, '%H:%i')) AS Schedule
FROM DoctorSchedule
WHERE DoctorId = 'DOC0000002'
ORDER BY FIELD(DayOfWeek, 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday');

        
select * from doctor;
select * from user;
select * from booking order by appointmentdate desc;


