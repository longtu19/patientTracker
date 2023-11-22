from flask import Flask, jsonify, request
from dotenv import load_dotenv
import psycopg2
import os
from flask_bcrypt import Bcrypt
from flask_cors import CORS, cross_origin
import json

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


# object = {"email": "abc@gmail.com", "password": '123456', "first_name": "Bob", "last_name": "Americanman", "status": "patient", \
#      "birthday": "12/24/2002", "sex": "Male"}

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
        cur.execute("SELECT * FROM System_user WHERE email = %s", (email, ))
        entry = cur.fetchone()
        if not entry:
            return jsonify({"Result": "Error", "Error": "Email is not registered"})
        if bcrypt.check_password_hash(entry[2], password):
            return {"Result": "Success", "User_ID": entry[0]}
        else:
            return jsonify({"Result": "Error", "Error": "Invalid Password!"})
    except ValueError as e:
        print(e)

#
@app.route('/get_patient_data', methods=["GET"])
@cross_origin(origin='*', headers=['Content-Type', 'Authorization'])
def get_patient_data():
    try:
        user_id = request.args.get('user_id')

        cur = conn.cursor()
        query = """
                SELECT u.first_name, u.last_name, p.height, p.weight, p.date_of_birth
                FROM patient u
                JOIN patient p ON u.id = p.user_id
                WHERE u.id = %s
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
                    "date_of_birth": patient_data[4],
                }
            })
        else:
            return jsonify({"Result": "Error", "Error": "User not found"})
    except Exception as e:
        print(e)
        return jsonify({"Result": "Error", "Error": "An error occurred"})
    
if __name__ == "__main__":
    app.run(debug = True)