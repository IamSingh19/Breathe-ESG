# Data Sources: Research and Implementation

## 1. SAP Fuel and Procurement Data

### Real-World Format Research

SAP exports are a mess. They come in like three different formats:

**IDoc (Intermediate Document)**
- It's SAP's native format, kind of like XML
- Super complex, requires SAP knowledge
- Not practical for a prototype

**Flat File / CSV**
- This is what analysts actually use
- They run a report in SAP and export to Excel/CSV
- Way easier to work with

**OData API**
- RESTful API if you have S/4HANA
- Requires credentials and system access
- Overkill for a prototype

### What We Chose and Why

We chose **flat file CSV** because:
- It's what analysts actually use in practice
- No API credentials needed
- Easy to validate and test
- Portable for version control

### Sample Data

Our sample SAP data (`sample_sap.csv`):
```
plant_code,document_number,posting_date,fuel_type,quantity,unit
1000,SAP-2024-001,2024-01-15,Diesel,500,L
1000,SAP-2024-002,2024-01-16,Natural Gas,250,kg
1100,SAP-2024-003,2024-01-17,Petrol,300,L
```

**Why this structure**:
- Plant code: SAP's facility identifier (typically 4 digits)
- Document number: Unique transaction ID
- Posting date: When the transaction was recorded
- Fuel type: Diesel, Petrol, Natural Gas, etc.
- Quantity: Amount consumed
- Unit: L (liters), kg, m³, etc.

**Realistic values**:
- Plant codes are 4-digit numbers (1000-9999)
- Quantities range from 10 to 100,000 liters per transaction
- Dates are within the last 12 months
- Units vary by fuel type (liquid fuels in liters, gases in kg or m³)

### What Would Break in Production

1. **German column headers**: Some SAP systems export with German names (Menge, Einheit, Buchungsdatum)
   - Fix: Support multiple language headers

2. **Inconsistent date formats**: Different regions use DD.MM.YYYY vs MM/DD/YYYY
   - Fix: Try multiple date formats during parsing

3. **Missing plant codes**: Data references plants that don't exist in the system
   - Fix: Validate against a plant master table

