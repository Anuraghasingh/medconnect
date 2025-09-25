import React from 'react';
import './AppointmentList.css';

function AppointmentList({ appointments, onCancelAppointment }) {
  if (appointments.length === 0) {
    return <p className="no-appointments-msg">You have no upcoming appointments.</p>;
  }

  return (
    <ul className="appointment-list">
      {appointments.map(appointment => (
        <li key={appointment.id} className="appointment-item">
          <div className="appointment-details">
            <span className="patient-name">Patient: {appointment.patientName}</span>
            <span className="doctor-name">Doctor: {appointment.doctorName}</span>
            <span className="appointment-date">Date: {new Date(appointment.appointmentDate).toLocaleString()}</span>
          </div>
          <button onClick={() => onCancelAppointment(appointment.id)} className="cancel-btn">Cancel</button>
        </li>
      ))}
    </ul>
  );
}

export default AppointmentList;