import React from 'react';
import { Link } from 'react-router-dom';
import './BatchList.css';

function BatchList({ batches }) {
  const getStatusIcon = (status) => {
    switch (status) {
      case 'pending':
        return '⏳';
      case 'approved':
        return '✓';
      case 'rejected':
        return '✕';
      default:
        return '•';
    }
  };

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      month: 'short',
      day: 'numeric',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  const getSourceIcon = (type) => {
    switch (type) {
      case 'sap':
        return '🏢';
      case 'utility':
        return '⚡';
      case 'travel':
        return '✈️';
      default:
        return '📦';
    }
  };

  return (
    <div className="batch-list">
      <div className="batch-list-header">
        <h3>Recent Batches</h3>
        <span className="batch-count">{batches.length} batches</span>
      </div>
      <div className="batch-table">
        <div className="batch-header">
          <div className="col-batch">Batch ID</div>
          <div className="col-source">Source</div>
          <div className="col-records">Records</div>
          <div className="col-flagged">Flagged</div>
          <div className="col-status">Status</div>
          <div className="col-date">Uploaded</div>
          <div className="col-action">Action</div>
        </div>
        {batches.map((batch) => (
          <div key={batch.id} className="batch-row">
            <div className="col-batch">
              <span className="batch-id-text">{batch.batch_id}</span>
            </div>
            <div className="col-source">
              <span className="source-badge">
                <span className="source-icon">{getSourceIcon(batch.source_type)}</span>
                {batch.source_type.toUpperCase()}
              </span>
            </div>
            <div className="col-records">
              <span className="record-count">{batch.sap_count + batch.utility_count + batch.travel_count}</span>
            </div>
            <div className="col-flagged">
              <span className={`flag-count ${batch.flagged_count > 0 ? 'has-flags' : ''}`}>
                {batch.flagged_count}
              </span>
            </div>
            <div className="col-status">
              <span 
                className={`status-badge status-${batch.status}`}
              >
                <span className="status-icon">{getStatusIcon(batch.status)}</span>
                {batch.status.charAt(0).toUpperCase() + batch.status.slice(1)}
              </span>
            </div>
            <div className="col-date">
              <span className="date-text">{formatDate(batch.uploaded_at)}</span>
            </div>
            <div className="col-action">
              <Link to={`/batch/${batch.id}`} className="view-btn">
                View Details
              </Link>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default BatchList;
