from flask import Flask, jsonify, request
from dotenv import load_dotenv
import psycopg2
import os
from flask_bcrypt import Bcrypt
from flask_cors import CORS, cross_origin
from datetime import datetime
from werkzeug.utils import secure_filename
from collections import defaultdict
import random

# Where we store our handler functions
from file_handler import FileHandler
from appointment_handler import AppointmentHandler

# Load environment variables
load_dotenv()

# Flask app
app = Flask(__name__)
bcrypt = Bcrypt(app)

cors = CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}}) 
app.config['CORS_HEADERS'] = 'Content-Type'

# The PostgreSQL instance
conn = psycopg2.connect(
    host = os.environ.get("ENDPOINT"),
    port = os.environ.get("PORT"),
    user = os.environ.get("MASTER_USERNAME"),
    password = os.environ.get("MASTER_PASSWORD"),
    dbname = os.environ.get("DATABASE_NAME")
)

@app.route('/')
def index():
    return "Welcome"

# Registers a user into the database
@app.route('/register', methods = ["POST", "GET"])
@cross_origin(origin='*',headers=['Content-Type','Authorization'])
def register():
    try:
        cur = conn.cursor()

        # Retrieves the email from the frontend request
        email = request.json['email']

        # Fetches all users with the provided email, if one doesn't exist then we create a new user.
        # Otherwise, we return an error since we can't register an existing email.
        cur.execute("SELECT * FROM system_user WHERE email = %s", (email, ))
        exists = cur.fetchone()
        if exists:
            return jsonify({"Result": "Error", "Error": "Email is already registered"})
        else:
            # Password encryption
            password = bcrypt.generate_password_hash(request.json['password'], 10).decode("utf-8")

            # Gets the necessary info from the frontend
            first_name = request.json['first_name']
            last_name = request.json['last_name']
            role = request.json['role']

            # Creates a new user in the system_user table
            cur.execute("INSERT INTO system_user (email, password_hash, first_name, last_name, role) \
                        VALUES (%s, %s, %s, %s, %s)", (email, password, first_name, last_name, role))
            conn.commit()

            # Grabs the user id of the newly registered user
            cur.execute("SELECT * FROM system_user WHERE email = %s", (email, ))
            get_cur_id = cur.fetchone()[0]

            # We have different cases for when a user is a doctor or a patient
            # If a user is a patient, we retrieve their birthday, sex, and
            # randomly assign them a primary care doctor, and insert them into the patients table
            #
            # If a user is a doctor, we insert them into the doctors table
            if role == "patient":
                birthday = request.json['birthday']
                sex = request.json['sex']

                cur.execute("SELECT DISTINCT doctor_id FROM doctor;")
                doctor_id_list = cur.fetchall()

                if not doctor_id_list:
                    primary_care_doctor_id = None
                else:
                    primary_care_doctor_id = doctor_id_list[random.randint(0, len(doctor_id_list)-1)]
            

                #Insert into patients table
                cur.execute("INSERT INTO patient (user_id, date_of_birth, sex, primary_care_doctor_id) \
                            VALUES (%s, %s, %s, %s)", (get_cur_id, birthday, sex, primary_care_doctor_id))
            else:
                cur.execute("INSERT INTO doctor (user_id) VALUES (%s)", (get_cur_id, ))
            
            conn.commit()
            return jsonify({"Result": "Success"})
    except ValueError as e:
        print(e)
        
