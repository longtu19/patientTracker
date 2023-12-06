import psycopg2
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta

load_dotenv()

conn = psycopg2.connect(
    host = os.environ.get("ENDPOINT"),
    port = os.environ.get("PORT"),
    user = os.environ.get("MASTER_USERNAME"),
    password = os.environ.get("MASTER_PASSWORD"),
    dbname = os.environ.get("DATABASE_NAME")
)

class AppointmentHandler:
    def __init__(self):
        #List of weekdays based on id
        self.weekdays = {0: "Monday", 1: "Tuesday", 2: "Wednesday", 3: "Thursday", \
                        4: "Friday", 5: "Saturday", 6: "Sunday"}
    
    #Makes a query to the table with the available hours during the week of a specific doctor
    #Returns the available hours of a doctor during a week
    @staticmethod
    def available_times_in_week(self, doctor_id):
        try:
            available = {self.weekdays[i]: [] for i in range(7)}
            cur = conn.cursor()
            for i in range(7):
                cur.execute("SELECT times FROM doctor_work_hours WHERE doctor_id = %s AND \
                            day_of_week = %s", (doctor_id, self.weekdays[i], ))
                hours = cur.fetchall()
                available[self.weekdays[i]] = hours
            return available

        except Exception as e:
            print(e)

    #Given a specific date, retrieves the 3 days before it and after it along with their weekdays
    #Returns two lists containing the 7 days with the supplied date in the middle, and their weekdays
    @staticmethod
    def get_seven_days(self, date):
        try:
            cur_date = datetime.strptime(date, '%Y-%m-%d')
            date_list = [cur_date.strftime("%Y/%m/%d")]
            weekday_list = [self.weekdays[cur_date.weekday()]]

            for i in range(1, 4):
                before = datetime.strptime(date, '%Y-%m-%d') - timedelta(i)
                date_list = [before.strftime("%Y/%m/%d")] + date_list
                weekday_list = [self.weekdays[before.weekday()]] + weekday_list

                after = datetime.strptime(date, '%Y-%m-%d') + timedelta(i)
                date_list.append(after.strftime("%Y/%m/%d"))
                weekday_list.append(self.weekdays[after.weekday()])

            return [date_list, weekday_list]

        except Exception as e:
            print(e)
