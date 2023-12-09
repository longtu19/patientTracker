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

from file_handler import FileHandler
from appointment_handler import AppointmentHandler

load_dotenv()
app = Flask(__name__)
bcrypt = Bcrypt(app)
cors = CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}}) 
app.config['CORS_HEADERS'] = 'Content-Type'

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

@app.route('/register', methods = ["POST", "GET"])
@cross_origin(origin='*',headers=['Content-Type','Authorization'])
def register():
    try:
        cur = conn.cursor()
        email = request.json['email']
        cur.execute("SELECT * FROM system_user WHERE email = %s", (email, ))
        exists = cur.fetchone()
        if exists:
            return jsonify({"Result": "Error", "Error": "Email is already registered"})
        else:
            password = bcrypt.generate_password_hash(request.json['password'], 10).decode("utf-8")
            first_name = request.json['first_name']
            last_name = request.json['last_name']
            role = request.json['role']
            cur.execute("INSERT INTO system_user (email, password_hash, first_name, last_name, role) \
               VALUES (%s, %s, %s, %s, %s)", (email, password, first_name, last_name, role))
            conn.commit()
            cur.execute("SELECT * FROM system_user WHERE email = %s", (email, ))
            get_cur_id = cur.fetchone()[0]

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
        

@app.route('/login', methods = ["POST", "GET"])
@cross_origin(origin='*',headers=['Content-Type','Authorization'])
def login():
    try:
        cur = conn.cursor()
        email = request.json.get('email')
        password = request.json.get('password')
        cur.execute("SELECT user_id, role, password_hash FROM System_user WHERE email = %s", (email, ))
        entry = cur.fetchone()
        if not entry:
            return jsonify({"Result": "Error", "Error": "Email is not registered"})
        if bcrypt.check_password_hash(entry[2], password):
            if entry[1] == "doctor":
                cur.execute("SELECT doctor_id FROM doctor WHERE user_id = %s", (entry[0], ))
                doctor_id = cur.fetchone()
                return {"Result": "Success", "User_ID": entry[0], "Role": entry[1], "Role_ID": doctor_id[0]}
            else:
                print(entry[0])
                cur.execute("SELECT patient_id FROM patient WHERE user_id = %s", (entry[0], ))
                patient_id = cur.fetchone()
                return {"Result": "Success", "User_ID": entry[0], "Role": entry[1], "Role_ID": patient_id[0]}
                
        else:
            return jsonify({"Result": "Error", "Error": "Invalid Password!"})
    except ValueError as e:
        print(e)

@app.route('/upload_file', methods = ["POST", "GET"])
@cross_origin(origin='*',headers=['Content-Type','Authorization'])
def upload_file():
    try:
        file_handler = FileHandler()
        cur = conn.cursor()
        print("DAYYYY")
        print(request.files)
        file = request.files['record']
        print("Hi from app")
        filename = file.filename
        # file = os.environ.get("TEST_FILE")
        # filename = "test.txt"
        if filename and file_handler.allowed_file(filename):
            patient_id = request.form.get("patient_id")
            print(patient_id)
            #patient_id = 12
            provided_filename = secure_filename(file.filename)
            stored_filename = file_handler.upload_file_to_s3(file, provided_filename)
            if stored_filename:
                date = datetime.now()
                
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


@app.route('/get_file_urls', methods = ["POST", "GET"])
@cross_origin(origin='*',headers=['Content-Type','Authorization'])
def get_file_urls():
    try:
        file_handler = FileHandler()
        cur = conn.cursor()
        patient_id = request.json.get('patient_id')
        
        query = """
                SELECT provided_filename, stored_filename
                FROM medical_record
                WHERE patient_id = %s
            """
        cur.execute(query, (patient_id, ))
        file_list = cur.fetchall()
        result = defaultdict(str)
        for file in file_list:
            provided = file[0]
            stored = file[1]
            url = file_handler.get_presigned_file_url(stored, provided)
            print(url)
            result[provided] = url
        return jsonify(result)

    except ValueError as e:
        print(e)
        return jsonify({"Result": "Error"})


