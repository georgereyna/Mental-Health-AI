import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';

function ClinicianDashboard() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const { id } = useParams();

  useEffect(() => {
    async function fetchData() {
      try {
        setLoading(true);
        console.log(`Fetching data for clinician ${id}...`);
        const response = await fetch(`http://localhost:8000/api/clinician/${id}`);
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
      <h1>Clinician Dashboard</h1>
      <p>Clinician ID: {data.props?.clinicianId}</p>
      <h2>Patients</h2>
      <ul>
        {data.props?.patients?.map((patient, index) => (
          <li key={index}>{patient.name} - Last Visit: {patient.lastVisit}</li>
        ))}
      </ul>
      <h2>Upcoming Appointments</h2>
      <ul>
        {data.props?.appointments?.map((apt, index) => (
          <li key={index}>{apt.date} - {apt.time} - Patient: {apt.patientName}</li>
        ))}
      </ul>
      <h2>Alerts</h2>
      <ul>
        {data.props?.alerts?.map((alert, index) => (
          <li key={index}>{alert.patientName}: {alert.message}</li>
        ))}
      </ul>
    </div>
  );
}

export default ClinicianDashboard;