create database phonepe_pulse_project;

use phonepe_pulse_project;

CREATE TABLE agg_trans (
    State varchar(255),
    Year int,
    Quarter int,
    Transaction_type varchar(255),
    Transaction_count bigint,
    Transaction_amount float
);

CREATE TABLE agg_user(
    State varchar(255),
    Year int,
    Quarter int,
    Agg_User_device varchar(255),
    Agg_User_count bigint,
    Agg_Device_Percentage float
);

 CREATE TABLE map_trans(
     State varchar(255),
     Year int,
     Quarter int,
     Districts varchar(255), 
     Map_Transaction_count bigint,
     Map_Transaction_amount bigint
);

create table  map_user(
    State varchar(255),
    Year int,
    Quarter int,
    Districts varchar(255),
    Registered_Users bigint,
    App_Opens bigint
);



create table top_user(
					State varchar(255),
                    Year int, 
                    Quarter int, 
                    Pincodes int, 
                    Registered_User bigint
);

SELECT t.State, SUM(u.Registered_User) AS Total_Registered_Users
FROM top_user u
JOIN top_trans t ON u.State = t.State
GROUP BY t.State
ORDER BY Total_Registered_Users DESC
LIMIT 10;


SELECT State, SUM(Transaction_amount) AS Total_Transaction_Amount
FROM agg_trans
GROUP BY State
ORDER BY Total_Transaction_Amount DESC
LIMIT 10;

SELECT State, SUM(Transaction_amount) AS Total_Transaction_Amount
FROM agg_trans
GROUP BY State
ORDER BY Total_Transaction_Amount 
LIMIT 10;

SELECT State, avg(Transaction_amount) AS Total_avg_Transaction_Amount
FROM agg_trans
GROUP BY State
ORDER BY Total_Transaction_Amount desc
LIMIT 10;

SELECT State, sum(Transaction_count) AS Total_Transaction_Count
FROM agg_trans
GROUP BY State
ORDER BY Total_Transaction_Count desc 
LIMIT 10;


SELECT State, avg(Transaction_amount) AS Total_Transaction_Count
FROM agg_trans
GROUP BY State
ORDER BY Total_Transaction_Count 
LIMIT 10;
