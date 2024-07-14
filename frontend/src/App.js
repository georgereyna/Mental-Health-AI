import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import InteractiveMenu from './components/InteractiveMenu';
import PatientDashboard from './components/PatientDashboard';
import ClinicianDashboard from './components/ClinicianDashboard';
import AdminDashboard from './components/AdminDashboard';

function App() {
  return (
    <Router>
      <div>
        <Routes>
          <Route path="/" element={<InteractiveMenu />} />
          <Route path="/patient/:id" element={<PatientDashboard />} />
          <Route path="/clinician/:id" element={<ClinicianDashboard />} />
          <Route path="/admin/:id" element={<AdminDashboard />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;