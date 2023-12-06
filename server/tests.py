import unittest
from flask import Flask, jsonify
from dotenv import load_dotenv
from app import app
import psycopg2
import os
import warnings
load_dotenv()
app = Flask(__name__)

conn = psycopg2.connect(
    host = os.environ.get("ENDPOINT"),
    port = os.environ.get("PORT"),
    user = os.environ.get("MASTER_USERNAME"),
    password = os.environ.get("MASTER_PASSWORD"),
    dbname = os.environ.get("DATABASE_NAME")
)

warnings.filterwarnings(action="ignore", message="unclosed", category=ResourceWarning)

test_object = {"email": "abc@gmail.com", "password": '123456', "first_name": "Bob", "last_name": "Americanman", \
            "status": "patient", "birthday": "12/24/2002", "sex": "Male"}

class FlaskTest(unittest.TestCase):
    def setUp(self) -> None:
        app.config['TESTING'] = True
        self.client = app.test_client()

    def test_register(self):
        self.client.post('/register', data=test_object)
        response = self.client.get('/register')
        print("Request result: ", response.data)

if __name__ == '__main__':
    unittest.main()