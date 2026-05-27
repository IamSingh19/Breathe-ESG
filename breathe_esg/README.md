# Breathe ESG - Data Ingestion & Review Platform

A Django REST + React application for ingesting, normalizing, and reviewing emissions data from multiple sources (SAP, utility providers, and corporate travel platforms).

## Architecture

### Backend (Django)
- **Data Models**: Separate models for SAP, utility, and travel records with built-in data quality flagging
- **Parsers**: CSV-based parsers for each data source with validation and anomaly detection
- **API**: REST endpoints for batch management, record retrieval, and dashboard analytics
- **Database**: SQLite (development), easily swappable for PostgreSQL

### Frontend (React)
- **Dashboard**: Real-time overview of ingestion status, record counts, and data quality metrics
- **Batch Management**: View, review, and approve/reject data batches
- **Record Tables**: Detailed views of SAP, utility, and travel records with flagging indicators

## Design Decisions

### Data Model
- **Separate record types** (SAPRecord, UtilityRecord, TravelRecord) instead of a generic record model because each source has fundamentally different fields and validation rules
- **IngestionBatch** tracks the lifecycle of data from upload through approval, enabling audit trails
- **Built-in flagging** at the model level for data quality issues (e.g., negative consumption, unrealistic distances)

### Parsers
- **CSV format** chosen for all sources because:
  - SAP: Most common export format for analysts
  - Utility: Portal exports are typically CSV
  - Travel: Corporate platforms export CSV
- **Multiple date format support** to handle regional variations (YYYY-MM-DD, DD.MM.YYYY, MM/DD/YYYY)
- **Validation at parse time** to catch issues early and provide meaningful error messages

### API Design
- **Batch-centric workflow**: Upload → Parse → Review → Approve/Reject
- **Separate endpoints** for each record type to allow filtering and analysis
- **Dashboard endpoint** provides aggregated metrics for the UI

### Frontend
- **Component-based architecture** for reusability and maintainability
- **Responsive design** that works on desktop and tablet
- **Sticky review panel** on batch detail page for efficient workflow

## Setup & Running

### Backend

1. **Create virtual environment**
   ```bash
   cd breathe_esg
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies**
   ```bash
   pip install django djangorestframework django-cors-headers python-dateutil openpyxl
   ```

3. **Run migrations**
   ```bash
   python manage.py migrate
   ```

4. **Load sample data**
   ```bash
   python manage.py load_sample_data
   ```

5. **Start server**
   ```bash
   python manage.py runserver
   ```

Server runs on `http://localhost:8000`

### Frontend

1. **Install dependencies**
   ```bash
   cd breathe-frontend
   npm install
   ```

2. **Start development server**
   ```bash
   npm start
   ```

Frontend runs on `http://localhost:3000`

## API Endpoints

### Ingestion
- `POST /api/ingestion/batches/upload/` - Upload and ingest data file
- `GET /api/ingestion/batches/` - List all batches
- `GET /api/ingestion/batches/{id}/records/` - Get all records in a batch
- `POST /api/ingestion/batches/{id}/approve/` - Approve a batch
- `POST /api/ingestion/batches/{id}/reject/` - Reject a batch

### Records
- `GET /api/ingestion/sap-records/` - List SAP records
- `GET /api/ingestion/utility-records/` - List utility records
- `GET /api/ingestion/travel-records/` - List travel records

### Dashboard
- `GET /api/review/dashboard/` - Get dashboard summary and metrics

## Data Quality Flags

The system automatically flags records for review:

**SAP Records**
- Quantity > 1,000,000 (unusually high fuel consumption)

**Utility Records**
- Billing start date >= billing end date
- Daily average consumption > 100,000 kWh

**Travel Records**
- Flight distance > 20,000 km
- Hotel check-in >= check-out date
- Cost > $10,000

## Sample Data

Sample CSV files are generated in the project root:
- `sample_sap.csv` - 50 SAP records
- `sample_utility.csv` - 30 utility records
- `sample_travel.csv` - 40 travel records

Generate new samples:
```bash
python generate_sample_data.py
```

## Testing the Flow

1. Start both backend and frontend servers
2. Navigate to `http://localhost:3000`
3. View the dashboard with sample data
4. Click "View" on a batch to see detailed records
5. Review and approve/reject batches
6. Check the dashboard to see updated status

## File Structure

```
breathe_esg/                    # Django backend
├── breathe/                    # Project settings
├── ingestion/                  # Data ingestion app
│   ├── models.py              # Data models
│   ├── parsers.py             # CSV parsers
│   ├── views.py               # API views
│   ├── serializers.py         # DRF serializers
│   └── urls.py                # URL routing
├── review/                     # Review dashboard app
│   ├── views.py               # Dashboard API
│   └── urls.py                # URL routing
├── manage.py
└── generate_sample_data.py    # Sample data generator

breathe-frontend/              # React frontend
├── src/
│   ├── components/            # Reusable components
│   ├── pages/                 # Page components
│   ├── App.js                 # Main app component
│   └── index.js               # Entry point
├── public/
│   └── index.html
└── package.json
```

## Future Enhancements

- PDF bill parsing for utility data
- OData API support for SAP
- User authentication and role-based access
- Batch scheduling and automated ingestion
- Export to audit-ready formats
- Historical trend analysis
