import React, { useState } from 'react';
import AppointmentForm from './AppointmentForm';
import AppointmentList from './AppointmentList';
import './App.css'; 

function App() {
  const [appointments, setAppointments] = useState([]);

  const addAppointment = (newAppointment) => {
    setAppointments([...appointments, { ...newAppointment, id: Date.now() }]);
  };

  const cancelAppointment = (id) => {
    setAppointments(appointments.filter(appointment => appointment.id !== id));
  };

  return (
    <div className="patient-module-container">
      <header className="patient-header">
        <h1>Patient Appointment Portal</h1>
      </header>
      
      <main className="patient-main">
        <section className="appointment-section">
          <h2>Book a New Appointment</h2>
          <AppointmentForm onAddAppointment={addAppointment} />
        </section>

        <section className="appointment-section">
          <h2>Your Upcoming Appointments</h2>
          <AppointmentList appointments={appointments} onCancelAppointment={cancelAppointment} />
        </section>
      </main>
    </div>
  );
}

export default App;