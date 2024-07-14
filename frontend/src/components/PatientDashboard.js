import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';

function PatientDashboard() {
  const [data, setData] = useState(null);
  const { id } = useParams();

  useEffect(() => {
    async function fetchData() {
      const response = await fetch(`http://localhost:5000/api/patient/${id}`);
      const result = await response.json();
      setData(result);
    }
    fetchData();
  }, [id]);

  if (!data) return <div>Loading...</div>;

  return (
    <div>
      <h1>Patient Dashboard</h1>
      <p>Patient ID: {data.props.patientId}</p>
      <h2>Appointments</h2>
      <ul>
        {data.props.appointments.map((apt, index) => (
          <li key={index}>{apt.date} - {apt.time}</li>
        ))}
      </ul>
      <h2>Symptoms</h2>
      <ul>
        {data.props.symptoms.map((symptom, index) => (
          <li key={index}>{symptom.name} - Severity: {symptom.severity}</li>
        ))}
      </ul>
      <h2>Treatment Plan</h2>
      <p>{data.props.treatmentPlan.description}</p>
    </div>
  );
}

export default PatientDashboard;