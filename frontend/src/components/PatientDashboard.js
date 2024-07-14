import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';

function PatientDashboard() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const { id } = useParams();

  useEffect(() => {
    async function fetchData() {
      try {
        setLoading(true);
        console.log(`Fetching data for patient ${id}...`);
        const response = await fetch(`http://localhost:8000/api/patient/${id}`);
        console.log('Response status:', response.status);
        console.log('Response headers:', response.headers);
        
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const result = await response.json();
        console.log('Data received:', result);
        setData(result);
      } catch (e) {
        console.error("There was a problem fetching the data:", e);
        setError(e.message);
      } finally {
        setLoading(false);
      }
    }
    fetchData();
  }, [id]);

  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error}</div>;
  if (!data) return <div>No data available</div>;

  return (
    <div>
      <h1>Patient Dashboard</h1>
      <p>Patient ID: {data.props?.patientId}</p>
      <h2>Appointments</h2>
      <ul>
        {data.props?.appointments?.map((apt, index) => (
          <li key={index}>{apt.date} - {apt.time}</li>
        ))}
      </ul>
      <h2>Symptoms</h2>
      <ul>
        {data.props?.symptoms?.map((symptom, index) => (
          <li key={index}>{symptom.name} - Severity: {symptom.severity}</li>
        ))}
      </ul>
      <h2>Treatment Plan</h2>
      <p>{data.props?.treatmentPlan?.description}</p>
    </div>
  );
}

export default PatientDashboard;