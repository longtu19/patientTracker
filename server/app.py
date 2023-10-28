from flask import Flask
from dotenv import load_dotenv
import psycopg2
import os

load_dotenv()
app = Flask(__name__)
conn = psycopg2.connect(
    host = os.environ.get("ENDPOINT"),
    port = os.environ.get("PORT"),
    user = os.environ.get("MASTER_USERNAME"),
    password = os.environ.get("MASTER_PASSWORD"),
    dbname = os.environ.get("DATABASE_NAME")
)

cur = conn.cursor()
cur.execute(" CREATE TABLE IF NOT EXISTS person (id INT PRIMARY KEY,name VARCHAR(255), age INT);")
conn.commit()

@app.route('/')
def index():
    return "hi"

@app.route('/register')
def register():
    pass

@app.route('/login')
def login():
    pass

if __name__ == "__main__":
    app.run(debug = True)