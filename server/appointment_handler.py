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
        self.weekdays = {0: "Mon", 1: "Tue", 2: "Wed", 3: "Thu", \
            4: "Fri", 5: "Sat", 6: "Sun"}        
    
    #Makes a query to the table with the available hours during the week of a specific doctor
    #Returns the available hours of a doctor during a week
    def available_times_in_week(self, doctor_id):
        try:
            cur = conn.cursor()
            cur.execute("SELECT day_of_week, start_work_hour, end_work_hour FROM doctor_work_hours WHERE doctor_id = %s", (doctor_id, ))
            total = cur.fetchall()

            days = total[0].split(" ")
            start = int(total[1].split(":")[0])
            end = int(total[2].split(":")[0])

            working_hours = []
            if end < start: end = end + 24
            for time in range(start, end):
                cur = str(time % 24) + ":00-"
                next = str((time + 1) % 24) + ":00"
                working_hours.append(cur + next)

            available = {day: working_hours for day in days}
            return available

        except Exception as e:
            print(e)

    #Given a specific date, retrieves the 3 days before it and after it along with their weekdays
    #Returns two lists containing the 7 days with the supplied date in the middle, and their weekdays
    def get_seven_days(self, date):
        try:
            cur_date = datetime.strptime(date, '%Y-%m-%d')
            date_list = [date]
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

if __name__ == "__main__":
    appointment_handler = AppointmentHandler()
    print(appointment_handler.available_times_in_week(2))

