import React from 'react'
import {useState} from 'react';
import "./scheduler.css";
const time = ['09:00','10:00', '11:00', '13:00','14:00','15:00', '16:00']

function Times(props) {

 const [event, setEvent] = useState(null)
 const [info, setInfo] = useState(false)

 function displayInfo(e) {
   setInfo(true);
   setEvent(e.target.innerText);
}

return (
    <div className="times">
        {props.timeList.map(times => {
        return (
            <div>
                <button onClick={(e)=> displayInfo(e)}> {times} </button>
            </div>
            )
        })}
        <div>
            {info ? `Your appointment is set to ${event} ${props.date.toDateString()}` : null}
        </div>
    </div>
  )
}

export default Times;