# Checks the user's credentials and attempts to have them logged in
@app.route('/login', methods = ["POST", "GET"])
@cross_origin(origin='*',headers=['Content-Type','Authorization'])
def login():
    try:
        cur = conn.cursor()

        # Retrieves the email and password from the frontend request
        email = request.json.get('email')
        password = request.json.get('password')

        cur.execute("SELECT user_id, role, password_hash FROM System_user WHERE email = %s", (email, ))
        entry = cur.fetchone()

        # If the email doesn't exist in our database then we return an error
        if not entry:
            return jsonify({"Result": "Error", "Error": "Email is not registered"})

        # Checks that the hash of the inputted password matches that from the database
        if bcrypt.check_password_hash(entry[2], password):
            # If the user is a doctor, we fetch their doctor id. Otherwise, we fetch their patient id.
            # We then return it to the frontend
            if entry[1] == "doctor":
                cur.execute("SELECT doctor_id FROM doctor WHERE user_id = %s", (entry[0], ))
                doctor_id = cur.fetchone()
                return {"Result": "Success", "User_ID": entry[0], "Role": entry[1], "Role_ID": doctor_id[0]}
            else:
                cur.execute("SELECT patient_id FROM patient WHERE user_id = %s", (entry[0], ))
                patient_id = cur.fetchone()
                return {"Result": "Success", "User_ID": entry[0], "Role": entry[1], "Role_ID": patient_id[0]}
                
        else:
            return jsonify({"Result": "Error", "Error": "Invalid Password!"})
    except ValueError as e:
        print(e)

# Handles file/medical record uploading from a patient
@app.route('/upload_file', methods = ["POST", "GET"])
@cross_origin(origin='*',headers=['Content-Type','Authorization'])
def upload_file():
    try:
        # Creates a new FileHandler object
        file_handler = FileHandler()
        cur = conn.cursor()

        # Retrieves the file from the frontend request
        file = request.files['record']

        filename = file.filename

        # If the file exists and the file type is valid (pdf, txt, png), we proceed
        # Otherwise, we return an error to the frontend
        if file and file_handler.allowed_file(filename):
            patient_id = request.form.get('patient_id')
            
            # provided_filename is the name of the original file
            # stored_filename is the name we store on the S3 bucket to avoiud collision.
            # We added secure_filename for the filename so that the name wouldn't pose a security risk
            provided_filename = secure_filename(filename)
            stored_filename = file_handler.upload_file_to_s3(file, provided_filename)

            # If the stored_filename was successfully returned, we proceed
            # Otherwise, we return an error
            if stored_filename:
                date = datetime.now()
                
                # Inserts the file into the database with both file names
                query = """ 
                        INSERT INTO medical_record (provided_filename, stored_filename, patient_id, date) \
                        VALUES (%s, %s, %s, %s)
                    """
                
                cur.execute(query, (provided_filename, stored_filename, patient_id, date, ))
                conn.commit()
                return jsonify({"Result": "Success"})
            return jsonify({"Result": "Error", "Message": "File not stored successfully"})
    except ValueError as e:
        print(e)
        return jsonify({"Result": "Error"})

# Retrieves the medical record URLs corresponding to a specific patient

@app.route('/get_file_urls', methods = ["POST", "GET"])
@cross_origin(origin='*',headers=['Content-Type','Authorization'])
def get_file_urls():
    try:
        file_handler = FileHandler()
        cur = conn.cursor()

        # Retrieves the patient id from the frontend
        patient_id = request.json.get('patient_id')
        
        query = """
                SELECT provided_filename, stored_filename
                FROM medical_record
                WHERE patient_id = %s
            """
        cur.execute(query, (patient_id, ))

        # Grabs all of the file names from the table
        file_list = cur.fetchall()

        # The resulting dictionary of URLS, where the key corresponds to the file name and the
        # value corresponds to the URL
        result = defaultdict(str)
        for file in file_list:
            provided = file[0]
            stored = file[1]

            # Since the S3 bucket only returns temporary URLs, we cannot store them in the database
            # Instead, we call this function which retrieves a temporary presigned URL by providing
            # the file name we want to retrieve
            url = file_handler.get_presigned_file_url(stored, provided)

            # Assigns the provided file name to the URL
            result[provided] = url
        return jsonify(result)

    except ValueError as e:
        print(e)
        return jsonify({"Result": "Error"})


