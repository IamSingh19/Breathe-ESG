import React, { useState, useEffect } from 'react';
import axios from 'axios';
import StatCard from '../components/StatCard';
import BatchList from '../components/BatchList';
import FlaggedRecords from '../components/FlaggedRecords';
import './Dashboard.css';

const API_BASE = `http://${window.location.hostname}:8000/api`;

function Dashboard() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchDashboard();
  }, []);

  const fetchDashboard = async () => {
    try {
      setLoading(true);
      const response = await axios.get(`${API_BASE}/review/dashboard/`);
      setData(response.data);
      setError(null);
    } catch (err) {
      setError('Failed to load dashboard data');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <div className="loading">Loading...</div>;
  if (error) return <div className="error-banner">{error}</div>;
  if (!data) return <div>No data available</div>;

  return (
    <div className="dashboard">
      <div className="dashboard-header">
        <h2>Review Dashboard</h2>
        <button className="refresh-btn" onClick={fetchDashboard}>
          Refresh
        </button>
      </div>

      <div className="stats-grid">
        <StatCard 
          title="Total Batches" 
          value={data.batches.total}
          color="#667eea"
        />
        <StatCard 
          title="Pending Review" 
          value={data.batches.pending}
          color="#f59e0b"
        />
        <StatCard 
          title="Approved" 
          value={data.batches.approved}
          color="#10b981"
        />
        <StatCard 
          title="Rejected" 
          value={data.batches.rejected}
          color="#ef4444"
        />
      </div>

      <div className="records-grid">
        <StatCard 
          title="Total Records" 
          value={data.records.total}
          color="#667eea"
        />
        <StatCard 
          title="Flagged Records" 
          value={data.records.total_flagged}
          color="#f59e0b"
          subtitle={`${((data.records.total_flagged / data.records.total) * 100).toFixed(1)}% of total`}
        />
        <StatCard 
          title="SAP Records" 
          value={data.records.sap.total}
          color="#8b5cf6"
          subtitle={`${data.records.sap.flagged} flagged`}
        />
        <StatCard 
          title="Utility Records" 
          value={data.records.utility.total}
          color="#06b6d4"
          subtitle={`${data.records.utility.flagged} flagged`}
        />
        <StatCard 
          title="Travel Records" 
          value={data.records.travel.total}
          color="#ec4899"
          subtitle={`${data.records.travel.flagged} flagged`}
        />
      </div>

      <div className="dashboard-content">
        <div className="left-column">
          <BatchList 
            batches={data.recent_batches}
          />
        </div>
        <div className="right-column">
          <FlaggedRecords reasons={data.flagged_reasons} />
        </div>
      </div>
    </div>
  );
}

export default Dashboard;
