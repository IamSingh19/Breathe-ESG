import React, { useState } from 'react';
import './RecordTable.css';

function RecordTable({ title, records, type }) {
  const [expandedId, setExpandedId] = useState(null);

  const renderSAPRow = (record) => (
    <>
      <div className="col-doc">{record.document_number}</div>
      <div className="col-type">{record.record_type}</div>
      <div className="col-value">
        {record.fuel_type || record.material_code}
      </div>
      <div className="col-qty">
        {record.quantity || record.amount}
      </div>
      <div className="col-flag">
        {record.is_flagged && <span className="flag-badge">{record.flag_reason}</span>}
      </div>
    </>
  );

  const renderUtilityRow = (record) => (
    <>
      <div className="col-meter">{record.meter_id}</div>
      <div className="col-facility">{record.facility_name}</div>
      <div className="col-consumption">{record.consumption_kwh} kWh</div>
      <div className="col-charge">${record.total_charge}</div>
      <div className="col-flag">
        {record.is_flagged && <span className="flag-badge">{record.flag_reason}</span>}
      </div>
    </>
  );

  const renderTravelRow = (record) => (
    <>
      <div className="col-type">{record.travel_type}</div>
      <div className="col-route">{record.origin} → {record.destination}</div>
      <div className="col-date">{new Date(record.trip_date).toLocaleDateString()}</div>
      <div className="col-cost">${record.cost}</div>
      <div className="col-flag">
        {record.is_flagged && <span className="flag-badge">{record.flag_reason}</span>}
      </div>
    </>
  );

  const renderRow = (record) => {
    switch (type) {
      case 'sap':
        return renderSAPRow(record);
      case 'utility':
        return renderUtilityRow(record);
      case 'travel':
        return renderTravelRow(record);
      default:
        return null;
    }
  };

  return (
    <div className="record-table">
      <h3>{title}</h3>
      <div className="table-wrapper">
        <div className="table-header">
          {type === 'sap' && (
            <>
              <div className="col-doc">Document</div>
              <div className="col-type">Type</div>
              <div className="col-value">Fuel/Material</div>
              <div className="col-qty">Qty/Amount</div>
              <div className="col-flag">Flags</div>
            </>
          )}
          {type === 'utility' && (
            <>
              <div className="col-meter">Meter ID</div>
              <div className="col-facility">Facility</div>
              <div className="col-consumption">Consumption</div>
              <div className="col-charge">Charge</div>
              <div className="col-flag">Flags</div>
            </>
          )}
          {type === 'travel' && (
            <>
              <div className="col-type">Type</div>
              <div className="col-route">Route</div>
              <div className="col-date">Date</div>
              <div className="col-cost">Cost</div>
              <div className="col-flag">Flags</div>
            </>
          )}
        </div>
        {records.map((record) => (
          <div 
            key={record.id} 
            className={`table-row ${record.is_flagged ? 'flagged' : ''}`}
            onClick={() => setExpandedId(expandedId === record.id ? null : record.id)}
          >
            {renderRow(record)}
          </div>
        ))}
      </div>
      <div className="table-footer">
        {records.length} records ({records.filter(r => r.is_flagged).length} flagged)
      </div>
    </div>
  );
}

export default RecordTable;
