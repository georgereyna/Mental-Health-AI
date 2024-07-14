import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';

function AdminDashboard() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const { id } = useParams();

  useEffect(() => {
    async function fetchData() {
      try {
        setLoading(true);
        console.log(`Fetching data for admin ${id}...`);
        const response = await fetch(`http://localhost:8000/api/admin/${id}`);
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
      <h1>Admin Dashboard</h1>
      <p>Admin ID: {data.props?.adminId}</p>
      <h2>Clinic Statistics</h2>
      <ul>
        {Object.entries(data.props?.clinicStats || {}).map(([key, value], index) => (
          <li key={index}>{key}: {value}</li>
        ))}
      </ul>
      <h2>Compliance Reports</h2>
      <ul>
        {data.props?.complianceReports?.map((report, index) => (
          <li key={index}>{report.title} - Status: {report.status}</li>
        ))}
      </ul>
      <h2>Staff Performance</h2>
      <ul>
        {Object.entries(data.props?.staffPerformance || {}).map(([staff, perf], index) => (
          <li key={index}>{staff} - Patients: {perf.patients}, Satisfaction: {perf.satisfaction}</li>
        ))}
      </ul>
    </div>
  );
}

export default AdminDashboard;