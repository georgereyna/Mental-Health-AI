import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';

function AdminDashboard() {
  const [data, setData] = useState(null);
  const { id } = useParams();

  useEffect(() => {
    async function fetchData() {
      const response = await fetch(`http://localhost:5000/api/admin/${id}`);
      const result = await response.json();
      setData(result);
    }
    fetchData();
  }, [id]);

  if (!data) return <div>Loading...</div>;

  return (
    <div>
      <h1>Admin Dashboard</h1>
      <p>Admin ID: {data.props.adminId}</p>
      <h2>Clinic Statistics</h2>
      <ul>
        {Object.entries(data.props.clinicStats).map(([key, value], index) => (
          <li key={index}>{key}: {value}</li>
        ))}
      </ul>
      <h2>Compliance Reports</h2>
      <ul>
        {data.props.complianceReports.map((report, index) => (
          <li key={index}>{report.title} - Status: {report.status}</li>
        ))}
      </ul>
      <h2>Staff Performance</h2>
      <ul>
        {Object.entries(data.props.staffPerformance).map(([staff, perf], index) => (
          <li key={index}>{staff} - Patients: {perf.patients}, Satisfaction: {perf.satisfaction}</li>
        ))}
      </ul>
    </div>
  );
}

export default AdminDashboard;