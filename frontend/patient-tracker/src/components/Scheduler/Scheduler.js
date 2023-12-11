import React, { useState, useEffect } from "react";
import Calendar from "react-calendar";
import Time from "./Time.js";
import "react-calendar/dist/Calendar.css";
import "./scheduler.css";

function formatDate(originalDate) {
  const year = originalDate.getFullYear();
  const month = (originalDate.getMonth() + 1).toString().padStart(2, "0"); // Months are zero-based, so we add 1
  const day = originalDate.getDate().toString().padStart(2, "0");
  const res = `${year}-${month}-${day}`;
  return res

}

function Scheduler() {
  const [date, setDate] = useState(new Date());
  const [showTime, setShowTime] = useState(false);
  const docId = localStorage.getItem("docId");
  const [timeList, setTimeList] = useState([]);

  useEffect(() => {
    const fetchDate = async () => {
      try {
       const formattedDate = formatDate(date)
       console.log(formattedDate)
       console.log(docId)
        const response = await fetch(
          "http://127.0.0.1:5000/get_appointment_times",
          {
            method: "POST",
            mode: "cors",
            body: JSON.stringify({
              date: formattedDate,
              doctor_id: docId,
            }),
            headers: {
              "Content-Type": "application/json",
            },
          }
        );
        const result = await response.json();
        console.log(result);
        if (result.Result === "Success") {
          setTimeList(result.Times);
          console.log("TIme here");
          console.log(timeList);
        }
      } catch (error) {
        alert(error);
      }
    };

    fetchDate();
  }, [docId, date]);

  return (
    <div className="background">
      <div className="calendar">
        <div>
          <Calendar
            onChange={setDate}
            value={date}
            onClickDay={() => setShowTime(true)}
          />
        </div>

        {date.length > 0 ? (
          <p>
            <span>Start:</span>
            {date[0].toDateString()}
            &nbsp; &nbsp;
            <span>End:</span>
            {date[1].toDateString()}
          </p>
        ) : (
          <p>
            <span>Selected date:</span>
            {date.toDateString()}
          </p>
        )}
        {showTime && <Time date={date} timeList={timeList} />}
      </div>
    </div>
  );
}

export default Scheduler;