# Retrieves all data of patient
@app.route('/get_patient_data', methods=["POST", "GET"])
@cross_origin(origin='*', headers=['Content-Type', 'Authorization'])
def get_patient_data():
    try:
        cur = conn.cursor()

        # Retrieves aser id from frontend
        user_id = request.json.get('user_id')
        get_user_info_query = """
                SELECT u.first_name, u.last_name, p.patient_id, p.date_of_birth, p.primary_care_doctor_id
                FROM patient p
                JOIN system_user u
                ON p.user_id = u.user_id
                WHERE u.user_id = %s;
            """
        # Retrieves all info of patients
        cur.execute(get_user_info_query, (user_id,))
        patient_data = cur.fetchone()

        # Retrieves latest health metrics of patients
        patient_id = patient_data[2]
        get_patient_health_metrics = """
                SELECT
                    (SELECT weight FROM health_metrics WHERE patient_id = %s AND weight IS NOT NULL ORDER BY measurement_date DESC LIMIT 1) AS latest_weight,
                    (SELECT height FROM health_metrics WHERE patient_id = %s AND height IS NOT NULL ORDER BY measurement_date DESC LIMIT 1) AS latest_height,
                    (SELECT blood_pressure FROM health_metrics WHERE patient_id = %s AND blood_pressure IS NOT NULL ORDER BY measurement_date DESC LIMIT 1) AS latest_blood_pressure,
                    (SELECT heart_rate FROM health_metrics WHERE patient_id = %s AND heart_rate IS NOT NULL ORDER BY measurement_date DESC LIMIT 1) AS latest_heart_rate
                FROM health_metrics
                WHERE patient_id = %s
                ORDER BY measurement_date DESC
                LIMIT 1;
            """
        cur.execute(get_patient_health_metrics, (patient_id, patient_id, patient_id, patient_id, patient_id,))
        patient_health_metrics = cur.fetchone()

        #No recorded patient's health metrics
        if patient_health_metrics is None:
            patient_health_metrics = [None, None, None, None]

        # Retrieves full name of patient's primary care doctor
        doctor_id = patient_data[4]
        doctor_first_name = None
        doctor_last_name = None
        if doctor_id is not None:
            get_doctor_name_query = """
                    SELECT u.first_name, u.last_name
                    FROM doctor d
                    JOIN system_user u
                    ON d.user_id = u.user_id
                    WHERE u.user_id = (
                        SELECT user_id
                        FROM doctor
                        WHERE doctor_id = %s
                    );
                """
            cur.execute(get_doctor_name_query, (doctor_id,))
            doctor_name = cur.fetchone()
            doctor_first_name = doctor_name[0]
            doctor_last_name = doctor_name[1]
            
        #Return all the data of patients
        if patient_data:
            return jsonify({
                "Result": "Success",
                "Data": {
                    "first_name": patient_data[0],
                    "last_name": patient_data[1],
                    "date_of_birth": patient_data[3].strftime('%Y-%m-%d'),
                    "primary_care_doctor_first_name": doctor_first_name,
                    "primary_care_doctor_last_name": doctor_last_name,
                    "docId": doctor_id,
                    "weight": patient_health_metrics[0],
                    "height": patient_health_metrics[1],
                    "blood_pressure": patient_health_metrics[2],
                    "heart_rate": patient_health_metrics[3]
                }
            })
        else:
            return jsonify({"Result": "Error", "Error": "User not found"})
    except Exception as e:
        print(e)
        return jsonify({"Result": "Error", "Error": "An error occurred"})
 
@app.route('/get_patients_by_doctor_id', methods=["POST", "GET"])
@cross_origin(origin='*', headers=['Content-Type', 'Authorization'])
def get_patients_by_doctor_id():
    try:
        cur = conn.cursor()
        
        # Retrieves user id of doctor from frontend
        user_id = request.json.get('user_id')
    
        # Retrieves list of patients' name and id under doctor
        query = """
                SELECT u.first_name, u.last_name, u.user_id, p.patient_id
                FROM patient p
                JOIN system_user u
                ON p.user_id = u.user_id
                WHERE p.primary_care_doctor_id = (
                    SELECT doctor_id
                    FROM doctor
                    WHERE user_id = %s
                );
            """
        cur.execute(query, (user_id,))
        patient_data = cur.fetchall()
        return jsonify({
            "Result": "Success",
            "Data": patient_data
        })
    except Exception as e:
        print(e)


