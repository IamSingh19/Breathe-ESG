# Data Model

## Overview

So the basic idea is: we have data coming in from three different places (SAP, utilities, travel platforms), and each one looks completely different. Instead of trying to force them into one generic "record" table, I made separate models for each. It's cleaner that way.

## Core Models

### DataSource
Represents where data comes from. Tracks the source type (SAP, Utility, or Travel) and when it was registered.

```
DataSource
├── name: string
├── source_type: choice (sap, utility, travel)
└── created_at: timestamp
```

Why separate? Because we might ingest from multiple SAP systems, multiple utility providers, or multiple travel platforms. This lets us track which system each batch came from.

### IngestionBatch
Tracks a batch of data from upload through approval. This is the audit trail.

```
IngestionBatch
├── source: FK → DataSource
├── batch_id: string (unique)
├── status: choice (pending, approved, rejected)
├── uploaded_at: timestamp
├── reviewed_at: timestamp (nullable)
├── reviewed_by: string (nullable)
├── notes: text
└── relationships:
    ├── sap_records (reverse FK)
    ├── utility_records (reverse FK)
    └── travel_records (reverse FK)
```

Why this structure? It creates a clear audit trail: who uploaded what, when it was reviewed, and what decision was made. The batch ID is unique so we can reference it in external systems.

## Record Models

### SAPRecord
Fuel and procurement data from SAP exports.

```
SAPRecord
├── batch: FK → IngestionBatch
├── record_type: choice (fuel, procurement)
├── plant_code: string
├── document_number: string
├── posting_date: date
├── fuel_type: string (nullable, fuel only)
├── quantity: decimal (nullable, fuel only)
├── unit: string (nullable, fuel only)
├── material_code: string (nullable, procurement only)
├── material_description: string (nullable, procurement only)
├── amount: decimal (nullable, procurement only)
├── currency: string (default USD)
├── is_flagged: boolean
├── flag_reason: string
└── created_at: timestamp
```

Why two record types in one model? Because they share common fields (plant code, document number, date) but have different specific fields. Combining them avoids duplication while keeping the distinction clear.

### UtilityRecord
Electricity consumption from utility providers.

```
UtilityRecord
├── batch: FK → IngestionBatch
├── meter_id: string
├── facility_name: string
├── billing_start_date: date
├── billing_end_date: date
├── consumption_kwh: decimal (non-negative)
├── tariff_type: string (nullable)
├── rate_per_kwh: decimal (nullable)
├── total_charge: decimal
├── currency: string (default USD)
├── is_flagged: boolean
├── flag_reason: string
└── created_at: timestamp
```

Why separate from SAP? Utility data has a completely different structure. It's billing-period-based, not transaction-based. Mixing it with SAP would create a confusing model.

### TravelRecord
Business travel from corporate travel platforms.

```
TravelRecord
├── batch: FK → IngestionBatch
├── travel_type: choice (flight, hotel, ground)
├── employee_id: string
├── trip_date: date
├── origin: string
├── destination: string
├── distance_km: integer (nullable, flight only)
├── flight_class: string (nullable, flight only)
├── check_in_date: date (nullable, hotel only)
├── check_out_date: date (nullable, hotel only)
├── nights: integer (nullable, hotel only)
├── vehicle_type: string (nullable, ground only)
├── distance_miles: decimal (nullable, ground only)
├── cost: decimal
├── currency: string (default USD)
├── is_flagged: boolean
├── flag_reason: string
└── created_at: timestamp
```

Why three travel types in one model? Same reason as SAP: they share employee ID, trip date, origin/destination, and cost, but have different specific fields. Separating them would create unnecessary duplication.

## Scope Categorization

The model doesn't explicitly store Scope 1/2/3 categorization because it's derived from the record type and source:

- **Scope 1 (Direct)**: SAP fuel records
- **Scope 2 (Indirect - Energy)**: Utility electricity records
- **Scope 3 (Indirect - Other)**: Travel records

This is calculated at query time in the dashboard, not stored. It keeps the model simpler and makes it easier to change categorization rules later.

## Unit Normalization

Units are stored as-is from the source (liters, kg, kWh, miles, km) because:
1. We need to preserve what the source said for audit purposes
2. Conversion factors vary by context (fuel density depends on fuel type)
3. The analyst can see the original unit and flag if it looks wrong

Normalization happens in the review dashboard, not in the model.

## Data Quality Flagging

Each record has `is_flagged` and `flag_reason` fields. Flags are set during parsing based on heuristics:

**SAP Records**
- Quantity > 1,000,000 liters (unusually high fuel consumption in one transaction)

**Utility Records**
- Billing start date >= billing end date (impossible billing period)
- Daily average consumption > 100,000 kWh (unrealistic for most facilities)

**Travel Records**
- Flight distance > 20,000 km (unusually long)
- Hotel check-in >= check-out date (impossible stay)
- Cost > $10,000 (unusually expensive)

These are heuristics, not hard rules. An analyst might approve a flagged record if it's legitimate.

## Audit Trail

The model supports audit trails through:
1. **IngestionBatch**: Tracks who reviewed and when
2. **created_at on each record**: When it was ingested
3. **batch relationship**: Which batch it came from

What's missing: We don't track edits to records after ingestion. If an analyst corrects a record, we don't store the original value. This is a deliberate tradeoff (see TRADEOFFS.md).

## Multi-Tenancy

The current model doesn't support multi-tenancy. All data is in one database. To add it, we'd add a `tenant_id` field to IngestionBatch and filter all queries by tenant. This is a deliberate limitation (see DECISIONS.md).

## Relationships

```
DataSource
    ↓
IngestionBatch
    ├→ SAPRecord
    ├→ UtilityRecord
    └→ TravelRecord
```

All records point back to their batch, which points to its source. This makes it easy to trace any record back to where it came from.

## Why This Design

1. **Separate record types** prevent mixing incompatible fields and make validation clear
2. **Batch-centric** creates a natural audit trail and approval workflow
3. **Flagging at the model level** means data quality is built in, not bolted on
4. **Minimal normalization** preserves source data for audit purposes
5. **Simple relationships** make queries fast and easy to understand
