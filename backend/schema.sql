CREATE DATABASE IF NOT EXISTS smart_healthcare;
USE smart_healthcare;

-- Patients
CREATE TABLE IF NOT EXISTS Patient (
  PatientID INT AUTO_INCREMENT PRIMARY KEY,
  Name VARCHAR(100) NOT NULL,
  Email VARCHAR(100) NOT NULL UNIQUE,
  Phone VARCHAR(20) NOT NULL,
  Password VARCHAR(255) NOT NULL,
  Age INT NOT NULL,
  Gender ENUM('Male','Female','Other') NOT NULL
);

-- Doctors
CREATE TABLE IF NOT EXISTS Doctor (
  DoctorID INT AUTO_INCREMENT PRIMARY KEY,
  Name VARCHAR(100) NOT NULL,
  Email VARCHAR(100) NOT NULL UNIQUE,
  Phone VARCHAR(20) NOT NULL,
  Specialty VARCHAR(100) NOT NULL,
  Password VARCHAR(255) NOT NULL
);

-- Admins
CREATE TABLE IF NOT EXISTS Admin (
  AdminID INT AUTO_INCREMENT PRIMARY KEY,
  Name VARCHAR(100) NOT NULL,
  Email VARCHAR(100) NOT NULL UNIQUE,
  Password VARCHAR(255) NOT NULL
);

-- Doctor Availability
CREATE TABLE IF NOT EXISTS DoctorAvailability (
  AvailabilityID INT AUTO_INCREMENT PRIMARY KEY,
  DoctorID INT NOT NULL,
  Date DATE NOT NULL,
  TimeSlot VARCHAR(20) NOT NULL,
  IsAvailable BOOLEAN NOT NULL DEFAULT TRUE,
  CONSTRAINT fk_availability_doctor FOREIGN KEY (DoctorID) REFERENCES Doctor(DoctorID) ON DELETE CASCADE,
  INDEX idx_doctor_date_time (DoctorID, Date, TimeSlot)
);

-- Appointments
CREATE TABLE IF NOT EXISTS Appointment (
  AppointmentID INT AUTO_INCREMENT PRIMARY KEY,
  PatientID INT NOT NULL,
  DoctorID INT NOT NULL,
  AppointmentDate DATE NOT NULL,
  AppointmentTime VARCHAR(20) NOT NULL,
  Status VARCHAR(20) NOT NULL,
  CONSTRAINT fk_appointment_patient FOREIGN KEY (PatientID) REFERENCES Patient(PatientID) ON DELETE CASCADE,
  CONSTRAINT fk_appointment_doctor FOREIGN KEY (DoctorID) REFERENCES Doctor(DoctorID) ON DELETE CASCADE,
  INDEX idx_appointment_doctor_date_time (DoctorID, AppointmentDate, AppointmentTime)
);


