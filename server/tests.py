import unittest
from flask import Flask, jsonify
from dotenv import load_dotenv
from app import app
import psycopg2
import os
import warnings
load_dotenv()
conn = psycopg2.connect(
    host = os.environ.get("ENDPOINT"),
    port = os.environ.get("PORT"),
    user = os.environ.get("MASTER_USERNAME"),
    password = os.environ.get("MASTER_PASSWORD"),
    dbname = os.environ.get("DATABASE_NAME")
)

warnings.filterwarnings(action="ignore", message="unclosed", category=ResourceWarning)

register_object = {
    "email": "abcdef@gmail.com", 
    "password": "123456", 
    "first_name": "Bob", 
    "last_name": "Americanman", 
    "status": "patient", 
    "birthday": "12/24/2002", 
    "sex": "Male",
    "role": "patient"
}

login_object = {
    "email": "traudaica123@gmail.com", 
    "password": "traudaica123", 
}

class FlaskTest(unittest.TestCase):
    def setUp(self) -> None:
        app.config['TESTING'] = True
        self.client = app.test_client()

    def test_landing(self):
        response = self.client.get('/')
        self.assertEqual(response.data.decode(), "Welcome")

    def test_register(self):
        response = self.client.post('/register', json=register_object)
        self.assertEqual(response.json["Result"], "Success")
        
        cur = conn.cursor()
        query = "DELETE FROM system_user WHERE email = %s"
        cur.execute(query, ("abcdef@gmail.com", ))
        conn.commit()
    
    def test_login(self):
        response = self.client.post('/login', json=login_object)
        self.assertEqual(response.json["Result"], "Success")

if __name__ == '__main__':
    unittest.main()