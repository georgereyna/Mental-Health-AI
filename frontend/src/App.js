import React from 'react';
import { BrowserRouter as Router, Route, Switch, Link } from 'react-router-dom';
import PatientDashboard from './components/PatientDashboard';
import ClinicianDashboard from './components/ClinicianDashboard';
import AdminDashboard from './components/AdminDashboard';

function App() {
  return (
    <Router>
      <div>
        <nav>
          <ul>
            <li><Link to="/patient/12345">Patient Dashboard</Link></li>
            <li><Link to="/clinician/67890">Clinician Dashboard</Link></li>
            <li><Link to="/admin/11111">Admin Dashboard</Link></li>
          </ul>
        </nav>

        <Switch>
          <Route path="/patient/:id" component={PatientDashboard} />
          <Route path="/clinician/:id" component={ClinicianDashboard} />
          <Route path="/admin/:id" component={AdminDashboard} />
        </Switch>
      </div>
    </Router>
  );
}

export default App;