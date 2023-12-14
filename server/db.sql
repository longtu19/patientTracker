-- User Table
CREATE TABLE System_user(
    user_id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL,
    role VARCHAR(50) NOT NULL
);

-- Patient Table
CREATE TABLE Patient (
    patient_id SERIAL PRIMARY KEY,
    user_id INT REFERENCES System_user(user_id) ON DELETE CASCADE,
    date_of_birth DATE,
    sex VARCHAR(50),
    address TEXT,
    phone_number VARCHAR(50),
    insurance_info TEXT,
    primary_care_doctor_id INT, -- Foreign key added later
);

-- Doctor Table
CREATE TABLE Doctor (
    doctor_id SERIAL PRIMARY KEY,
    user_id INT REFERENCES System_user(user_id) ON DELETE CASCADE,
    specialty VARCHAR(255)
);

-- Medical Record Table
CREATE TABLE Medical_record (
    record_id SERIAL PRIMARY KEY,
    patient_id INT REFERENCES Patient(patient_id) ON DELETE CASCADE,
    stored_filename VARCHAR(255) NOT NULL,
    provided_filename VARCHAR(255) NOT NULL,
    date DATE,
    file_line TEXT
);

-- Appointment Table
CREATE TABLE Appointment (
    appointment_id SERIAL PRIMARY KEY,
    patient_id INT REFERENCES Patient(patient_id) ON DELETE CASCADE,
    doctor_id INT REFERENCES Doctor(doctor_id) ON DELETE CASCADE,
    scheduled_date_time TIMESTAMP,
    status VARCHAR(50) DEFAULT, 'scheduled', -- Values like 'scheduled', 'canceled', 'completed'
    cancel_reason TEXT
);

--Doctor's Work Hours Table
CREATE TABLE Doctor_work_hours(
    availability_id SERIAL PRIMARY KEY,
    doctor_id INT REFERENCES Doctor(doctor_id) ON DELETE CASCADE,
    day_of_week VARCHAR(27) NOT NULL, -- Values like 'Mon', 'Tue', 'Wed', etc.
    start_work_hour TIMESTAMP,
    end_work_hour TIMESTAMP
);

CREATE TABLE health_metrics (
    metric_id SERIAL PRIMARY KEY,
    patient_id INT,
	weight INT,
	height INT,
	blood_pressure VARCHAR(10),
	heart_rate INT, 
    measurement_date TIMESTAMP,
    FOREIGN KEY (patient_id) REFERENCES patient(patient_id) ON DELETE CASCADE
);
-- Add the foreign key for primary_care_doctor_id in patient table
ALTER TABLE Patient
ADD FOREIGN KEY (primary_care_doctor_id) REFERENCES Doctor(doctor_id) ON DELETE SET NULL;