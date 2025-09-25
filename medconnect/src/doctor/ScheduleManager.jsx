import React, { useState } from 'react';
import './ScheduleManager.css';

function ScheduleManager({ schedule, onAddTimeSlot, onRemoveTimeSlot }) {
  const [newDay, setNewDay] = useState('Monday');
  const [newTime, setNewTime] = useState('');

  const handleAddTime = (e) => {
    e.preventDefault();
    if (newTime) {
      onAddTimeSlot(newDay, newTime);
      setNewTime('');
    }
  };

  return (
    <div className="schedule-manager-container">
      <form onSubmit={handleAddTime} className="add-slot-form">
        <select value={newDay} onChange={(e) => setNewDay(e.target.value)}>
          {['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'].map(day => (
            <option key={day} value={day}>{day}</option>
          ))}
        </select>
        <input
          type="time"
          value={newTime}
          onChange={(e) => setNewTime(e.target.value)}
          required
        />
        <button type="submit" className="add-btn">Add Slot</button>
      </form>

      <div className="schedule-list">
        {schedule.map(daySchedule => (
          <div key={daySchedule.day} className="day-schedule">
            <h3>{daySchedule.day}</h3>
            {daySchedule.timeSlots.length > 0 ? (
              <ul>
                {daySchedule.timeSlots.map(time => (
                  <li key={time}>
                    <span>{time}</span>
                    <button onClick={() => onRemoveTimeSlot(daySchedule.day, time)} className="remove-btn">
                      &times;
                    </button>
                  </li>
                ))}
              </ul>
            ) : (
              <p>No slots available.</p>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}

export default ScheduleManager;