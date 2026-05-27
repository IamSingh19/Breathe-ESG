# Quick Start Guide

## 5-Minute Setup

### Backend

```bash
cd breathe_esg

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install django djangorestframework django-cors-headers python-dateutil

# Set up database
python manage.py migrate
python manage.py load_sample_data

# Start server
python manage.py runserver
```

Backend runs on `http://localhost:8000`

### Frontend

```bash
cd breathe-frontend

# Install dependencies
npm install

# Start development server
npm start
```

Frontend runs on `http://localhost:3000`

## What You Get

- **Dashboard:** Overview of all ingested data with stats and recent batches
- **Batch Review:** Detailed view of records with flagging indicators
- **Approval Workflow:** Review and approve/reject batches before audit
- **Sample Data:** 120 records across 3 batches ready to explore

## Key Features

### Data Ingestion
- Upload CSV files from SAP, utilities, or travel platforms
- Automatic parsing and validation
- Data quality flagging for suspicious records

### Review Dashboard
- Real-time metrics on ingestion status
- Batch list with status indicators
- Flagged records summary by reason

### Batch Management
- View all records in a batch
- Approve or reject batches
- Add reviewer notes
- Track approval history

## API Endpoints

```
GET  /api/review/dashboard/              # Dashboard metrics
GET  /api/ingestion/batches/              # List batches
GET  /api/ingestion/batches/{id}/records/ # Get batch records
POST /api/ingestion/batches/{id}/approve/ # Approve batch
POST /api/ingestion/batches/{id}/reject/  # Reject batch
GET  /api/ingestion/sap-records/          # List SAP records
GET  /api/ingestion/utility-records/      # List utility records
GET  /api/ingestion/travel-records/       # List travel records
```

## Sample Data

Three batches are pre-loaded:
- **sap_sample_001:** 50 SAP records (fuel and procurement)
- **utility_sample_001:** 30 utility records (electricity consumption)
- **travel_sample_001:** 40 travel records (flights, hotels, ground transport)

All batches are in "pending" status and ready for review.

## Next Steps

1. **Explore the Dashboard**
   - View overall statistics
   - See recent batches

2. **Review a Batch**
   - Click "View" on any batch
   - Examine records and flags
   - Approve or reject

3. **Upload New Data**
   - Generate new sample data: `python generate_sample_data.py`
   - Upload via API or create new batches

4. **Customize**
   - Modify data quality flags in `ingestion/parsers.py`
   - Add new record types in `ingestion/models.py`
   - Extend dashboard in `review/views.py`

## Troubleshooting

**Backend won't start:**
```bash
# Check if port 8000 is in use
python manage.py runserver 8001
```

**Frontend won't connect to backend:**
- Verify backend is running on port 8000
- Check CORS settings in `breathe/settings.py`

**No data showing:**
```bash
python manage.py load_sample_data
```

**Database errors:**
```bash
python manage.py migrate
```

## Project Structure

```
breathe_esg/                    # Django backend
├── ingestion/                  # Data ingestion app
│   ├── models.py              # Data models
│   ├── parsers.py             # CSV parsers
│   ├── views.py               # API views
│   └── serializers.py         # DRF serializers
├── review/                     # Review dashboard app
│   └── views.py               # Dashboard API
├── manage.py
└── README.md

breathe-frontend/              # React frontend
├── src/
│   ├── components/            # Reusable components
│   ├── pages/                 # Page components
│   └── App.js                 # Main app
└── package.json
```

## Documentation

- **README.md** - Full project overview and setup
- **DESIGN.md** - Architecture and design decisions
- **TESTING.md** - Testing and deployment guide

## Support

For issues or questions:
1. Check the documentation files
2. Review the code comments
3. Check Django and React documentation
4. Examine the sample data format

Happy reviewing!
