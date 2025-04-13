use srm_ehr;
INSERT INTO departments (dept_name, building, rooms) VALUES ('General Medicine', 'Building A', '101-110');
INSERT INTO departments (dept_name, building, rooms) VALUES ('Cardiology', 'Building B', '201-210');
INSERT INTO departments (dept_name, building, rooms) VALUES ('Neurology', 'Building C', '301-305');
INSERT INTO departments (dept_name, building, rooms) VALUES ('Pediatrics', 'Building A', '111-120');
INSERT INTO departments (dept_name, building, rooms) VALUES ('Obstetrics and Gynecology', 'Building D', '401-410');
INSERT INTO departments (dept_name, building, rooms) VALUES ('Oncology', 'Building E', '501-510');
INSERT INTO departments (dept_name, building, rooms) VALUES ('Orthopedics', 'Building B', '211-220');
INSERT INTO departments (dept_name, building, rooms) VALUES ('Urology', 'Building F', '601-605');
INSERT INTO departments (dept_name, building, rooms) VALUES ('Dermatology', 'Building A', '121-125');
INSERT INTO departments (dept_name, building, rooms) VALUES ('Gastroenterology', 'Building C', '306-310');
INSERT INTO departments (dept_name, building, rooms) VALUES ('Nephrology', 'Building F', '606-610');
INSERT INTO departments (dept_name, building, rooms) VALUES ('Pulmonology', 'Building D', '411-415');
INSERT INTO departments (dept_name, building, rooms) VALUES ('Psychiatry', 'Building G', '701-705');
INSERT INTO departments (dept_name, building, rooms) VALUES ('Ophthalmology', 'Building H', '801-805');
INSERT INTO departments (dept_name, building, rooms) VALUES ('ENT', 'Building H', '806-810');
INSERT INTO users (id, name, email, password, dob, role) 
VALUES ('a_1', 'Admin One', 'admin1@example.com', NULL, '1980-01-01', 'admin');

-- Doctors
INSERT INTO users (id, name, email, password, dob, role) 
VALUES 
('d_1', 'Dr. Doc1', 'doc1@example.com', NULL, '1971-06-15', 'doctor'),
('d_2', 'Dr. Doc2', 'doc2@example.com', NULL, '1972-06-15', 'doctor'),
('d_3', 'Dr. Doc3', 'doc3@example.com', NULL, '1973-06-15', 'doctor'),
('d_4', 'Dr. Doc4', 'doc4@example.com', NULL, '1974-06-15', 'doctor'),
('d_5', 'Dr. Doc5', 'doc5@example.com', NULL, '1975-06-15', 'doctor');

-- Patients
INSERT INTO users (id, name, email, password, dob, role) 
VALUES 
('p_1', 'Patient1', 'patient1@example.com', NULL, '1991-03-20', 'patient'),
('p_2', 'Patient2', 'patient2@example.com', NULL, '1992-03-20', 'patient'),
('p_3', 'Patient3', 'patient3@example.com', NULL, '1993-03-20', 'patient'),
('p_4', 'Patient4', 'patient4@example.com', NULL, '1994-03-20', 'patient'),
('p_5', 'Patient5', 'patient5@example.com', NULL, '1995-03-20', 'patient');
INSERT INTO approved_admins (name, dob, email) VALUES ('Admin One', '1980-01-01', 'admin1@example.com');
INSERT -- First, get the department_id for each department

-- First, get the department_id for each department
SELECT id, dept_name FROM departments;

-- Then insert doctors referencing the department_id
INSERT INTO approved_doctors (name, dob, email, department, department_id)
VALUES 
('Dr. Doc1', '1971-06-15', 'doc1@example.com', 'General Medicine', 1),
('Dr. Doc2', '1972-06-15', 'doc2@example.com', 'Cardiology', 2),
('Dr. Doc3', '1973-06-15', 'doc3@example.com', 'Neurology', 3),
('Dr. Doc4', '1974-06-15', 'doc4@example.com', 'Pediatrics', 4),
('Dr. Doc5', '1975-06-15', 'doc5@example.com', 'Obstetrics and Gynecology', 5);

