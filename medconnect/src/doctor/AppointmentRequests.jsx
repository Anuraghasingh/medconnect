import React from 'react';
import './AppointmentRequests.css';

function AppointmentRequests({ requests, onUpdateStatus }) {
  const pendingRequests = requests.filter(req => req.status === 'Pending');

  if (pendingRequests.length === 0) {
    return <p className="no-requests-msg">You have no new appointment requests.</p>;
  }

  return (
    <ul className="request-list">
      {pendingRequests.map(request => (
        <li key={request.id} className="request-item">
          <div className="request-details">
            <span className="patient-name">Patient: {request.patientName}</span>
            <span className="request-time">Time: {request.time}</span>
          </div>
          <div className="request-actions">
            <button
              onClick={() => onUpdateStatus(request.id, 'Accepted')}
              className="accept-btn"
            >
              Accept
            </button>
            <button
              onClick={() => onUpdateStatus(request.id, 'Declined')}
              className="decline-btn"
            >
              Decline
            </button>
          </div>
        </li>
      ))}
    </ul>
  );
}

export default AppointmentRequests;