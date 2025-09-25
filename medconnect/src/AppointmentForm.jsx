import React, { useState } from 'react';
import './AppointmentForm.css';

function AppointmentForm({ onAddAppointment }) {
  const [patientName, setPatientName] = useState('');
  const [doctorName, setDoctorName] = useState('');
  const [appointmentDate, setAppointmentDate] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!patientName || !doctorName || !appointmentDate) {
      alert('Please fill in all fields.');
      return;
    }
    onAddAppointment({ patientName, doctorName, appointmentDate });
    setPatientName('');
    setDoctorName('');
    setAppointmentDate('');
  };

  return (
    <form className="appointment-form" onSubmit={handleSubmit}>
      <div className="form-group">
        <label htmlFor="patient-name">Patient Name</label>
        <input
          type="text"
          id="patient-name"
          value={patientName}
          onChange={(e) => setPatientName(e.target.value)}
          placeholder="Enter your name"
          required
        />
      </div>

      <div className="form-group">
        <label htmlFor="doctor-name">Doctor Name / Specialization</label>
        <input
          type="text"
          id="doctor-name"
          value={doctorName}
          onChange={(e) => setDoctorName(e.target.value)}
          placeholder="e.g., Dr. Anurag, Ram"
          required
        />
      </div>

      <div className="form-group">
        <label htmlFor="appointment-date">Appointment Date & Time</label>
        <input
          type="datetime-local"
          id="appointment-date"
          value={appointmentDate}
          onChange={(e) => setAppointmentDate(e.target.value)}
          required
        />
      </div>

      <button type="submit" className="submit-btn">Book Appointment</button>
    </form>
  );
}

export default AppointmentForm;