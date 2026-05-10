CREATE DATABASE CyberTrenerDB;


USE CyberTrenerDB;

CREATE TABLE users (
    id INT IDENTITY(1,1) PRIMARY KEY, 
    username NVARCHAR(255) UNIQUE NOT NULL
);


CREATE TABLE workouts (
    id INT IDENTITY(1,1) PRIMARY KEY, 
    user_id INT FOREIGN KEY REFERENCES users(id), 
    date DATETIME, 
    exercise_type NVARCHAR(100), 
    reps INT, 
    duration_sec INT
);
