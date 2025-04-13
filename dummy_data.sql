

-- Insert dummy users
INSERT INTO users (name, email, dob, role)
VALUES 
  ('Alice Smith', 'alice@example.com', '1990-05-12', 'patient'),
  ('Dr. John Doe', 'john.doe@example.com', '1980-11-20', 'doctor'),
  ('Admin Jane', 'admin.jane@example.com', '1975-02-28', 'admin');




-- Insert dummy doctor profiles (assuming user IDs start from 1)
INSERT INTO doctors (user_id, department, qualification, phone) VALUES
(1, 'Cardiology', 'MD Cardiology', '9876543210'),
(2, 'Neurology', 'MD Neurology', '8765432109');



-- Insert dummy admin profiles (assuming user IDs start from 3)
INSERT INTO admins (user_id, department, contact_number) VALUES
(3, 'Front Desk', '9123456780'),
(4, 'Records', '9234567890');



-- Insert dummy patient records (added by doctors with user_id 1 or 2)
INSERT INTO patients (name, age, gender, symptoms, diagnosis, added_by) VALUES
('John Doe', 45, 'male', 'Chest pain, shortness of breath', 'Mild heart attack', 1),
('Alice Green', 30, 'female', 'Frequent headaches, dizziness', 'Migraine', 2),
('Ramesh Kumar', 55, 'male', 'High BP, tiredness', 'Hypertension', 1),
('Sita Rani', 60, 'female', 'Memory loss, confusion', 'Early Alzheimer's', 2);

