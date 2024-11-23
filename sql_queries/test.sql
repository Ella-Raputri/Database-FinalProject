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
        

select * from booking order by appointmentdate desc;


