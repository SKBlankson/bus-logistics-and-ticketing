drop schema if exists logistics_eticketing;
create schema logistics_eticketing;
use logistics_eticketing;

create table Ashesi_Employee(
    employee_id VARCHAR(10) PRIMARY KEY NOT NULL ,
    f_name varchar(100) NOT NULL ,
    l_name varchar(100) NOT NULL ,
    ashesi_email VARCHAR(100) NULL ,
    account_password varchar(250) NULL ,
    momo_network varchar(50) NULL CHECK ( momo_network IN ('MTN','Vodafone','AirtelTigo')) ,
    momo_number varchar(10) NULL
    );

create table Vehicles(
    license_plate VARCHAR(20) PRIMARY KEY NOT NULL ,
    vehicle_type varchar(15) NOT NULL CHECK ( vehicle_type IN ('Bus','Private Vehicle') )  ,
    capacity int NOT NULL,
    descriptive_name varchar(100) NOT NULL,
    make varchar(100) NULL,
    model varchar(100) NULL,
    permit_issuer varchar(100) NULL,
    permit_issue_date date NULL,
    permit_expiry_date date NULL,
    assigned_driver varchar(10) NULL,
    last_maintenance_date date DEFAULT NULL,
    maintenance_cycle_days int(11) DEFAULT 30,
    next_maintenance_date date DEFAULT NULL,
    FOREIGN KEY (assigned_driver) REFERENCES Ashesi_Employee(employee_id) ON DELETE RESTRICT ON UPDATE CASCADE
);

create table Stops
(
    stop_id varchar(20) PRIMARY KEY NOT NULL,
    stop_name varchar(150) NOT NULL UNIQUE,
    cost float NOT NULL DEFAULT 0
);


CREATE TABLE Semester_Schedule (
    schedule_id INT AUTO_INCREMENT PRIMARY KEY,
    day_of_week VARCHAR(9) NOT NULL CHECK (day_of_week IN ('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday')),
    pickup_location VARCHAR(20) NOT NULL,
    final_destination VARCHAR(20) NOT NULL,
    departure_time TIME NOT NULL,
    arrival_time TIME NOT NULL,
    assigned_driver varchar(10) DEFAULT NULL,
    assigned_vehicle varchar(20) DEFAULT NULL,
    time_period varchar(7) NOT NULL,
    FOREIGN KEY (pickup_location) REFERENCES Stops(stop_id) ON DELETE RESTRICT ON UPDATE CASCADE,
    FOREIGN KEY (final_destination) REFERENCES Stops(stop_id) ON DELETE RESTRICT ON UPDATE CASCADE,
    FOREIGN KEY (assigned_driver) REFERENCES Ashesi_Employee(employee_id) ON DELETE RESTRICT ON UPDATE CASCADE,
    FOREIGN KEY (assigned_vehicle) REFERENCES Vehicles(license_plate) ON DELETE RESTRICT ON UPDATE CASCADE
);

CREATE TABLE Semester_Schedule_Stop (
    schedule_id INT NOT NULL ,
    stop_id VARCHAR(20) NOT NULL,
    departure_time TIME DEFAULT NULL,
    arrival_time TIME NOT NULL,
    PRIMARY KEY (schedule_id, stop_id),
    FOREIGN KEY (schedule_id) REFERENCES Semester_Schedule(schedule_id) ON DELETE RESTRICT ON UPDATE CASCADE,
    FOREIGN KEY (stop_id) REFERENCES Stops(stop_id) ON DELETE RESTRICT
);

CREATE TABLE Driver (
    employee_id VARCHAR(10) PRIMARY KEY ,
    drivers_license_number VARCHAR(20) NOT NULL,
    license_expiry_date DATE NOT NULL,
    FOREIGN KEY (employee_id) REFERENCES Ashesi_Employee(employee_id) ON DELETE RESTRICT ON UPDATE CASCADE
);

