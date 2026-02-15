CREATE TABLE Students (
    roll_no VARCHAR(20) PRIMARY KEY,
    name VARCHAR(100),
    department VARCHAR(50)
);

CREATE TABLE Stations (
    station_id INT PRIMARY KEY AUTO_INCREMENT,
    block_name VARCHAR(50),
    total_slots INT
);

CREATE TABLE Bicycles (
    bicycle_id INT PRIMARY KEY AUTO_INCREMENT,
    type ENUM('Normal','EV'),
    station_id INT,
    status ENUM('Available','In Use','Maintenance'),
    battery_status VARCHAR(50),
    FOREIGN KEY (station_id) REFERENCES Stations(station_id)
);

CREATE TABLE Rentals (
    rental_id INT PRIMARY KEY AUTO_INCREMENT,
    roll_no VARCHAR(20),
    bicycle_id INT,
    grab_time DATETIME,
    return_time DATETIME,
    returned_station INT,
    FOREIGN KEY (roll_no) REFERENCES Students(roll_no),
    FOREIGN KEY (bicycle_id) REFERENCES Bicycles(bicycle_id)
);
