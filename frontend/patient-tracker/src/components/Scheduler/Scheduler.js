import React, { useState } from 'react';
import Calendar from 'react-calendar';
import Time from './Time.js'
import 'react-calendar/dist/Calendar.css';

function Scheduler() {
    const [date, setDate] = useState(new Date());
    const [showTime, setShowTime] = useState(false);

    return (
        <div className='app'>
            <h1 className='header'>React Calendar</h1>
            <div>
                <Calendar/>
            </div>
            <p>
                <span>Selected date:</span>{date.toDateString()}
            </p> 
            <Time showTime={showTime} date={date}/>

        </div>
    )
}

export default Scheduler;
