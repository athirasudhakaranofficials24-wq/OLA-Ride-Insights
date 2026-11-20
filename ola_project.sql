create database ola_project ;
show databases;

USE ola_project;

CREATE TABLE ola_cleaned_data (
    `Date` DATE,
    `Time` TIME,
    Booking_ID VARCHAR(50),
    Booking_Status VARCHAR(50),
    Customer_ID VARCHAR(50),
    Vehicle_Type VARCHAR(50),
    Pickup_Location VARCHAR(100),
    Drop_Location VARCHAR(100),
    V_TAT FLOAT,
    C_TAT FLOAT,
    Canceled_Rides_by_Customer VARCHAR(150),
    Canceled_Rides_by_Driver VARCHAR(150),
    Incomplete_Rides VARCHAR(20),
    Incomplete_Rides_Reason VARCHAR(150),
    Booking_Value FLOAT,
    Payment_Method VARCHAR(50),
    Ride_Distance FLOAT,
    Driver_Ratings FLOAT,
    Customer_Rating FLOAT,
    `Vehicle Images` TEXT
);
SELECT COUNT(*)
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_SCHEMA = 'ola_project'
AND TABLE_NAME = 'ola_cleaned_data';
SHOW TABLES IN ola_project;
USE ola_project;

CREATE TABLE ola_cleaned_data (
    `Date` DATE,
    `Time` TIME,
    Booking_ID VARCHAR(50),
    Booking_Status VARCHAR(50),
    Customer_ID VARCHAR(50),
    Vehicle_Type VARCHAR(50),
    Pickup_Location VARCHAR(100),
    Drop_Location VARCHAR(100),
    V_TAT FLOAT,
    C_TAT FLOAT,
    Canceled_Rides_by_Customer VARCHAR(150),
    Canceled_Rides_by_Driver VARCHAR(150),
    Incomplete_Rides VARCHAR(20),
    Incomplete_Rides_Reason VARCHAR(150),
    Booking_Value FLOAT,
    Payment_Method VARCHAR(50),
    Ride_Distance FLOAT,
    Driver_Ratings FLOAT,
    Customer_Rating FLOAT,
    `Vehicle Images` TEXT
);
SELECT DATABASE();
USE ola_project;
SHOW TABLES;
CREATE TABLE ola_project.ola_cleaned_data (
    `Date` DATE,
    `Time` TIME,
    Booking_ID VARCHAR(50),
    Booking_Status VARCHAR(50),
    Customer_ID VARCHAR(50),
    Vehicle_Type VARCHAR(50),
    Pickup_Location VARCHAR(100),
    Drop_Location VARCHAR(100),
    V_TAT FLOAT,
    C_TAT FLOAT,
    Canceled_Rides_by_Customer VARCHAR(150),
    Canceled_Rides_by_Driver VARCHAR(150),
    Incomplete_Rides VARCHAR(20),
    Incomplete_Rides_Reason VARCHAR(150),
    Booking_Value FLOAT,
    Payment_Method VARCHAR(50),
    Ride_Distance FLOAT,
    Driver_Ratings FLOAT,
    Customer_Rating FLOAT,
    `Vehicle Images` TEXT
);
SELECT COUNT(*)
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_SCHEMA = 'ola_project'
AND TABLE_NAME = 'ola_cleaned_data';
SHOW VARIABLES LIKE 'secure_file_priv';
LOAD DATA INFILE
'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/OLA_Cleaned_Data.csv'
INTO TABLE ola_project.ola_cleaned_data
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(
    `Date`, `Time`, Booking_ID, Booking_Status, Customer_ID,
    Vehicle_Type, Pickup_Location, Drop_Location,
    @V_TAT, @C_TAT,
    Canceled_Rides_by_Customer, Canceled_Rides_by_Driver,
    Incomplete_Rides, Incomplete_Rides_Reason,
    @Booking_Value, Payment_Method, @Ride_Distance,
    @Driver_Ratings, @Customer_Rating, `Vehicle Images`
)
SET
    V_TAT = NULLIF(TRIM(@V_TAT), ''),
    C_TAT = NULLIF(TRIM(@C_TAT), ''),
    Booking_Value = NULLIF(TRIM(@Booking_Value), ''),
    Ride_Distance = NULLIF(TRIM(@Ride_Distance), ''),
    Driver_Ratings = NULLIF(TRIM(@Driver_Ratings), ''),
    Customer_Rating = NULLIF(TRIM(@Customer_Rating), '');
    SELECT COUNT(*) FROM ola_project.ola_cleaned_data;
    SELECT `Date`, `Time`
FROM ola_project.ola_cleaned_data
LIMIT 5;
SELECT
    COUNT(*) AS Total_Rows,
    COUNT(Booking_ID) AS Booking_Count,
    COUNT(DISTINCT Booking_ID) AS Unique_Bookings
FROM ola_project.ola_cleaned_data;
SELECT *
FROM ola_cleaned_data
WHERE Booking_Status = 'Success';
SELECT Vehicle_Type,
AVG(Ride_Distance) AS Average_Ride_Distance
FROM ola_cleaned_data
GROUP BY Vehicle_Type;
SELECT COUNT(*) AS Customer_Cancelled_Rides
FROM ola_cleaned_data
WHERE Booking_Status = 'Canceled by Customer';
SELECT Customer_ID,
       COUNT(*) AS Total_Rides
FROM ola_cleaned_data
GROUP BY Customer_ID
ORDER BY Total_Rides DESC
LIMIT 5;
SELECT Canceled_Rides_by_Driver,
       COUNT(*) AS Total_Cancellations
FROM ola_cleaned_data
WHERE Canceled_Rides_by_Driver IN
('Personal & Car related issue')
GROUP BY Canceled_Rides_by_Driver;
SELECT
    MAX(Driver_Ratings) AS Maximum_Rating,
    MIN(Driver_Ratings) AS Minimum_Rating
FROM ola_cleaned_data
WHERE Vehicle_Type = 'Prime Sedan';
SELECT *
FROM ola_cleaned_data
WHERE Payment_Method = 'UPI';
SELECT Vehicle_Type,
       AVG(Customer_Rating) AS Average_Customer_Rating
FROM ola_cleaned_data
GROUP BY Vehicle_Type;
SELECT SUM(Booking_Value) AS Total_Booking_Value
FROM ola_cleaned_data
WHERE Booking_Status = 'Success';
SELECT Incomplete_Rides_Reason,
       COUNT(*) AS Total_Incomplete_Rides
FROM ola_cleaned_data
WHERE Incomplete_Rides = 'Yes'
GROUP BY Incomplete_Rides_Reason;





