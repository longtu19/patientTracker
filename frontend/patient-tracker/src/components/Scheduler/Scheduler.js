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
  return res;
}

function Scheduler() {
  const [date, setDate] = useState(new Date());
  const [showTime, setShowTime] = useState(false);
  const docId = localStorage.getItem("docId");
  const patId = localStorage.getItem("role_id")
  const [timeList, setTimeList] = useState({});

  useEffect(() => {
    const fetchDate = async () => {
      const formattedDate = formatDate(date);
      try {
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
        if (result.Result === "Success") {
          setTimeList(result.Times);
        }
      } catch (error) {
        alert(error);
      }
    };

    fetchDate();
  }, [docId, date]);

  return (
    <div className="container">
      <div className="row">
        <div className="calendar col-2">
          <Calendar
            onChange={setDate}
            value={date}
            onClickDay={() => setShowTime(true)}
          />
        </div>
        <div className="col-2">
          {showTime && <Time date={formatDate(date)} timeList={timeList} docId = {docId} patId = {patId} />}
        </div>
      </div>
    </div>
  );
}

export default Scheduler;
