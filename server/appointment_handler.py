import psycopg2
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
from collections import defaultdict

load_dotenv()

# Connects to the database
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
        self.weekdays = {0: "Mon", 1: "Tue", 2: "Wed", 3: "Thu", \
                        4: "Fri", 5: "Sat", 6: "Sun"}        
    
    # Makes a query to the table with the available hours during the week of a specific doctor
    # Returns the available hours of a doctor during a week
    def available_times_in_week(self, doctor_id):
        try:
            cur = conn.cursor()

            # Queries the doctor_work_hours table by a specific doctor_id
            # Returns the availability of that doctor that week based on weekdays and hours
            query = """
                    SELECT day_of_week, start_work_hour, end_work_hour
                    FROM doctor_work_hours
                    WHERE doctor_id = %s
                """
            cur.execute(query, (4, ))
            total = cur.fetchall()
            available = defaultdict(list)
            for entry in total:
                days = []

                # Days are formatted in "X Y ..." where X and Y are specific weekdays 
                days = entry[0].split(" ")

                # Active hours during certain weekdays
                start_string = entry[1].strftime("%H:%M:%S")
                end_string = entry[2].strftime("%H:%M:%S")
                start = int(start_string.split(":")[0])
                end = int(end_string.split(":")[0])

                working_hours = []

                # If the end hour is smaller than we add 24 to it so that it loops back around
                if end < start: end = end + 24

                # Formats the total available timeframe into 1-hour timeframes
                for time in range(start, end):
                    cur = str(time % 24) + ":00:00-"
                    next = str((time + 1) % 24) + ":00:00"
                    working_hours.append(cur + next)

                # Each weekday would have different available 1-hour timeframes
                for day in days: available[day] = working_hours
       
            return available

        except Exception as e:
            print(e)

    # Given a specific date, retrieves the 3 days before it and after it along with their weekdays
    # Returns two lists containing the 7 days with the supplied date in the middle, and their weekdays
    def get_seven_days(self, date):
        try:
            # Gets the current date in datetime type so that we can find its weekday
           
            cur_date = datetime.strptime(date, '%Y-%m-%d')

            # date_list contains all the 7 days in year-month-date form
            date_list = [date]

            # weekday_list contains all the weekdays corresponding to the days in date_list
            weekday_list = [self.weekdays[cur_date.weekday()]]

            for i in range(1, 4):
                # Subtract by timedelta(i) to get the i-th day before the current day
                before = datetime.strptime(date, '%Y-%m-%d') - timedelta(i)
                date_list = [before.strftime("%Y-%m-%d")] + date_list
                weekday_list = [self.weekdays[before.weekday()]] + weekday_list

                # Add by timedelta(i) to get the i-th day after the current day
                after = datetime.strptime(date, '%Y-%m-%d') + timedelta(i)
                date_list.append(after.strftime("%Y-%m-%d"))
                weekday_list.append(self.weekdays[after.weekday()])

            return [date_list, weekday_list]

        except Exception as e:
            print(e)

if __name__ == "__main__":
    appointment_handler = AppointmentHandler()
    print(appointment_handler.available_times_in_week(2))

