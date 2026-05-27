# Design Decisions

## Data Source Formats

### SAP: Flat File CSV

**What we chose**: CSV export format

**Why**: SAP can export in like three different ways (IDoc XML, OData API, flat file). I went with flat file CSV because that's what actually happens in the real world. Analysts export from SAP and get a CSV. It's simple, no API keys needed, and easy to test.

**What we ignored**: 
- IDoc format (too complex for a prototype)
- OData API (requires SAP system access and authentication)
- Real-time sync (out of scope for batch-based review)

**Sample data structure**:
```
plant_code,document_number,posting_date,fuel_type,quantity,unit
1000,SAP-2024-001,2024-01-15,Diesel,500,L
1000,SAP-2024-002,2024-01-16,Natural Gas,250,kg
```

**What would break in production**:
- German column headers (some SAP systems export with German names)
- Inconsistent date formats across regions
- Plant codes that don't exist in the lookup table
- Missing units (some exports omit this)
- Negative quantities (data entry errors)

### Utility: Portal CSV Export

**What we chose**: CSV export from utility portal
**Why**:
- Most facilities teams get bills as PDFs or portal exports
- CSV is easier to parse than PDF
- It's what the sample data represents
- API access varies by utility and region

**What we ignored**:
- PDF parsing (complex, error-prone)
- Direct utility API (varies by provider)
- Real-time meter readings (not typical for billing data)

**Sample data structure**:
```
meter_id,facility_name,billing_start_date,billing_end_date,consumption_kwh,tariff_type,rate_per_kwh,total_charge
M-001,HQ Building,2024-01-01,2024-01-31,45000,Commercial,0.12,5400
M-002,Warehouse,2024-01-01,2024-01-31,120000,Industrial,0.08,9600
```

**What would break in production**:
- Billing periods that don't align with calendar months
- Multiple tariff rates within one billing period
- Meter readings in different units (kWh vs MWh)
- Missing consumption data (estimated bills)
- Demand charges (we only track consumption)

### Travel: Corporate Platform CSV Export

**What we chose**: CSV export from corporate travel platform
**Why**:
- Concur, Navan, and similar platforms export to CSV
- It's standardized across platforms
- It includes all three travel types (flight, hotel, ground)
- No API authentication needed

**What we ignored**:
- Real-time API sync
- Expense report integration
- Per-diem calculations
- Mileage reimbursement rules

**Sample data structure**:
```
travel_type,employee_id,trip_date,origin,destination,distance_km,flight_class,cost
flight,EMP-001,2024-01-10,SFO,NYC,4130,Economy,450
hotel,EMP-001,2024-01-10,NYC,NYC,0,N/A,200
ground,EMP-001,2024-01-12,NYC,SFO,0,N/A,75
```

**What would break in production**:
- Airport codes without distance data (we'd need a lookup table)
- Multi-leg flights (we treat each leg as one record)
- Hotel chains with multiple locations (ambiguous destination)
- Ground transport without distance (we'd need to geocode)
- Cancelled trips (we don't track cancellations)

## Ingestion Mechanism

**What we chose**: File upload via REST API
**Why**:
- Simple to implement
- Works for all three sources
- Analyst has control over when data is ingested
- Easy to test with sample files

**What we ignored**:
- Scheduled/automated ingestion
- Real-time streaming
- Direct database inserts
- Email-based uploads

## Batch Workflow

**What we chose**: Upload → Parse → Review → Approve/Reject
**Why**:
- Clear, linear workflow
- Analyst can see what came in before approving
- Audit trail is built in
- Easy to reject and re-upload if needed

**What we ignored**:
- Partial approvals (approve some records, reject others)
- Editing records before approval
- Rollback after approval
- Scheduled approvals

## Data Quality Flagging

**What we chose**: Heuristic-based flagging at parse time
**Why**:
- Catches obvious errors early
- Analyst can see flags before approving
- Rules are simple and transparent
- Easy to adjust thresholds

**What we ignored**:
- Machine learning-based anomaly detection
- Cross-batch comparisons (e.g., "this is 10x higher than last month")
- Duplicate detection
- Outlier analysis

**Thresholds chosen**:
- SAP fuel: > 1M liters (seems unrealistic for one transaction)
- Utility: > 100k kWh/day (seems unrealistic for most facilities)
- Travel: > 20k km (around the Earth's circumference)
- Travel cost: > $10k (unusually expensive)

These are conservative. We'd ask the PM: what's realistic for your clients?

## Currency Handling

**What we chose**: Store currency code, don't convert
**Why**:
- Preserves source data
- Avoids exchange rate complexity
- Analyst can see original currency
- Conversion happens at reporting time

**What we ignored**:
- Automatic currency conversion
- Exchange rate tracking
- Multi-currency consolidation

## Scope Categorization

**What we chose**: Derive from record type, not store explicitly
**Why**:
- Simpler model
- Easier to change rules later
- Avoids duplication

**Mapping**:
- SAP fuel → Scope 1
- Utility electricity → Scope 2
- Travel → Scope 3

**What we ignored**:
- Scope 1 vs 2 for procurement (we treat all procurement as Scope 3)
- Biogenic emissions (we don't distinguish)
- Avoided emissions (we don't track)

## Questions for the PM

1. **Multi-tenancy**: Should we support multiple clients in one system, or is this single-client?
2. **Edit history**: If an analyst corrects a record, should we keep the original value?
3. **Partial approvals**: Can an analyst approve some records in a batch and reject others?
4. **Data retention**: How long do we keep rejected batches?
5. **Scope 1 vs 2**: How do we categorize procurement? Is it always Scope 3?
6. **Procurement emissions**: Do we need to calculate emissions from procurement data, or just ingest it?
7. **Travel distance**: If we don't have distance, should we calculate it from airport codes?
8. **Utility demand charges**: Should we track peak demand separately from consumption?
9. **Billing period alignment**: Should we normalize utility data to calendar months?
10. **Audit export**: What format do auditors expect? CSV, PDF, JSON?

## What We Didn't Build

See TRADEOFFS.md for three major features we deliberately skipped.