CREATE TABLE Staff (
    employee_id VARCHAR(10) PRIMARY KEY,
    FOREIGN KEY (employee_id) REFERENCES Ashesi_Employee(employee_id) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE Trip (
    trip_id VARCHAR(10) PRIMARY KEY,
    schedule_id INT NOT NULL,
    trip_date DATETIME NOT NULL,
    assigned_driver VARCHAR(10) NOT NULL,
    assigned_vehicle VARCHAR(20) NOT NULL,
    FOREIGN KEY (assigned_driver) REFERENCES  Driver(employee_id) ON DELETE RESTRICT ON UPDATE CASCADE,
    FOREIGN KEY (assigned_vehicle) REFERENCES  Vehicles(license_plate) ON DELETE RESTRICT ON UPDATE CASCADE,
    FOREIGN KEY (schedule_id) REFERENCES Semester_Schedule(schedule_id) ON DELETE RESTRICT ON UPDATE CASCADE
);

CREATE TABLE Ticket (
    ticket_id INT AUTO_INCREMENT PRIMARY KEY,
    trip_id VARCHAR(10) NOT NULL,
    employee_id VARCHAR(10) NOT NULL,
    purchase_date DATETIME NOT NULL,
    ticket_price FLOAT NOT NULL,
    FOREIGN KEY (trip_id) REFERENCES Trip(trip_id) ON DELETE RESTRICT ON UPDATE CASCADE,
    FOREIGN KEY (employee_id) REFERENCES Ashesi_Employee(employee_id) ON DELETE RESTRICT ON UPDATE CASCADE
);

CREATE TABLE Employee_Trip (
    trip_id VARCHAR(10) NOT NULL,
    ticket_id INT,
    employee_id VARCHAR(10) NOT NULL,
    PRIMARY KEY (trip_id, employee_id),
    FOREIGN KEY (trip_id) REFERENCES Trip(trip_id) ON DELETE RESTRICT ON UPDATE CASCADE,
    FOREIGN KEY (ticket_id) REFERENCES Ticket(ticket_id) ON DELETE RESTRICT ON UPDATE CASCADE,
    FOREIGN KEY (employee_id) REFERENCES Ashesi_Employee(employee_id) ON DELETE RESTRICT ON UPDATE CASCADE
);

CREATE TABLE Private_Trip (
    trip_id VARCHAR(10) NOT NULL,
    trip_notes VARCHAR(600) DEFAULT NULL,
    client_list VARCHAR(600) DEFAULT NULL,
    PRIMARY KEY (trip_id),
    FOREIGN KEY (trip_id) REFERENCES Trip(trip_id) ON DELETE RESTRICT ON UPDATE CASCADE
);

CREATE TABLE Staff_Shuttle_Trip (
    trip_id VARCHAR(10) PRIMARY KEY,
    FOREIGN KEY (trip_id) REFERENCES Trip(trip_id) ON DELETE RESTRICT ON UPDATE CASCADE
);


INSERT INTO `ashesi_employee` (`employee_id`, `f_name`, `l_name`, `ashesi_email`, `account_password`, `momo_network`, `momo_number`) VALUES
('11232025', 'David', 'Yebuah', NULL, NULL, NULL, '0556207958'),
('12342024', 'Adelle', 'Nanka Bruce', NULL, NULL, NULL, '023456214'),
('29362024', 'Samuel', 'Blankson', NULL, NULL, NULL, '0556207957');

INSERT INTO `driver` (`employee_id`, `drivers_license_number`, `license_expiry_date`) VALUES
('11232025', 'RX-88SD', '2023-12-13'),
('29362024', 'RX-sdsd', '2023-10-10');


INSERT INTO `vehicles` (`license_plate`, `vehicle_type`, `capacity`, `descriptive_name`, `make`, `model`, `permit_issuer`, `permit_issue_date`, `permit_expiry_date`, `assigned_driver`, `last_maintenance_date`, `maintenance_cycle_days`, `next_maintenance_date`) VALUES
('GE-111-Y', 'Private Vehicle', 60, 'Green Bus', 'Toyota', 'Corolla Cross', 'GRA', '2012-10-10', '2023-12-10', '29362024', NULL, 30, NULL),
('GE-332-Y', 'Private Vehicle', 60, 'Green Bus', 'Toyota', 'Corolla Cross', 'GRA', '2012-10-10', '2023-12-10', '29362024', NULL, 30, NULL),
('GE-4623-Y', 'Bus', 60, 'Green Bus', 'Toyota', 'Sprinter', 'GRA', '2012-10-10', '2023-12-10', '29362024', NULL, 30, NULL),
('GE-463-Y', 'Bus', 60, 'Yellow Bus', 'Toyota', 'Sprinter', 'GRA', '2012-10-10', '2023-12-10', '29362024', NULL, 30, NULL),
('GE-48-Y', 'Bus', 40, 'Green Bus', 'Toyota', 'Sprinter', 'GRA', '2012-10-10', '2023-12-10', '29362024', NULL, 30, NULL);

