// frontend/src/App.jsx - Test with your real Dashboard component
import React from 'react';
import { Routes, Route, Link } from 'react-router-dom';

// Import your actual Dashboard component
import Dashboard from './components/dashboard/Dashboard';

// Home component for testing
const TestHome = () => (
  <div style={{ padding: '20px', textAlign: 'center' }}>
    <h1>🏠 KairoCal Home</h1>
    <p>Router issue fixed! Now testing real Dashboard component.</p>
    <div style={{ margin: '20px 0' }}>
      <Link 
        to="/dashboard" 
        style={{
          display: 'inline-block',
          padding: '12px 24px',
          backgroundColor: '#4f46e5',
          color: 'white',
          textDecoration: 'none',
          borderRadius: '8px',
          margin: '10px'
        }}
      >
        Go to Real Dashboard
      </Link>
    </div>
    <div style={{
      backgroundColor: '#fef3c7',
      padding: '15px',
      borderRadius: '8px',
      margin: '20px 0',
      fontSize: '14px'
    }}>
      <strong>🔍 What we're testing:</strong><br/>
      If Dashboard loads instantly → Dashboard component is fine<br/>
      If Dashboard hangs → Issue is in Dashboard.jsx or its imports
    </div>
  </div>
);

function App() {
  return (
    <div style={{ fontFamily: 'Arial, sans-serif' }}>
      <Routes>
        <Route path="/" element={<TestHome />} />
        <Route path="/dashboard" element={
          <React.Suspense fallback={
            <div style={{ padding: '20px', textAlign: 'center' }}>
              <h2>⏳ Loading Dashboard...</h2>
              <p>If this stays forever, there's an issue with the Dashboard component.</p>
            </div>
          }>
            <Dashboard />
          </React.Suspense>
        } />
      </Routes>
    </div>
  );
}

export default App;