4. **Negative quantities**: Data entry errors or reversals
   - Fix: Flag negative quantities, but allow them (they're legitimate reversals)

5. **Missing units**: Some exports omit the unit field
   - Fix: Assume default unit based on fuel type (L for liquids, kg for gases)

6. **Procurement data without emissions factors**: We ingest material codes but don't know their emissions
   - Fix: Require a material master table with emission factors

---

## 2. Utility Electricity Data

### Real-World Format Research

Utilities provide data in several ways:

**Portal CSV Export**
- Most common for commercial customers
- Utilities like Duke Energy, Con Edison, etc. offer portals
- Exports include: meter ID, billing period, consumption, charges
- Typically monthly data

**PDF Bills**
- Unstructured, requires OCR or manual parsing
- Contains consumption, charges, tariff info
- Hard to automate

**API Access**
- Some utilities offer APIs (e.g., Green Button standard)
- Requires authentication
- Real-time or near-real-time data
- Not universally available

### What We Chose and Why

We chose **portal CSV export** because:
- It's the most common format for facilities teams
- Easy to parse and validate
- No API authentication needed
- Standardized structure across utilities

### Sample Data

Our sample utility data (`sample_utility.csv`):
```
meter_id,facility_name,billing_start_date,billing_end_date,consumption_kwh,tariff_type,rate_per_kwh,total_charge
M-001,HQ Building,2024-01-01,2024-01-31,45000,Commercial,0.12,5400
M-002,Warehouse,2024-01-01,2024-01-31,120000,Industrial,0.08,9600
M-003,Office Park,2024-01-01,2024-01-31,35000,Commercial,0.13,4550
```

**Why this structure**:
- Meter ID: Unique identifier for each meter
- Facility name: Human-readable location
- Billing period: Start and end dates (typically monthly)
- Consumption: kWh (kilowatt-hours)
- Tariff type: Commercial, Industrial, Residential
- Rate: Price per kWh
- Total charge: Amount billed

**Realistic values**:
- Commercial buildings: 30,000-100,000 kWh/month
- Industrial facilities: 100,000-500,000 kWh/month
- Rates: $0.08-$0.15 per kWh (varies by region and tariff)
- Billing periods: Always start on the 1st, end on the last day of the month

### What Would Break in Production

1. **Billing periods that don't align with calendar months**
   - Some utilities bill on a 28-day cycle
   - Fix: Store actual billing period, not assume monthly

2. **Multiple tariff rates within one billing period**
   - Time-of-use rates (peak vs off-peak)
   - Seasonal rates
   - Fix: Store multiple rate records per meter per period

3. **Meter readings in different units**
   - Some utilities export in MWh instead of kWh
   - Fix: Normalize to kWh during parsing

4. **Missing consumption data**
   - Estimated bills (meter not read)
   - Fix: Flag estimated data, allow analyst to reject

5. **Demand charges**
   - Peak demand (kW) charged separately from consumption (kWh)
   - Fix: Add a demand_kw field

6. **Meter changes**
   - Old meter replaced with new meter mid-period
   - Fix: Track meter history

---

## 3. Corporate Travel Data

### Real-World Format Research

Corporate travel platforms provide data in several ways:

**Concur (SAP Concur)**
- Expense management platform
- Exports include: employee, trip date, origin, destination, cost, category
- Categories: Flight, Hotel, Ground Transport, Meals, etc.
- API available for real-time access

**Navan (formerly TripActions)**
- Modern travel management platform
- Similar structure to Concur
- Better data quality (auto-populated from booking)
- API available

**Direct CSV Export**
- Most platforms allow CSV export from reports
- Standardized format across platforms
- Includes all trip details

### What We Chose and Why

We chose **CSV export** because:
- Works with any platform (Concur, Navan, etc.)
- No API authentication needed
- Easy to test with sample data
- Analyst has control over what data is exported

### Sample Data

Our sample travel data (`sample_travel.csv`):
```
travel_type,employee_id,trip_date,origin,destination,distance_km,flight_class,cost
flight,EMP-001,2024-01-10,SFO,NYC,4130,Economy,450
hotel,EMP-001,2024-01-10,NYC,NYC,0,N/A,200
ground,EMP-001,2024-01-12,NYC,SFO,0,N/A,75
flight,EMP-002,2024-01-15,LAX,ORD,2015,Business,1200
hotel,EMP-002,2024-01-15,ORD,ORD,0,N/A,350
```

**Why this structure**:
- Travel type: Flight, Hotel, Ground (taxi, rental car, etc.)
- Employee ID: Who traveled
- Trip date: When the trip started
- Origin/Destination: Airport codes or city names
- Distance: For flights (km), for ground transport (miles)
- Flight class: Economy, Business, First (flights only)
- Cost: Amount charged

**Realistic values**:
- Flight distances: 500-15,000 km (domestic to international)
- Flight costs: $200-$2,000 (economy to business class)
- Hotel costs: $100-$500/night
- Ground transport: $20-$100
- Employee IDs: EMP-001, EMP-002, etc.

### What Would Break in Production

1. **Airport codes without distance data**
   - Some platforms only export airport codes, not distance
   - Fix: Maintain an airport distance lookup table

2. **Multi-leg flights**
   - A trip from SFO to NYC via Chicago is three legs
   - We treat each leg as one record
   - Fix: Group legs by trip ID

3. **Hotel chains with multiple locations**
   - "Marriott" doesn't tell us which city
   - Fix: Require full hotel name or city

4. **Ground transport without distance**
   - Taxi rides don't have distance data
   - Fix: Geocode origin/destination to calculate distance

5. **Cancelled trips**
   - Trip was booked but cancelled
   - We don't track cancellations
   - Fix: Add a status field (booked, cancelled, completed)

6. **Personal vs business travel**
   - Some platforms mix personal and business
   - Fix: Add a trip_type field or filter by cost center

7. **Mileage reimbursement**
   - Personal car mileage for business purposes
   - Different emission factor than commercial flights
   - Fix: Add a vehicle_type field for ground transport

---

## Summary: What We Learned

### SAP
- Real-world SAP data is messy (multiple formats, languages, units)
- CSV is the practical choice for a prototype
- Procurement data is harder than fuel (need material master)

### Utility
- Billing periods are the key unit, not calendar months
- Tariff structures are complex (time-of-use, seasonal, demand charges)
- Meter readings can be estimated or missing

### Travel
- Distance data is often missing (need lookup tables)
- Multi-leg trips need special handling
- Personal vs business distinction is important

### General
- All three sources have data quality issues
- Flagging heuristics are essential
- Analyst review is non-negotiable
