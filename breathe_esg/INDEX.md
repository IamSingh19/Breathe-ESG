# Breathe ESG - Complete Project Index

## 🎯 Start Here

**New to the project?** Read in this order:
1. **PROJECT_SUMMARY.md** - 5-minute overview
2. **QUICKSTART.md** - Get it running in 5 minutes
3. **DESIGN.md** - Understand the architecture

## 📋 Documentation

### Quick References
- **QUICKSTART.md** - Setup and run in 5 minutes
- **README.md** - Full project documentation
- **DESIGN.md** - Architecture and design decisions
- **TESTING.md** - Testing and deployment
- **PROJECT_SUMMARY.md** - Project overview
- **FILE_MANIFEST.md** - Complete file listing

### What Each Document Covers

| Document | Purpose | Read Time |
|----------|---------|-----------|
| QUICKSTART.md | Get running fast | 5 min |
| README.md | Full documentation | 15 min |
| DESIGN.md | Why decisions were made | 20 min |
| TESTING.md | Testing and deployment | 15 min |
| PROJECT_SUMMARY.md | Big picture overview | 10 min |
| FILE_MANIFEST.md | File structure | 5 min |

## 🏗️ Architecture

### Backend (Django)
```
breathe_esg/
├── ingestion/          # Data ingestion app
│   ├── models.py       # Data models
│   ├── parsers.py      # CSV parsers
│   ├── views.py        # API endpoints
│   └── serializers.py  # DRF serializers
├── review/             # Review dashboard app
│   └── views.py        # Dashboard API
└── manage.py           # Django CLI
```

### Frontend (React)
```
breathe-frontend/
├── src/
│   ├── components/     # Reusable components
│   ├── pages/          # Page components
│   ├── App.js          # Main app
│   └── index.js        # Entry point
└── package.json        # Dependencies
```

## 🚀 Quick Start

### Backend
```bash
cd breathe_esg
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install django djangorestframework django-cors-headers
python manage.py migrate
python manage.py load_sample_data
python manage.py runserver
```

### Frontend
```bash
cd breathe-frontend
npm install
npm start
```

### Access
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000/api/

## 📊 What's Included

### Data
- **50 SAP records** - Fuel and procurement data
- **30 Utility records** - Electricity consumption
- **40 Travel records** - Business travel expenses
- **3 Batches** - All in pending status, ready for review

### Features
- ✅ Data ingestion from CSV files
- ✅ Automatic data quality flagging
- ✅ Review dashboard with metrics
- ✅ Batch approval/rejection workflow
- ✅ Record tables with filtering
- ✅ Responsive design

### API Endpoints
- `GET /api/review/dashboard/` - Dashboard metrics
- `GET /api/ingestion/batches/` - List batches
- `GET /api/ingestion/batches/{id}/records/` - Get batch records
- `POST /api/ingestion/batches/{id}/approve/` - Approve batch
- `POST /api/ingestion/batches/{id}/reject/` - Reject batch
- `GET /api/ingestion/sap-records/` - SAP records
- `GET /api/ingestion/utility-records/` - Utility records
- `GET /api/ingestion/travel-records/` - Travel records

## 🔍 Key Features

### Data Quality
- Automatic flagging of suspicious records
- Multiple date format support
- Validation at parse time
- Clear error messages

### Workflow
1. Upload CSV file
2. System parses and validates
3. Analyst reviews in dashboard
4. Approve or reject batch
5. Approved data locked for audit

### Dashboard
- Real-time metrics
- Batch status overview
- Flagged records summary
- Recent batch list

## 📁 File Structure

### Backend Files
- `ingestion/models.py` - 163 lines
- `ingestion/parsers.py` - 436 lines
- `ingestion/views.py` - 173 lines
- `ingestion/serializers.py` - 52 lines
- `review/views.py` - 89 lines
- `generate_sample_data.py` - 126 lines
- `test_api.py` - 62 lines

