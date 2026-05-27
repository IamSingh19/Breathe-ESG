import React from 'react';
import './StatCard.css';

function StatCard({ title, value, color, subtitle }) {
  return (
    <div className="stat-card" style={{ borderLeftColor: color }}>
      <div className="stat-card-header">
        <div className="stat-icon" style={{ backgroundColor: `${color}20` }}>
          <div style={{ color, fontSize: '1.5rem' }}>📊</div>
        </div>
      </div>
      <div className="stat-value" style={{ color }}>
        {typeof value === 'number' ? value.toLocaleString() : value}
      </div>
      <div className="stat-title">{title}</div>
      {subtitle && <div className="stat-subtitle">{subtitle}</div>}
    </div>
  );
}

export default StatCard;
