import React, { useState, useEffect } from 'react';
import { useParams, Link, useNavigate } from 'react-router-dom';
import axios from 'axios';
import RecordTable from '../components/RecordTable';
import './BatchDetail.css';

const API_BASE = `http://${window.location.hostname}:8000/api`;

function BatchDetail() {
  const { batchId } = useParams();
  const navigate = useNavigate();
  const [batch, setBatch] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [reviewNotes, setReviewNotes] = useState('');
  const [reviewerName, setReviewerName] = useState('');
  const [submitting, setSubmitting] = useState(false);

  useEffect(() => {
    fetchBatchDetails();
  }, [batchId]);

  const fetchBatchDetails = async () => {
    try {
      setLoading(true);
      const response = await axios.get(`${API_BASE}/ingestion/batches/${batchId}/records/`);
      setBatch(response.data);
      setError(null);
    } catch (err) {
      setError('Failed to load batch details');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleApprove = async () => {
    try {
      setSubmitting(true);
      await axios.post(`${API_BASE}/ingestion/batches/${batchId}/approve/`, {
        reviewed_by: reviewerName || 'Unknown',
        notes: reviewNotes
      }, {
        headers: { 'Content-Type': 'application/json' }
      });
      alert('Batch approved successfully');
      navigate('/');
    } catch (err) {
      alert('Failed to approve batch');
      console.error(err);
    } finally {
      setSubmitting(false);
    }
  };

  const handleReject = async () => {
    try {
      setSubmitting(true);
      await axios.post(`${API_BASE}/ingestion/batches/${batchId}/reject/`, {
        reviewed_by: reviewerName || 'Unknown',
        notes: reviewNotes
      }, {
        headers: { 'Content-Type': 'application/json' }
      });
      alert('Batch rejected');
      navigate('/');
    } catch (err) {
      alert('Failed to reject batch');
      console.error(err);
    } finally {
      setSubmitting(false);
    }
  };

  const handleReset = async () => {
    try {
      setSubmitting(true);
      const response = await axios.post(`${API_BASE}/ingestion/batches/${batchId}/reset/`, {}, {
        headers: { 'Content-Type': 'application/json' }
      });
      setBatch(response.data);
      setReviewNotes('');
      setReviewerName('');
      alert('Batch reset to pending. You can now review again.');
    } catch (err) {
      alert('Failed to reset batch');
      console.error(err);
    } finally {
      setSubmitting(false);
    }
  };

  if (loading) return <div className="loading">Loading batch details...</div>;
  if (error) return <div className="error">{error}</div>;
  if (!batch) return <div>No batch data</div>;

  return (
    <div className="batch-detail">
      <div className="detail-header">
        <Link to="/" className="back-btn">← Back</Link>
        <h2>Batch: {batch.batch_number}</h2>
        <span className={`status-badge status-${batch.status}`}>{batch.status}</span>
      </div>

      <div className="detail-content">
        <div className="records-section">
          {batch.sap_records && batch.sap_records.length > 0 && (
            <RecordTable 
              title="SAP Records" 
              records={batch.sap_records}
              type="sap"
            />
          )}
          {batch.utility_records && batch.utility_records.length > 0 && (
            <RecordTable 
              title="Utility Records" 
              records={batch.utility_records}
              type="utility"
            />
          )}
          {batch.travel_records && batch.travel_records.length > 0 && (
            <RecordTable 
              title="Travel Records" 
              records={batch.travel_records}
              type="travel"
            />
          )}
        </div>

        {batch.status === 'pending' && (
          <div className="review-section">
            <h3>Review & Approve</h3>
            <div className="form-group">
              <label>Reviewer Name</label>
              <input 
                type="text"
                value={reviewerName}
                onChange={(e) => setReviewerName(e.target.value)}
                placeholder="Your name"
              />
            </div>
            <div className="form-group">
              <label>Review Notes</label>
              <textarea 
                value={reviewNotes}
                onChange={(e) => setReviewNotes(e.target.value)}
                placeholder="Add any notes about this batch..."
                rows="4"
              />
            </div>
            <div className="action-buttons">
              <button 
                className="approve-btn"
                onClick={handleApprove}
                disabled={submitting}
              >
                {submitting ? 'Processing...' : 'Approve Batch'}
              </button>
              <button 
                className="reject-btn"
                onClick={handleReject}
                disabled={submitting}
              >
                {submitting ? 'Processing...' : 'Reject Batch'}
              </button>
            </div>
          </div>
        )}

        {(batch.status === 'approved' || batch.status === 'rejected') && (
          <div className="review-section">
            <h3>Batch Status: {batch.status.toUpperCase()}</h3>
            <p>Reviewed by: {batch.reviewed_by}</p>
            {batch.notes && <p>Notes: {batch.notes}</p>}
            <button 
              className="reset-btn"
              onClick={handleReset}
              disabled={submitting}
            >
              {submitting ? 'Processing...' : 'Reset to Pending'}
            </button>
          </div>
        )}
      </div>
    </div>
  );
}

export default BatchDetail;