### Frontend Files
- `App.js` - 82 lines
- `pages/Dashboard.js` - 91 lines
- `pages/BatchDetail.js` - 149 lines
- `components/StatCard.js` - 16 lines
- `components/BatchList.js` - 73 lines
- `components/RecordTable.js` - 110 lines
- `components/FlaggedRecords.js` - 28 lines

### Documentation
- README.md - 180 lines
- DESIGN.md - 253 lines
- TESTING.md - 247 lines
- QUICKSTART.md - 166 lines
- PROJECT_SUMMARY.md - 268 lines
- FILE_MANIFEST.md - 159 lines

## 🎓 Learning Path

### Understand the Data Model
1. Read `ingestion/models.py` - See what data is stored
2. Read `DESIGN.md` - Understand why it's structured this way
3. Check sample data - See realistic examples

### Understand the Data Flow
1. Read `ingestion/parsers.py` - How CSV is parsed
2. Read `ingestion/views.py` - How data is ingested
3. Read `review/views.py` - How data is displayed

### Understand the Frontend
1. Read `App.js` - Main app structure
2. Read `pages/Dashboard.js` - Dashboard layout
3. Read `components/` - Individual components

### Understand the API
1. Read `ingestion/serializers.py` - Data serialization
2. Read `ingestion/views.py` - API endpoints
3. Test with curl or Postman

## 🧪 Testing

### Run Tests
```bash
cd breathe_esg
python test_api.py
```

### Manual Testing
```bash
# Get dashboard data
curl http://localhost:8000/api/review/dashboard/

# List batches
curl http://localhost:8000/api/ingestion/batches/

# Get batch records
curl http://localhost:8000/api/ingestion/batches/1/records/
```

## 🚢 Deployment

See `TESTING.md` for:
- Production environment setup
- Database migration
- Static file collection
- Gunicorn configuration
- Security considerations

## ❓ FAQ

**Q: How do I add a new data source?**
A: Create a new model in `models.py`, a parser in `parsers.py`, and a viewset in `views.py`.

**Q: How do I change the data quality flags?**
A: Edit the flagging logic in `ingestion/parsers.py`.

**Q: How do I add authentication?**
A: Use Django-rest-auth or similar package. See `TESTING.md`.

**Q: How do I deploy to production?**
A: See `TESTING.md` for production deployment guide.

**Q: Can I use PostgreSQL instead of SQLite?**
A: Yes, update `DATABASES` in `settings.py`.

## 🎯 Design Principles

1. **Realistic** - Data models match actual business data
2. **Practical** - Validation based on real anomalies
3. **Workflow-Focused** - Architecture matches analyst workflow
4. **Minimal** - Only what's needed, no unnecessary abstractions
5. **Clear** - Design decisions are explicit and documented
6. **Honest** - Limitations are acknowledged

## 📞 Support

### If you have questions about...

**The data model** → Read `ingestion/models.py` and `DESIGN.md`

**How data is parsed** → Read `ingestion/parsers.py`

**The API** → Read `ingestion/views.py` and `review/views.py`

**The frontend** → Read `App.js` and `pages/`

**Design decisions** → Read `DESIGN.md`

**Getting started** → Read `QUICKSTART.md`

**Deployment** → Read `TESTING.md`

## ✅ Verification Checklist

- [x] Backend setup complete
- [x] Frontend setup complete
- [x] Database initialized
- [x] Sample data loaded
- [x] API endpoints tested
- [x] Dashboard working
- [x] Batch review working
- [x] Documentation complete

## 🎉 You're Ready!

1. Start the backend: `python manage.py runserver`
2. Start the frontend: `npm start`
3. Open http://localhost:3000
4. Review the sample data
5. Approve or reject batches
6. Explore the code

Enjoy!

---

**Project:** Breathe ESG Data Ingestion & Review Platform  
**Status:** Complete and tested  
**Ready for:** Review and deployment  
**Questions?** Check the documentation files above
