import React from 'react';
import { BrowserRouter, Routes, Route, Link } from 'react-router-dom';
import Dashboard from './pages/Dashboard';
import BatchDetail from './pages/BatchDetail';
import './App.css';

function App() {
  return (
    <BrowserRouter>
      <div className="app">
        <header className="app-header">
          <h1>Breathe ESG - Data Review Platform</h1>
          <p>Ingest, normalize, and review emissions data</p>
        </header>

        <nav className="app-nav">
          <Link to="/">Dashboard</Link>
        </nav>

        <main className="app-main">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/batch/:batchId" element={<BatchDetail />} />
          </Routes>
        </main>
      </div>
    </BrowserRouter>
  );
}

export default App;
