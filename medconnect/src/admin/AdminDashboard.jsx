import React, { useState } from 'react';
import './AdminDashboard.css';

const initialPatients = [
  { id: 1, name: '   Anil singh', email: 'john.doe@example.com', status: 'Approved' },
  { id: 2, name: 'Ramesh Sharma', email: 'jane.smith@example.com', status: 'Pending' },
];

const initialDoctors = [
  { id: 101, name: ' Smriti', specialization: 'Cardiology', status: 'Active' },
  { id: 102, name: ' Rakesh Rosha', specialization: 'Neurology', status: 'Active' },
];

const initialAppointments = [
  { id: 1001, patientName: 'Sanjay Yadav', doctorName: 'Dr. girish', date: '2025-09-20', status: 'Confirmed' },
  { id: 1002, patientName: 'Mamta Singh', doctorName: 'Dr. manmohan', date: '2025-09-22', status: 'Pending' },
];

function AdminDashboard() {
  const [patients, setPatients] = useState(initialPatients);
  const [doctors, setDoctors] = useState(initialDoctors);
  const [appointments, setAppointments] = useState(initialAppointments);

  const addPatient = (newPatient) => {
    setPatients([...patients, { ...newPatient, id: Date.now(), status: 'Pending' }]);
  };
  const updatePatient = (updatedPatient) => {
    setPatients(patients.map(p => p.id === updatedPatient.id ? updatedPatient : p));
  };
  const deletePatient = (id) => {
    setPatients(patients.filter(p => p.id !== id));
  };

  const addDoctor = (newDoctor) => {
    setDoctors([...doctors, { ...newDoctor, id: Date.now(), status: 'Active' }]);
  };
  const updateDoctor = (updatedDoctor) => {
    setDoctors(doctors.map(d => d.id === updatedDoctor.id ? updatedDoctor : d));
  };
  const deleteDoctor = (id) => {
    setDoctors(doctors.filter(d => d.id !== id));
  };

  const generateReport = () => {
    alert(`Generating system report...\nTotal Patients: ${patients.length}\nTotal Doctors: ${doctors.length}\nTotal Appointments: ${appointments.length}`);
  };

  return (
    <div className="admin-dashboard-container">
      <header className="admin-header">
        <h1>Admin Panel</h1>
        <p>Manage the entire system and monitor activities.</p>
        <button className="report-btn" onClick={generateReport}>Generate System Report</button>
      </header>

      <main className="admin-main">
        <section className="admin-section patient-management">
          <h2>Patient Management</h2>
          <div className="user-list">
            {patients.map(p => (
              <div key={p.id} className="user-card">
                <span className="user-name">{p.name}</span>
                <span className={`user-status status-${p.status.toLowerCase()}`}>{p.status}</span>
                <div className="user-actions">
                  <button onClick={() => updatePatient({...p, status: 'Approved'})}>Approve</button>
                  <button onClick={() => deletePatient(p.id)} className="delete-btn">Delete</button>
                </div>
              </div>
            ))}
          </div>
        </section>

        <section className="admin-section doctor-management">
          <h2>Doctor Management</h2>
          <div className="user-list">
            {doctors.map(d => (
              <div key={d.id} className="user-card">
                <span className="user-name">Dr. {d.name}</span>
                <span className="user-specialization">{d.specialization}</span>
                <div className="user-actions">
                  <button>Edit</button>
                  <button onClick={() => deleteDoctor(d.id)} className="delete-btn">Remove</button>
                </div>
              </div>
            ))}
          </div>
        </section>

        <section className="admin-section appointment-monitoring">
          <h2>Appointment Overview</h2>
          <div className="appointment-list">
            {appointments.map(a => (
              <div key={a.id} className="appointment-item">
                <span className="item-detail">Patient: {a.patientName}</span>
                <span className="item-detail">Doctor: {a.doctorName}</span>
                <span className="item-detail">Date: {a.date}</span>
                <span className={`item-status status-${a.status.toLowerCase()}`}>{a.status}</span>
              </div>
            ))}
          </div>
        </section>
      </main>
    </div>
  );
}

export default AdminDashboard;