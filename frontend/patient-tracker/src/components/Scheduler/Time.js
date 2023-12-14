import React from "react";
import { useState } from "react";
import "./scheduler.css";
const time = ["09:00", "10:00", "11:00", "13:00", "14:00", "15:00", "16:00"];

// Times object to represent doc's availability
function Times(props) {
  const timeObj = props.timeList;
  const [selectedTime, setSelectedTime] = useState(null);
  const [event, setEvent] = useState(null);
  const [info, setInfo] = useState(false);
  let selectedDate = props.date;

  const formatTime = (selectedDate, selectedTime) => {
    const [startTime, endTime] = selectedTime.split("-");

    const formattedStartTime = `${selectedDate} ${startTime}`;
    const formattedEndTime = `${selectedDate} ${endTime}`;

    // Replace '-' with '/' in the date for the desired format
    const finalFormattedStartTime = formattedStartTime.replace(/-/g, "/");
    const finalFormattedEndTime = formattedEndTime.replace(/-/g, "/");

    return {
      startTime: finalFormattedStartTime,
      endTime: finalFormattedEndTime,
    };
  };

  // Sends selected time to backend with patient id and doctor id
  const makeApt = async (time) => {
    let selectedTimeObj = formatTime(selectedDate, selectedTime)
    const response = await fetch("http://127.0.0.1:5000/make_appointment", {
      method: "POST",
      mode: "cors",
      body: JSON.stringify({
        start_time: selectedTimeObj["startTime"],
        end_time: selectedTimeObj["endTime"],
        patient_id: props.patId,
        doctor_id: props.docId,
      }),
      headers: {
        "Content-Type": "application/json",
      },
    });

    const res = await response.json();
    console.log(res);
    if (res.Result === "Success") {
      alert("Your appointment is set on " + selectedDate + " " + time + "!");
    } else {
      alert("Error making appointment at this time. Please try again late!");
    }
  };

  function displayInfo(e) {
    setInfo(true);
    setEvent(e.target.innerText);
  }

  return (
    // UIUX
    <div className="times">
      {timeObj[selectedDate] &&
        timeObj[selectedDate].map((time) => {
          return (
            <div className="timeSlot">
              <input
                class="form-check-input"
                type="radio"
                value={time}
                name="free-time"
                onChange={() => setSelectedTime(time)}
              />
              <label className="form-check-label" for="inlineCheckbox1">
                {" "}
                {time}
              </label>{" "}
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
      {timeObj[selectedDate] && (
        <div className="aptButton">
          <button onClick={() => makeApt(selectedTime)}>
            Make Appointment
          </button>
        </div>
      )}
    </div>
  );
}

export default Times;
