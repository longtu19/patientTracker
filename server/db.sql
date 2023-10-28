-- User Table
CREATE TABLE user (
    user_id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL,
    role VARCHAR(50) NOT NULL,
);

-- Patient Table
CREATE TABLE patient (
    patient_id SERIAL PRIMARY KEY,
    user_id INT REFERENCES user(user_id) ON DELETE CASCADE,
    date_of_birth DATE,
    gender VARCHAR(50),
    address TEXT,
    phone_number VARCHAR(50),
    insurance_info TEXT,
    primary_care_doctor_id INT, -- Foreign key added later
    height INT,
    weight INT
);

-- Doctor Table
CREATE TABLE doctor (
    doctor_id SERIAL PRIMARY KEY,
    user_id INT REFERENCES user(user_id) ON DELETE CASCADE,
    specialty VARCHAR(255),
    qualification TEXT,
    working_hospital TEXT
);

-- Medical Record Table
CREATE TABLE medical_record (
    record_id SERIAL PRIMARY KEY,
    patient_id INT REFERENCES patient(patient_id) ON DELETE CASCADE,
    type VARCHAR(255) NOT NULL,
    date DATE,
    file_link TEXT
);

-- Appointment Table
CREATE TABLE appointment (
    appointment_id SERIAL PRIMARY KEY,
    patient_id INT REFERENCES patient(patient_id) ON DELETE CASCADE,
    doctor_id INT REFERENCES doctor(doctor_id) ON DELETE CASCADE,
    scheduled_date_time TIMESTAMP,
    status VARCHAR(50) DEFAULT 'scheduled' -- Values like 'scheduled', 'canceled', 'completed'
);

--Doctor's Work Hours Table
CREATE TABLE doctor_work_hours(
    availability_id SERIAL PRIMARY KEY,
    doctor_id INT REFERENCES doctor(doctor_id) ON DELETE CASCADE,
    day_of_week VARCHAR(3) NOT NULL -- Values like 'Mon', 'Tue', 'Wed', etc.
);

-- Add the foreign key for primary_care_doctor_id in patient table
ALTER TABLE patient
ADD FOREIGN KEY (primary_care_doctor_id) REFERENCES doctor(doctor_id) ON DELETE SET NULL;