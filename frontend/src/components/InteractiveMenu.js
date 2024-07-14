import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

function InteractiveMenu() {
  const [selectedOption, setSelectedOption] = useState('');
  const [userId, setUserId] = useState('');
  const navigate = useNavigate();

  const handleSubmit = (e) => {
    e.preventDefault();
    if (selectedOption && userId) {
      navigate(`/${selectedOption}/${userId}`);
    }
  };

  return (
    <div>
      <h1>Mental Health Clinic AI System</h1>
      <form onSubmit={handleSubmit}>
        <div>
          <button type="button" onClick={() => setSelectedOption('patient')}>Patient Interface</button>
          <button type="button" onClick={() => setSelectedOption('clinician')}>Clinician Interface</button>
          <button type="button" onClick={() => setSelectedOption('admin')}>Administrator Interface</button>
        </div>
        {selectedOption && (
          <div>
            <label>
              Enter {selectedOption} ID:
              <input 
                type="text" 
                value={userId} 
                onChange={(e) => setUserId(e.target.value)} 
                required 
              />
            </label>
            <button type="submit">Submit</button>
          </div>
        )}
      </form>
    </div>
  );
}

export default InteractiveMenu;