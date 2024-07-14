import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';

function ClinicianDashboard() {
  const [data, setData] = useState(null);
  const { id } = useParams();

  useEffect(() => {
    async function fetchData() {
      const response = await fetch(`http://localhost:5000/api/clinician/${id}`);
      const result = await response.json();
      setData(result);
    }
    fetchData();
  }, [id]);

  if (!data) return <div>Loading...</div>;

  return (
    <div>
      <h1>Clinician Dashboard</h1>
      <p>Clinician ID: {data.props.clinicianId}</p>
      <h2>Patients</h2>
      <ul>
        {data.props.patients.map((patient, index) => (
          <li key={index}>{patient.name} - Last Visit: {patient.lastVisit}</li>
        ))}
      </ul>
      <h2>Appointments</h2>
      <ul>
        {data.props.appointments.map((apt, index) => (
          <li key={index}>{apt.time} - {apt.patientName}</li>
        ))}
      </ul>
      <h2>Alerts</h2>
      <ul>
        {data.props.alerts.map((alert, index) => (
          <li key={index}>{alert.patientName}: {alert.message}</li>
        ))}
      </ul>
    </div>
  );
}

export default ClinicianDashboard;