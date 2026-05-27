# Testing & Deployment Guide

## Backend Testing

### 1. Database Verification
```bash
cd breathe_esg
python -c "
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'breathe.settings')
import django
django.setup()

from ingestion.models import SAPRecord, UtilityRecord, TravelRecord
print(f'SAP Records: {SAPRecord.objects.count()}')
print(f'Utility Records: {UtilityRecord.objects.count()}')
print(f'Travel Records: {TravelRecord.objects.count()}')
"
```

### 2. API Endpoint Testing
```bash
python test_api.py
```

This tests all endpoints:
- Dashboard summary
- Batch list
- SAP records
- Utility records
- Travel records

### 3. Manual API Testing with curl

**Get dashboard data:**
```bash
curl http://localhost:8000/api/review/dashboard/
```

**List batches:**
```bash
curl http://localhost:8000/api/ingestion/batches/
```

**Get batch details:**
```bash
curl http://localhost:8000/api/ingestion/batches/1/records/
```

**Approve a batch:**
```bash
curl -X POST http://localhost:8000/api/ingestion/batches/1/approve/ \
  -H "Content-Type: application/json" \
  -d '{"reviewed_by": "John Doe", "notes": "Data looks good"}'
```

## Frontend Testing

### 1. Component Rendering
- Dashboard loads with stats cards
- Batch list displays all batches
- Flagged records summary shows issues
- Batch detail page shows all record types

### 2. User Interactions
- Click "View" on a batch → navigates to detail page
- Click "Back" → returns to dashboard
- Fill review form and click "Approve" → batch status changes
- Click "Reject" → batch is rejected

### 3. Data Display
- Stats cards show correct counts
- Record tables display data with proper formatting
- Flagged records are highlighted in yellow
- Status badges show correct colors

## End-to-End Flow

1. **Start Backend**
   ```bash
   cd breathe_esg
   python manage.py runserver
   ```

2. **Start Frontend**
   ```bash
   cd breathe-frontend
   npm install
   npm start
   ```

3. **Test Flow**
   - Open http://localhost:3000
   - View dashboard with sample data
   - Click "View" on a batch
   - Review records and approve/reject
   - Return to dashboard and verify status changed

## Data Quality Validation

The system automatically flags records for review. Check flagged records:

```bash
python -c "
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'breathe.settings')
import django
django.setup()

from ingestion.models import SAPRecord, UtilityRecord, TravelRecord

print('Flagged SAP Records:')
for r in SAPRecord.objects.filter(is_flagged=True):
    print(f'  {r.document_number}: {r.flag_reason}')

print('\nFlagged Utility Records:')
for r in UtilityRecord.objects.filter(is_flagged=True):
    print(f'  {r.meter_id}: {r.flag_reason}')

print('\nFlagged Travel Records:')
for r in TravelRecord.objects.filter(is_flagged=True):
    print(f'  {r.employee_id}: {r.flag_reason}')
"
```

## Uploading New Data

### 1. Create CSV File
Format depends on source type:

**SAP (sample_sap.csv):**
```
plant_code,document_number,posting_date,fuel_type,quantity,unit,material_code,material_description,amount,currency
PLANT001,DOC1000001,2024-01-15,Diesel,1000,L,,,USD
```

**Utility (sample_utility.csv):**
```
meter_id,facility_name,billing_start_date,billing_end_date,consumption_kwh,tariff_type,rate_per_kwh,total_charge,currency
METER001,HQ Building,2024-01-01,2024-01-31,15000,Commercial,0.12,1800,USD
```

**Travel (sample_travel.csv):**
```
travel_type,employee_id,trip_date,origin,destination,distance_km,flight_class,check_in_date,check_out_date,nights,vehicle_type,distance_miles,cost,currency
flight,EMP001,2024-01-15,New York,Los Angeles,2800,Business,,,,,1200,USD
```

### 2. Upload via API
```bash
curl -X POST http://localhost:8000/api/ingestion/batches/upload/ \
  -F "source_id=1" \
  -F "file=@sample_sap.csv"
```

### 3. View in Dashboard
- Refresh dashboard
- New batch appears in "Recent Batches"
- Records are counted and flagged

## Production Deployment

### 1. Environment Setup
```bash
# Create .env file
DEBUG=False
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DATABASE_URL=postgresql://user:password@localhost/breathe_esg
```

### 2. Database Migration
```bash
python manage.py migrate --settings=breathe.settings_production
```

### 3. Static Files
```bash
python manage.py collectstatic --settings=breathe.settings_production
```

### 4. Run with Gunicorn
```bash
gunicorn breathe.wsgi:application --bind 0.0.0.0:8000
```

### 5. Frontend Build
```bash
cd breathe-frontend
npm run build
# Serve build/ directory with nginx or similar
```

## Troubleshooting

### Backend Issues

**Port already in use:**
```bash
python manage.py runserver 8001
```

**Database errors:**
```bash
python manage.py migrate
python manage.py load_sample_data
```

**CORS errors:**
Check CORS_ALLOWED_ORIGINS in settings.py

### Frontend Issues

**API not responding:**
- Verify backend is running on port 8000
- Check API_BASE in App.js

**Blank dashboard:**
- Check browser console for errors
- Verify backend has sample data loaded

**Styling issues:**
- Clear browser cache
- Rebuild frontend: `npm run build`

## Performance Optimization

### Backend
- Add database indexes on frequently queried fields
- Use pagination for large record sets (already implemented)
- Cache dashboard data with Redis

### Frontend
- Lazy load record tables
- Implement virtual scrolling for large lists
- Use React.memo for components

## Security Considerations

- [ ] Add user authentication
- [ ] Implement role-based access control
- [ ] Add CSRF protection
- [ ] Validate file uploads
- [ ] Sanitize user input
- [ ] Use HTTPS in production
- [ ] Add rate limiting
- [ ] Implement audit logging
