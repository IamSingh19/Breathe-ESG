import React from 'react';
import './FlaggedRecords.css';

function FlaggedRecords({ reasons }) {
  const sortedReasons = Object.entries(reasons)
    .sort((a, b) => b[1] - a[1])
    .slice(0, 10);

  const maxCount = sortedReasons.length > 0 ? sortedReasons[0][1] : 1;

  return (
    <div className="flagged-records">
      <div className="flagged-header">
        <h3>Flagged Records</h3>
        <span className="flag-icon">⚠️</span>
      </div>
      <div className="reasons-list">
        {sortedReasons.length > 0 ? (
          sortedReasons.map(([reason, count]) => (
            <div key={reason} className="reason-item">
              <div className="reason-label">{reason}</div>
              <div className="reason-bar-container">
                <div 
                  className="reason-bar"
                  style={{ width: `${(count / maxCount) * 100}%` }}
                />
              </div>
              <div className="reason-count">{count}</div>
            </div>
          ))
        ) : (
          <div className="no-flags">
            <span className="no-flags-icon">✓</span>
            <p>No flagged records</p>
          </div>
        )}
      </div>
    </div>
  );
}

export default FlaggedRecords;
