import React from "react";
import { useState } from "react";
import "./scheduler.css";
const time = ["09:00", "10:00", "11:00", "13:00", "14:00", "15:00", "16:00"];

function Times(props) {
  const timeObj = props.timeList;

  const [event, setEvent] = useState(null);
  const [info, setInfo] = useState(false);
  let selectedDate = props.date;

  const makeApt = async (time) => {
    console.log("make apt")
    let timeSplit = time.split("-")
    const response = await fetch("http://127.0.0.1:5000/make_appointment", {
      method: "POST",
      mode: "cors",
      body: JSON.stringify({ start_time: timeSplit[0], end_time: timeSplit[1], patient_id: props.patId, doctor_id: props.docId }),
      headers: {
        "Content-Type": "application/json",
      },
    });

    const res = await response.json()
    console.log(res)
    if (res.Result === "Success"){
        console.log("oke chua")
        alert("Your appointment is set on " + selectedDate + time + "!")
    }
    else{
        alert("Error making appointment at this time. Please try again late!")
    }
  };

  function displayInfo(e) {
    setInfo(true);
    setEvent(e.target.innerText);
  }

  return (
    <div className="times">
      {timeObj[selectedDate] &&
        timeObj[selectedDate].map((time) => {
          return (
            <div className="timeSlot">
              <button onClick={() => makeApt(time)}> {time} </button>
            </div>
          );
        })}
      {timeObj[selectedDate] === undefined && (
        <div>No available hour on this day. Please select another day!</div>
      )}
      <div>
        {timeObj[selectedDate] && info
          ? `Your appointment is set to ${event} ${selectedDate}`
          : null}
      </div>
    </div>
  );
}

export default Times;