# Given a specific date, returns all the available appointment times of that date 
# and 3 other days before and after that date
@app.route('/get_appointment_times', methods = ["POST", "GET"])
@cross_origin(origin='*',headers=['Content-Type','Authorization'])
def get_appointment_times():
    try:
        cur = conn.cursor()
        date = request.json.get("date")
        doctor_id = request.json.get("doctor_id")
        appointment_handler = AppointmentHandler()

        # All available hours of a doctor during a week
        available_week_times = appointment_handler.available_times_in_week(doctor_id)
        
        # The 7 days and corresponding weekdays based on the user inputted date
        date_list, weekday_list = appointment_handler.get_seven_days(date)

        # The hash map containing all available times for a specific day
        all_available_times = defaultdict(list)
        

        # Loops through all 7 provided days and their weekdays
        for day, weekday in zip(date_list, weekday_list):
            # Only returns appointments from or after today's date, and if the weekday is within the doctor's available days
            current_datetime = datetime.strptime(day, '%Y-%m-%d')
            day_difference = (datetime.now() - current_datetime).days
            if day_difference > 0 or weekday not in available_week_times: continue

            # Finds all the scheduled appointments related to a specific doctor and on a specific weekday
            query = """
                    SELECT start_time, end_time
                    FROM appointment
                    WHERE doctor_id = %s AND date(start_time) = %s AND status = %s
                """
            cur.execute(query, (doctor_id, day, "Scheduled", ))
            day_appointments = cur.fetchall()
            # List of times in which the doctor is unavailable
            unavailable_timeframes = []

            # Retrieves the times in which a doctor has an appointment
            for appointment in day_appointments:
                # Since the times are formated in year/month/day hour:minute:second, we'd have to split
                # the string accordingly. The 1st index of the split is what we want, hour:minute:second
                start = appointment[0].strftime("%Y-%m-%d %H:%M:%S").split(" ")[1]
                end = appointment[1].strftime("%Y-%m-%d %H:%M:%S").split(" ")[1]

                timeframe = start + "-" + end
                unavailable_timeframes.append(timeframe)

            #Retrieves times within the available times that are not in the unavailable timeframes
            all_available_times[day] = sorted(list(set(available_week_times[weekday]) - set(unavailable_timeframes)))
        return jsonify({"Result": "Success", "Times": all_available_times})
    except Exception as e:
        print(e)
        return jsonify({"Result": "Error"})

# Creates a new appointment
@app.route('/make_appointment', methods = ["POST", "GET"])
@cross_origin(origin='*',headers=['Content-Type','Authorization'])
def make_appointment():
    try:
        cur = conn.cursor()

        # All the necessary info is retrieved from the frontend
        patient_id = request.json.get("patient_id")
        doctor_id = request.json.get("doctor_id")
        start_time = request.json.get("start_time")
        end_time = request.json.get("end_time")

        # Inserts the new appointment into the database
        query = """
            INSERT INTO appointment (patient_id, doctor_id, status, start_time, end_time)
            VALUES (%s, %s, %s, %s, %s)
        """ 
        cur.execute(query, (patient_id, doctor_id, "Scheduled", start_time, end_time))
        conn.commit()
        return jsonify({"Result": "Success"})
    except Exception as e:
        print(e)
        return jsonify({"Result": "Error"})

# Updates an appointment's status to canceled or completed 
@app.route('/update_appointment', methods = ["POST", "GET"])
@cross_origin(origin='*',headers=['Content-Type','Authorization'])
def update_appointment():
    try:
        cur = conn.cursor()

        # Retrieves the necessary information from the frontend
        appointment_id = request.get_json("appointment_id")
        new_status = request.get_json("new_status")
        cancel_reason = request.get_json("cancel_reason")

        # Updates the corresponding appointment in the database with new info
        query = """
            UPDATE appointment
            SET status = %s, cancel_reason = %s,
            WHERE appointment_id = %s
        """
        cur.execute(query, (new_status, cancel_reason, appointment_id,  ))
        conn.commit()
            
        return jsonify({"Result": "Success"})

    except Exception as e:
        print(e)
        return jsonify({"Result": "Error"})


