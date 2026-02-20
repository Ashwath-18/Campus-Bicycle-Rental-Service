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

INSERT INTO Stations (station_id, block_name, total_slots) VALUES
(1, 'Kashyapa Bhavanam', 20),
(2, 'Sri Vyasa Maharshi Bhavanam', 20),
(3, 'Nachiketas Bhavanam', 20),
(4, 'Yagnavalkya Bhavanam', 20),
(5, 'Vasishta Bhavanam', 20),
(6, 'Agasthya Bhavanam', 20),
(7, 'Gauthama Bhavanam (PG Boys)', 20),
(8, 'Kapila Bhavanam', 20),
(9, 'Bhrigu Bhavanam', 20);

INSERT INTO Bicycles (bicycle_id, type, station_id, status, battery_status) VALUES
(1, 'Normal', 1, 'Available', NULL),
(2, 'EV', 1, 'Available', 'Full'),
(3, 'Normal', 2, 'Available', NULL),
(4, 'EV', 2, 'Available', 'Full'),
(5, 'Normal', 3, 'Available', NULL),
(6, 'EV', 3, 'Available', 'Full'),
(7, 'Normal', 4, 'Available', NULL),
(8, 'EV', 4, 'Available', 'Full'),
(9, 'Normal', 5, 'Available', NULL),
(10, 'EV', 5, 'Available', 'Full'),
(11, 'Normal', 6, 'Available', NULL),
(12, 'EV', 6, 'Available', 'Full'),
(13, 'Normal', 7, 'Available', NULL),
(14, 'EV', 7, 'Available', 'Full'),
(15, 'Normal', 8, 'Available', NULL),
(16, 'EV', 8, 'Available', 'Full'),
(17, 'Normal', 9, 'Available', NULL),
(18, 'EV', 9, 'Available', 'Full');

INSERT INTO Stations (station_id, block_name, total_slots) VALUES
(10, 'Adithi Bhavanam', 20),
(11, 'Mythreyi Bhavanam', 20),
(12, 'Gargi Bhavanam', 20),
(13, 'Savithri Bhavanam', 20);

INSERT INTO Stations (station_id, block_name, total_slots) VALUES
(14, 'Academic Block 1 - AB-1', 30),
(15, 'Academic Block 2 - AB-2', 30),
(16, 'Academic Block 3 - AB-3', 30),
(17, 'MBA / Business Block', 25);

INSERT INTO Stations (station_id, block_name, total_slots) VALUES
(18, 'Sopanam Canteen', 20),
(19, 'Samudra Canteen', 20),
(20, 'MBA Canteen', 20);