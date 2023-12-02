from flask import Flask, jsonify, request
from dotenv import load_dotenv
import psycopg2
import os
from flask_bcrypt import Bcrypt
from flask_cors import CORS, cross_origin
import json
import datetime
import boto3

load_dotenv()
app = Flask(__name__)
bcrypt = Bcrypt(app)
cors = CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}}) 
app.config['CORS_HEADERS'] = 'Content-Type'

app.config['S3_BUCKET'] = os.environ.get("BUCKET_NAME")
app.config['S3_KEY'] = os.environ.get("ACCESS_KEY")
app.config['S3_SECRET'] = os.environ.get("SECRET_ACCESS_KEY")
app.config['S3_REGION'] = os.environ.get("BUCKET_REGION")

s3 = boto3.client(
    "s3",
    aws_access_key_id = app.config['S3_KEY'],
    aws_secret_access_key = app.config['S3_SECRET']
)

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png'}
def allowed_file(filename):
    return '.' in filename and filename.split('.')[1].lower() in ALLOWED_EXTENSIONS

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

# object = {"email": "abc@gmail.com", "password": '123456', "first_name": "Bob", "last_name": "Americanman", "status": "patient", \
#      "birthday": "12/24/2002", "sex": "Male"}

@app.route('/register', methods = ["POST", "GET"])
@cross_origin(origin='*',headers=['Content-Type','Authorization'])
def register():
    try:
        cur = conn.cursor()
        email = request.json['email']
        print("PATRICCCCC")
        print(email)
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

                #Insert into patients table
                cur.execute("INSERT INTO patient (user_id, date_of_birth, sex) \
                VALUES (%s, %s, %s)", (get_cur_id, birthday, sex))
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
            return {"Result": "Success", "User_ID": entry[0], "Role": entry[1]}
        else:
            return jsonify({"Result": "Error", "Error": "Invalid Password!"})
    except ValueError as e:
        print(e)


@app.route('/upload_file', methods = ["POST", "GET"])
@cross_origin(origin='*',headers=['Content-Type','Authorization'])
def upload_file():
    try:
        # cur = conn.cursor()
        # file = request.files['record']
        # filename = file.filename
        file = "/Users/phucnguyen02/Documents/Fall_2023/CS520/patientTracker/server/test.txt"
        filename = "test.txt"
        if allowed_file(filename):
            # original_filename = request.json.get('original_filename')
            # date = datetime.datetime.now()
            # patient_id = request.json.get('patient_id')

            s3.upload_file(
                file, 
                os.getenv("BUCKET_NAME"), 
                filename
            )
            return jsonify({"Result": "Success"})
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
        query = """
                SELECT u.first_name, u.last_name, p.height, p.weight, p.date_of_birth
                FROM patient p
                JOIN system_user u
                ON p.user_id = u.user_id
                WHERE u.user_id = %s;
            """
        cur.execute(query, (user_id,))
        patient_data = cur.fetchone()
        if patient_data:
            return jsonify({
                "Result": "Success",
                "Data": {
                    "first_name": patient_data[0],
                    "last_name": patient_data[1],
                    "height": patient_data[2],
                    "weight": patient_data[3],
                    "date_of_birth": patient_data[4].strftime('%Y-%m-%d')
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
        doctor_id = request.json.get('user_id')
        cur = conn.cursor()

        query = """
                SELECT u.first_name, u.last_name, u.user_id
                FROM patient p
                JOIN system_user u
                ON p.user_id = u.user_id
                WHERE p.primary_care_doctor_id = %s;
            """
        cur.execute(query, (doctor_id,))
        patient_data = cur.fetchone()
        return jsonify({
            "Result": "Success",
            "Data": patient_data
        })
    except Exception as e:
        print(e)

if __name__ == "__main__":
    app.run(debug = True)