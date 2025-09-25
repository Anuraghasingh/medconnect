import React, { useState } from 'react';
import ScheduleManager from './ScheduleManager';
import AppointmentRequests from './AppointmentRequests';
import './Doctor.css'; // Main CSS file

function Doctor() {
  const [schedule, setSchedule] = useState([
    { day: 'Monday', timeSlots: ['09:00 AM', '10:00 AM', '11:00 AM'] },
    { day: 'Tuesday', timeSlots: ['02:00 PM', '03:00 PM'] },
  ]);

  const [appointmentRequests, setAppointmentRequests] = useState([
    { id: 1, patientName: 'Amrit kumar', time: 'Monday, 10:00 AM', status: 'Pending' },
    { id: 2, patientName: 'Aman kumar', time: 'Tuesday, 03:00 PM', status: 'Pending' },
  ]);

  const addTimeSlot = (day, time) => {
    setSchedule(schedule.map(s =>
      s.day === day ? { ...s, timeSlots: [...s.timeSlots, time].sort() } : s
    ));
  };

  const removeTimeSlot = (day, time) => {
    setSchedule(schedule.map(s =>
      s.day === day ? { ...s, timeSlots: s.timeSlots.filter(t => t !== time) } : s
    ));
  };

  const updateAppointmentStatus = (id, newStatus) => {
    setAppointmentRequests(appointmentRequests.map(req =>
      req.id === id ? { ...req, status: newStatus } : req
    ));
  };

  return (
    <div className="doctor-module-container">
      <header className="doctor-header">
        <h1>Dr. Agrawal Dashboard</h1>
        <p>Manage your schedule and appointments efficiently.</p>
      </header>

      <main className="doctor-main">
        <section className="dashboard-section">
          <h2>Manage Schedule</h2>
          <ScheduleManager 
            schedule={schedule} 
            onAddTimeSlot={addTimeSlot} 
            onRemoveTimeSlot={removeTimeSlot} 
          />
        </section>

        <section className="dashboard-section">
          <h2>Appointment Requests</h2>
          <AppointmentRequests 
            requests={appointmentRequests} 
            onUpdateStatus={updateAppointmentStatus} 
          />
        </section>
      </main>
    </div>
  );
}

export default  Doctor ;