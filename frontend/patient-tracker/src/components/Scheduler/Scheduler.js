import React, { useState } from 'react';
import Calendar from 'react-calendar';
import Time from './Time.js'
import 'react-calendar/dist/Calendar.css';
import './scheduler.css';

function Scheduler() {
    const [date, setDate] = useState(new Date());
    const [showTime, setShowTime] = useState(false) 
    
    return (
     <div className='background'>
        <div className='calendar'>

       <div>
        <Calendar onChange={setDate} value={date} onClickDay={() => setShowTime(true)}/>
       </div>
    
       {date.length > 0 ? (
       <p>
         <span>Start:</span>
         {date[0].toDateString()}
         &nbsp;
         &nbsp;
         <span>End:</span>{date[1].toDateString()}
       </p>
              ) : (
       <p>
          <span>Selected date:</span>{date.toDateString()}
       </p> 
              )
       }
       <Time showTime={showTime} date={date}/>
       </div>
        </div>
    )   
}

export default Scheduler;
