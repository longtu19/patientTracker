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

weekdays = {0: "Monday", 1: "Tuesday", 2: "Wednesday", 3: "Thursday", \
                    4: "Friday", 5: "Saturday", 6: "Sunday"}

def list_intersection(list1, list2):
    return list(set(list1) & set(list2))

def available_times_in_week(doctor_id):
    try:
        times = ["8:00AM - 9:00AM", "9:00AM - 10:00AM", "10:00AM - 11:00AM", "11:00AM - 12:00PM", \
                "12:00PM - 1:00PM", "1:00PM - 2:00PM", "2:00PM - 3:00PM", "3:00PM - 4:00PM", "4:00PM - 5:00PM"]
        available = {weekdays[i]: times for i in range(7)}
        cur = conn.cursor()
        for i in range(7):
            cur.execute("SELECT times FROM doctor_work_hours WHERE doctor_id = %s AND \
                        day_of_week = %s", (doctor_id, weekdays[i], ))
            hours = cur.fetchall()
            available[weekdays[i]] = list_intersection(available[weekdays[i]], hours)
        return available

    except Exception as e:
        print(e)

def get_seven_days(date):
    cur_date = datetime.strptime(date, '%Y-%m-%d')
    date_list = [cur_date]
    weekday_list = [weekdays[cur_date.weekday()]]

    for i in range(1, 4):
        before = datetime.strptime(date, '%Y-%m-%d') - timedelta(i)
        date_list = [before] + date_list
        weekday_list = [weekdays[before.weekday()]] + weekday_list

        after = datetime.strptime(date, '%Y-%m-%d') + timedelta(i)
        date_list.append(after)
        weekday_list.append(weekdays[after.weekday()])

    return [date_list, weekday_list]

if __name__ == "__main__":
    print(available_times_in_week(0))
    print(get_seven_days('2023-12-06'))