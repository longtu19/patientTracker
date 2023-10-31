from flask import Flask
from dotenv import load_dotenv
import psycopg2
import os
from flask_bcrypt import Bcrypt
from requests import *

load_dotenv()
app = Flask(__name__)
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

@app.route('/register', methods = ["POST"])
def register():
    try:
        cur = conn.cursor()
        email = request.form['email']
        cur.execute("SELECT * FROM System_user WHERE email = %s", (email, ))
        exists = cur.fetchone()
        if exists:
            return {"Result": "Error", "Error": "Email is already registered"}
        else:
            password = Bcrypt.generate_password_hash(request.form['password'])
            first_name = request.form['first_name']
            last_name = request.form['last_name']
            is_patient = request.form['status'] == "patient"
            if is_patient:
                birthday = request.form['birthday']
                sex = request.form['sex']
                cur.execute("INSERT INTO System_user (email, password, first_name, last_name, birthday, sex) \
                VALUES (%s, %s, %s, %s, %s, %s)", (email, password, first_name, last_name, birthday, sex))
            else:
                cur.execute("INSERT INTO System_user (email, password, first_name, last_name) \
                VALUES (%s, %s, %s, %s)", (email, password, first_name, last_name))
            conn.commit()
            return {"Result": "Success"}
    except ValueError as e:
        print(e)
        
@app.route('/login')
def login():
    try:
        cur = conn.cursor()
        email = request.form['email']
        password = request.form['password']
        cur.execute("SELECT * FROM System_user WHERE email = %s", (email))
        entry = cur.fetchone()
        if not entry:
            return {"Result": "Error", "Error": "Email is not registered"}

        if Bcrypt.check_password_hash(entry['password'], password):
            conn.commit()
            return {"Result": "Success"}
        else:
            return {"Result": "Error", "Error": "Invalid Password!"}
    except ValueError as e:
        print(e)

if __name__ == "__main__":
    app.run(debug = True)