#Route for deleting an appointment
@app.route('/delete_appointment', methods = ["POST", "GET"])
@cross_origin(origin='*',headers=['Content-Type','Authorization'])
def delete_appointment():
    try:
        cur = conn.cursor()

        # Retrieves the appointment id from the frontend
        appointment_id = request.get_json("appointment_id")
        
        # Deletes the appointment from the database based on id
        query = """
            DELETE FROM appointment
            WHERE appointment_id = %s
        """
        cur.execute(query, (appointment_id, ))
        conn.commit()
        return jsonify({"Result": "Success"})

    except Exception as e:
        print(e)
        return jsonify({"Result": "Error"})

# Retrieves the list of appointments for a specific patient
@app.route('/get_appointments_by_patient_id', methods = ["POST", "GET"])
@cross_origin(origin='*',headers=['Content-Type','Authorization'])
def get_appointments_by_patient_id():
    try:
        cur = conn.cursor()

        # Retrieves patient id from frontend
        patient_id = request.json.get("patient_id")
        query = """
            SELECT * FROM appointment
            WHERE patient_id = %s
        """
        cur.execute(query, (patient_id, ))

        # Returns the list of appointments for a specific patient
        appointments = cur.fetchall()
        return jsonify({"Result": "Success", "Appointments": appointments})

    except Exception as e:
        print(e)
        return jsonify({"Result": "Error"})

# Retrieves the list of appointments for a specific doctor
@app.route('/get_appointments_by_doctor_id', methods = ["POST", "GET"])
@cross_origin(origin='*',headers=['Content-Type','Authorization'])
def get_appointments_by_doctor_id():
    try:
        cur = conn.cursor()

        # Retrieves the doctor id from the frontend
        doctor_id = request.json.get("doctor_id")
        query = """
            SELECT * FROM appointment
            WHERE doctor_id = %s
        """
        cur.execute(query, (doctor_id, ))

        # Grabs all the appointments for that doctor from the database
        appointments = cur.fetchall()

        # The resulting list of appointments
        result = []

        for appointment in appointments:
            # Grabs the corresponding patient for the appointment
            patient_id = appointment[1]
            query = """
                SELECT user_id FROM patient
                WHERE patient_id = %s
            """
            cur.execute(query, (patient_id, ))
            user_id = cur.fetchone()[0]

            # Grabs the patient's full name
            query = """
                SELECT first_name, last_name FROM System_user
                WHERE user_id = %s
            """
            cur.execute(query, (user_id, ))
            entry = cur.fetchone()

            # Formats the returned appointment by including the appointment information and the patient's full name
            first_name = entry[0]
            last_name = entry[1]
            appointment_info = []
            appointment_info.extend(appointment[:6])
            appointment_info.extend([first_name, last_name])
            appointment_info.extend(appointment[6:])
            result.append(appointment_info)
        return jsonify({"Result": "Success", "Appointments": result})

    except ValueError as e:
        print(e)
        return jsonify({"Result": "Error"})

#insert new health metrics
@app.route('/insert_health_metrics', methods = ["POST", "GET"])
@cross_origin(origin='*',headers=['Content-Type','Authorization'])
def insert_health_metrics():
    try:
        cur = conn.cursor()

        # Retrieves the health metrics from the frontend
        patient_id = request.get_json("patient_id")
        height = request.get_json("height")
        weight = request.get_json("weight")
        blood_pressure = request.get_json("blood_pressure")
        heart_rate = request.get_json("heart_rate")

        # Inserted measured health metrics to database
        query = """
            INSERT INTO health_metrics (patient_id, weight, height, blood_pressure, heart_rate, measurement_date)
            VALUES( %s, %s, %s, %s, %s, current_timestamp)
        """
        cur.execute(query, (patient_id, weight, height, blood_pressure, heart_rate, ))
        conn.commit()
        return jsonify({"Result": "Success"})

    except Exception as e:
        print(e)
        return jsonify({"Result": "Error"})

if __name__ == "__main__":
    app.run(debug = True)