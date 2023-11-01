from flask import Flask, jsonify
from dotenv import load_dotenv
import psycopg2
import os
from flask_bcrypt import Bcrypt
from flask_cors import CORS

from requests import *

load_dotenv()
app = Flask(__name__)
bcrypt = Bcrypt(app)
cors = CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})  # Replace with your frontend's URL

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


# object = {"email": "abc@gmail.com", "password": "123456", "first_name": "Bob", "last_name": "Americanman", "status": "patient", \
#     "birthday": "12/24/2002", "sex": "Male"}

@app.route('/register', methods = ["POST", "GET"])
def register():
    try:
        cur = conn.cursor()
        email = request.form['email']
        cur.execute("SELECT * FROM system_user WHERE email = %s", (email, ))
        exists = cur.fetchone()
        if exists:
            return jsonify({"Result": "Error", "Error": "Email is already registered"})
        else:
            password = bcrypt.generate_password_hash(request.form['password'])
            first_name = request.form['first_name']
            last_name = request.form['last_name']
            role = request.form['role']
            cur.execute("INSERT INTO system_user (email, password_hash, first_name, last_name, role) \
               VALUES (%s, %s, %s, %s, %s)", (email, password, first_name, last_name, role))
            conn.commit()

            cur.execute("SELECT * FROM system_user WHERE email = %s", (email, ))
            get_cur_id = cur.fetchone()[0]

            if role == "patient":
                birthday = request.form['birthday']
                sex = request.form['sex']

                #Insert into patients table
                cur.execute("INSERT INTO patient (user_id, date_of_birth, sex) \
                VALUES (%s, %s, %s)", (get_cur_id, birthday, sex))
            else:
                cur.execute("INSERT INTO doctor (user_id) VALUES (%s)", (get_cur_id))
            
            conn.commit()
            return jsonify({"Result": "Success"})
    except ValueError as e:
        print(e)
        
@app.route('/login', methods = ["POST", "GET"])
def login():
    try:
        cur = conn.cursor()
        email = request.form['email']
        password = request.form['password']
        cur.execute("SELECT * FROM System_user WHERE email = %s", (email))
        entry = cur.fetchone()
        if not entry:
            return jsonify({"Result": "Error", "Error": "Email is not registered"})

        if bcrypt.check_password_hash(entry[2], password):
            return jsonify({"Result": "Success"})
        else:
            return jsonify({"Result": "Error", "Error": "Invalid Password!"})
    except ValueError as e:
        print(e)

if __name__ == "__main__":
    app.run(debug = True)