#
@app.route('/get_patient_data', methods=["POST", "GET"])
@cross_origin(origin='*', headers=['Content-Type', 'Authorization'])
def get_patient_data():
    try:
        user_id = request.json.get('user_id')
        cur = conn.cursor()
        get_user_info_query = """
                SELECT u.first_name, u.last_name, p.height, p.weight, p.date_of_birth, p.primary_care_doctor_id
                FROM patient p
                JOIN system_user u
                ON p.user_id = u.user_id
                WHERE u.user_id = %s;
            """
        cur.execute(get_user_info_query, (user_id,))
        patient_data = cur.fetchone()

        doctor_id = patient_data[5]
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
            
        if patient_data:
            return jsonify({
                "Result": "Success",
                "Data": {
                    "first_name": patient_data[0],
                    "last_name": patient_data[1],
                    "height": patient_data[2],
                    "weight": patient_data[3],
                    "date_of_birth": patient_data[4].strftime('%Y-%m-%d'),
                    "primary_care_doctor_first_name": doctor_first_name,
                    "primary_care_doctoc_last_name": doctor_last_name
                }
            })
        else:
            return jsonify({"Result": "Error", "Error": "User not found"})
    except Exception as e:
        print(e)
        return jsonify({"Result": "Error", "Error": "An error occurred"})
 
#
@app.route('/get_patients_by_doctor_id', methods=["POST", "GET"])
@cross_origin(origin='*', headers=['Content-Type', 'Authorization'])
def get_patients_by_doctor_id():
    try:
        user_id = request.json.get('user_id')
        cur = conn.cursor()

        query = """
                SELECT u.first_name, u.last_name, u.user_id
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


@app.route('/get_appointment_times', methods = ["POST", "GET"])
@cross_origin(origin='*',headers=['Content-Type','Authorization'])
def get_appointment_times():
    try:
        cur = conn.cursor()
        #date = request.get_json("date")
        date = '2023-12-11'
        #doctor_id = request.get_json("doctor_id")
        doctor_id = 13
        appointment_handler = AppointmentHandler()
        available_week_times = appointment_handler.available_times_in_week(doctor_id)
        date_list, weekday_list = appointment_handler.get_seven_days(date)
        
        all_available_times = defaultdict(list)
        for day, weekday in zip(date_list, weekday_list):
            #Only returns appointments from or after today's date, and if the weekday is within the doctor's available days
            if datetime.strptime(day, '%Y-%m-%d') < datetime.now() or weekday not in available_week_times: continue
            query = """
                    SELECT start_time, end_time
                    FROM appointment
                    WHERE doctor_id = %s AND date(start_time) = %s AND status = %s
                """
            cur.execute(query, (doctor_id, day, "Scheduled", ))
            day_appointments = cur.fetchall()
            # day_appointments = [["2023-12-09 8:00:00", "2023-12-09 9:00:00"], ["2023-12-09 11:00:00", "2023-12-09 12:00:00"]]
            unavailable_timeframes = []
            for appointment in day_appointments:
                start = appointment[0].split(" ")[1]
                end = appointment[1].split(" ")[1]
                timeframe = start + "-" + end
                unavailable_timeframes.append(timeframe)
            
            #Retrieves times within the available times that are not in the unavailable timeframes
            all_available_times[day] = list(set(available_week_times[weekday]) - set(unavailable_timeframes))

        return jsonify({"Result": "Success", "Times": all_available_times})
    except Exception as e:
        print(e)
        return jsonify({"Result": "Error"})

@app.route('/make_appointment', methods = ["POST", "GET"])
@cross_origin(origin='*',headers=['Content-Type','Authorization'])
def make_appointment():
    try:
        cur = conn.cursor()
        patient_id = request.get_json("patient_id")
        doctor_id = request.get_json("doctor_id")
        start_time = request.get_json("start_time")
        end_time = request.get_json("end_time")
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


@app.route('/update_appointment', methods = ["POST", "GET"])
@cross_origin(origin='*',headers=['Content-Type','Authorization'])
def update_appointment():
    try:
        cur = conn.cursor()
        appointment_id = request.get_json("appointment_id")
        new_status = request.get_json("new_status")
        cancel_reason = request.get_json("cancel_reason")
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

@app.route('/delete_appointment', methods = ["POST", "GET"])
@cross_origin(origin='*',headers=['Content-Type','Authorization'])
def delete_appointment():
    try:
        cur = conn.cursor()
        appointment_id = request.get_json("appointment_id")
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

if __name__ == "__main__":
    app.run(debug = True)