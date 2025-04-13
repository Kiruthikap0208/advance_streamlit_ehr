CREATE DATABASE IF NOT EXISTS srm_ehr;
USE srm_ehr;
-- USERS TABLE
CREATE TABLE IF NOT EXISTS users (
    id VARCHAR(20) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(100), -- Set to NULL initially
    dob DATE,
    role ENUM('admin', 'doctor', 'patient') NOT NULL
);

-- APPROVED ADMINS
CREATE TABLE IF NOT EXISTS approved_admins (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    dob DATE,
    email VARCHAR(100)
);

-- APPROVED DOCTORS
DROP TABLE IF EXISTS approved_doctors;
CREATE TABLE approved_doctors (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    dob DATE,
    email VARCHAR(100),
    department VARCHAR(100),
    department_id INT,
    FOREIGN KEY (department_id) REFERENCES departments(id)	
);

-- APPROVED PATIENTS
CREATE TABLE IF NOT EXISTS approved_patients (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    dob DATE,
    email VARCHAR(100)
);

-- PATIENTS TABLE (Linked to users)
CREATE TABLE IF NOT EXISTS patients (
    id VARCHAR(20) PRIMARY KEY,
    name VARCHAR(100),
    dob DATE,
    age INT,
    gender VARCHAR(10),
    symptoms TEXT,
    diagnosis TEXT,
    created_by VARCHAR(20),
    FOREIGN KEY (id) REFERENCES users(id)
);

-- DOCTOR DEPARTMENTS
CREATE TABLE IF NOT EXISTS departments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    dept_name VARCHAR(100) NOT NULL UNIQUE,
    building VARCHAR(50),
    rooms VARCHAR(50)
);

-- APPOINTMENTS TABLE
CREATE TABLE IF NOT EXISTS appointments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    patient_id VARCHAR(20),
    doctor_id VARCHAR(20),
    appointment_time DATETIME,
    notes TEXT,
    FOREIGN KEY (patient_id) REFERENCES users(id),
    FOREIGN KEY (doctor_id) REFERENCES users(id)
);

-- PRESCRIPTIONS
CREATE TABLE IF NOT EXISTS prescriptions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    patient_id VARCHAR(20),
    doctor_id VARCHAR(20),
    medicine TEXT,
    dosage TEXT,
    instructions TEXT,
    date_issued DATE DEFAULT (CURRENT_DATE),
    FOREIGN KEY (patient_id) REFERENCES users(id),
    FOREIGN KEY (doctor_id) REFERENCES users(id)
);

-- REPORTS
CREATE TABLE IF NOT EXISTS reports (
    id INT AUTO_INCREMENT PRIMARY KEY,
    patient_id VARCHAR(20),
    file_path VARCHAR(255),
    uploaded_by VARCHAR(20),
    uploaded_at DATETIME,
    FOREIGN KEY (patient_id) REFERENCES users(id)
);

ALTER TABLE appointments
ADD COLUMN dept_name VARCHAR(100),
ADD COLUMN building VARCHAR(50),
ADD COLUMN room_no VARCHAR(50);


