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
    battery_percentage INT DEFAULT NULL,
    FOREIGN KEY (station_id) REFERENCES Stations(station_id)
);

CREATE TABLE Rentals (
    rental_id INT PRIMARY KEY AUTO_INCREMENT,
    roll_no VARCHAR(20),
    bicycle_id INT,
    grab_time DATETIME,
    grab_station_id INT,
    return_time DATETIME,
    return_station_id INT,
    FOREIGN KEY (roll_no) REFERENCES Students(roll_no),
    FOREIGN KEY (bicycle_id) REFERENCES Bicycles(bicycle_id),
    FOREIGN KEY (grab_station_id) REFERENCES Stations(station_id),
    FOREIGN KEY (return_station_id) REFERENCES Stations(station_id)
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
(9, 'Bhrigu Bhavanam', 20),
(10, 'Adithi Bhavanam', 20),
(11, 'Mythreyi Bhavanam', 20),
(12, 'Gargi Bhavanam', 20),
(13, 'Savithri Bhavanam', 20),
(14, 'Academic Block 1 - AB-1', 30),
(15, 'Academic Block 2 - AB-2', 30),
(16, 'Academic Block 3 - AB-3', 30),
(17, 'MBA / Business Block', 25),
(18, 'Sopanam Canteen', 20),
(19, 'Samudra Canteen', 20),
(20, 'MBA Canteen', 20);

INSERT INTO Bicycles (bicycle_id, type, station_id, status, battery_percentage) VALUES
(1, 'Normal', 1, 'Available', NULL),
(2, 'EV', 1, 'Available', '100'),
(3, 'Normal', 2, 'Available', NULL),
(4, 'EV', 2, 'Available', '100'),
(5, 'Normal', 3, 'Available', NULL),
(6, 'EV', 3, 'Available', '100'),
(7, 'Normal', 4, 'Available', NULL),
(8, 'EV', 4, 'Available', '100'),
(9, 'Normal', 5, 'Available', NULL),
(10, 'EV', 5, 'Available', '100'),
(11, 'Normal', 6, 'Available', NULL),
(12, 'EV', 6, 'Available', '100'),
(13, 'Normal', 7, 'Available', NULL),
(14, 'EV', 7, 'Available', '100'),
(15, 'Normal', 8, 'Available', NULL),
(16, 'EV', 8, 'Available', '100'),
(17, 'Normal', 9, 'Available', NULL),
(18, 'EV', 9, 'Available', '100');


INSERT INTO Students (roll_no, name) VALUES
('CB.PS.I5DAS24001', 'Abhiram Pazhayath'),
('CB.PS.I5DAS24002', 'Anugraha G'),
('CB.PS.I5DAS24003', 'Archana R'),
('CB.PS.I5DAS24004', 'Ashwath V'),
('CB.PS.I5DAS24005', 'Aswathy P'),
('CB.PS.I5DAS24006', 'Avantika Lakssmi S'),
('CB.PS.I5DAS24007', 'Deepthi A'),
('CB.PS.I5DAS24008', 'Devika Kishore'),
('CB.PS.I5DAS24009', 'Dhavamuniselvi'),
('CB.PS.I5DAS24010', 'Dheeraj V'),
('CB.PS.I5DAS24011', 'Dheekshith R'),
('CB.PS.I5DAS24012', 'Gautham S'),
('CB.PS.I5DAS24013', 'Gayathry E'),
('CB.PS.I5DAS24014', 'Hiranya G'),
('CB.PS.I5DAS24015', 'Jayarakshana G'),
('CB.PS.I5DAS24016', 'Kavin A K'),
('CB.PS.I5DAS24017', 'Krishnapriya M'),
('CB.PS.I5DAS24018', 'L Karpakam'),
('CB.PS.I5DAS24019', 'Manu Muralitharan'),
('CB.PS.I5DAS24020', 'Meenakshi Vinu'),
('CB.PS.I5DAS24021', 'Meera V Rajan'),
('CB.PS.I5DAS24022', 'MITHUN D'),
('CB.PS.I5DAS24023', 'Mounash S G'),
('CB.PS.I5DAS24024', 'Mrudula Madhu'),
('CB.PS.I5DAS24025', 'Nandana N Nair'),
('CB.PS.I5DAS24026', 'Neha Praveen C'),
('CB.PS.I5DAS24027', 'Nisitaa S'),
('CB.PS.I5DAS24028', 'Nithyashree V S'),
('CB.PS.I5DAS24029', 'Poojit K S'),
('CB.PS.I5DAS24030', 'Pragadeeshwaran R'),
('CB.PS.I5DAS24031', 'Pravanima G'),
('CB.PS.I5DAS24032', 'Priyadharshini K'),
('CB.PS.I5DAS24033', 'R Monish'),
('CB.PS.I5DAS24034', 'Raghav Krishna V'),
('CB.PS.I5DAS24035', 'S Priyadharshini'),
('CB.PS.I5DAS24036', 'Sabaresh R'),
('CB.PS.I5DAS24037', 'Sangamithra K'),
('CB.PS.I5DAS24038', 'Sanjay R M C'),
('CB.PS.I5DAS24039', 'Sanjith S'),
('CB.PS.I5DAS24040', 'Shivshabaresh B S'),
('CB.PS.I5DAS24041', 'Shreyans R P Haswani'),
('CB.PS.I5DAS24042', 'Shruti Srinivasan'),
('CB.PS.I5DAS24044', 'Sreemathi Ganesan'),
('CB.PS.I5DAS24045', 'Sri Vignesh S'),
('CB.PS.I5DAS24046', 'Sri Sathvyga PS'),
('CB.PS.I5DAS24047', 'Srimaghi S K'),
('CB.PS.I5DAS24049', 'Sujay Karthik'),
('CB.PS.I5DAS24050', 'V S Nandhini'),
('CB.PS.I5DAS24051', 'V Sudarshana'),
('CB.PS.I5DAS24052', 'Vidyalakshmi M K'),
('CB.PS.I5DAS24053', 'Vishnukruthika A D'),
('CB.PS.I5DAS24055', 'Vismaya P P'),
('CB.PS.I5DAS24056', 'Karan S'),
('CB.PS.I5DAS24057', 'Cavin Gaurav B'),
('CB.PS.I5DAS24058', 'Sahana Vardhini K');


# Inserting bicycles for all stations
DELIMITER $$

CREATE PROCEDURE insert_all_bicycles()
BEGIN
    DECLARE station INT DEFAULT 1;
    DECLARE normal_count INT;
    DECLARE ev_count INT;

    WHILE station <= 20 DO

        SET normal_count = 1;
        WHILE normal_count <= 50 DO
            INSERT INTO Bicycles (type, station_id, status, battery_percentage)
            VALUES ('Normal', station, 'Available', NULL);
            SET normal_count = normal_count + 1;
        END WHILE;

        SET ev_count = 1;
        WHILE ev_count <= 20 DO
            INSERT INTO Bicycles (type, station_id, status, battery_percentage)
            VALUES ('EV', station, 'Available', 100);
            SET ev_count = ev_count + 1;
        END WHILE;

        SET station = station + 1;

    END WHILE;

END$$

DELIMITER ;

CALL insert_all_bicycles();