INSERT INTO approved_patients (name, dob, email) VALUES ('Patient1', '1991-03-20', 'patient1@example.com');
INSERT INTO approved_patients (name, dob, email) VALUES ('Patient2', '1992-03-20', 'patient2@example.com');
INSERT INTO approved_patients (name, dob, email) VALUES ('Patient3', '1993-03-20', 'patient3@example.com');
INSERT INTO approved_patients (name, dob, email) VALUES ('Patient4', '1994-03-20', 'patient4@example.com');
INSERT INTO approved_patients (name, dob, email) VALUES ('Patient5', '1995-03-20', 'patient5@example.com');
INSERT INTO patients (id, name, dob, age, gender, symptoms, diagnosis, created_by) VALUES ('p_1', 'Patient1', '1991-03-20', 34, 'Male', 'Cough and fever', 'Viral Infection', 'd_1');
INSERT INTO patients (id, name, dob, age, gender, symptoms, diagnosis, created_by) VALUES ('p_2', 'Patient2', '1992-03-20', 33, 'Female', 'Cough and fever', 'Viral Infection', 'd_2');
INSERT INTO patients (id, name, dob, age, gender, symptoms, diagnosis, created_by) VALUES ('p_3', 'Patient3', '1993-03-20', 32, 'Male', 'Cough and fever', 'Viral Infection', 'd_3');
INSERT INTO patients (id, name, dob, age, gender, symptoms, diagnosis, created_by) VALUES ('p_4', 'Patient4', '1994-03-20', 31, 'Female', 'Cough and fever', 'Viral Infection', 'd_4');
INSERT INTO patients (id, name, dob, age, gender, symptoms, diagnosis, created_by) VALUES ('p_5', 'Patient5', '1995-03-20', 30, 'Male', 'Cough and fever', 'Viral Infection', 'd_5');
-- Dummy Appointments with department, building, and room_no
INSERT INTO appointments (patient_id, doctor_id, appointment_time, notes, dept_name, building, room_no)
VALUES
('p_1', 'd_1', '2025-04-15 10:00:00', 'Routine check-up', 'General Medicine', 'Building A', '101'),
('p_2', 'd_2', '2025-04-15 11:00:00', 'Chest pain diagnosis', 'Cardiology', 'Building B', '202'),
('p_3', 'd_3', '2025-04-16 09:30:00', 'Skin rash review', 'Dermatology', 'Building C', '305'),
('p_4', 'd_4', '2025-04-16 14:00:00', 'Kidney consultation', 'Nephrology', 'Building D', '404'),
('p_5', 'd_5', '2025-04-17 15:00:00', 'Follow-up visit', 'Neurology', 'Building E', '512');

INSERT INTO prescriptions (patient_id, doctor_id, medicine, dosage, instructions, date_issued) VALUES ('p_1', 'd_1', 'Medicine 0', 'Twice a day', 'After meals', '2025-04-13');
INSERT INTO prescriptions (patient_id, doctor_id, medicine, dosage, instructions, date_issued) VALUES ('p_2', 'd_2', 'Medicine 1', 'Twice a day', 'After meals', '2025-04-13');
INSERT INTO prescriptions (patient_id, doctor_id, medicine, dosage, instructions, date_issued) VALUES ('p_3', 'd_3', 'Medicine 2', 'Twice a day', 'After meals', '2025-04-13');
INSERT INTO prescriptions (patient_id, doctor_id, medicine, dosage, instructions, date_issued) VALUES ('p_4', 'd_4', 'Medicine 3', 'Twice a day', 'After meals', '2025-04-13');
INSERT INTO prescriptions (patient_id, doctor_id, medicine, dosage, instructions, date_issued) VALUES ('p_5', 'd_5', 'Medicine 4', 'Twice a day', 'After meals', '2025-04-13');
INSERT INTO reports (patient_id, file_path, uploaded_by, uploaded_at) VALUES ('p_1', 'reports/p_1_report.pdf', 'd_1', '2025-04-13 19:55:28');
INSERT INTO reports (patient_id, file_path, uploaded_by, uploaded_at) VALUES ('p_2', 'reports/p_2_report.pdf', 'd_2', '2025-04-13 19:55:28');
INSERT INTO reports (patient_id, file_path, uploaded_by, uploaded_at) VALUES ('p_3', 'reports/p_3_report.pdf', 'd_3', '2025-04-13 19:55:28');
INSERT INTO reports (patient_id, file_path, uploaded_by, uploaded_at) VALUES ('p_4', 'reports/p_4_report.pdf', 'd_4', '2025-04-13 19:55:28');
INSERT INTO reports (patient_id, file_path, uploaded_by, uploaded_at) VALUES ('p_5', 'reports/p_5_report.pdf', 'd_5', '2025-04-13 19:55:28');