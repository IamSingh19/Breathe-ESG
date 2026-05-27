# Tradeoffs: What We Didn't Build

## 1. Edit History and Record Versioning

**What we didn't build**: The ability to edit records after they're ingested and keep track of what changed.

**Why**: It gets complicated fast. You'd need a whole history table, and then you have to decide: do we re-approve after someone edits? It's cleaner to just reject the batch and have them re-upload. That way the audit trail stays simple.

**What happens instead**:
- If a record is wrong, the analyst rejects the batch
- The data provider fixes the source file
- A new batch is uploaded
- The old batch stays in the database as rejected

**Cost of adding it later**: Moderate. We'd need to add a RecordHistory model and track changes. The API would need to expose edit endpoints.

**When we'd need it**: If analysts frequently need to make small corrections (typos, unit conversions) without re-uploading.

---

## 2. Multi-Tenancy

**What we didn't build**: Support for multiple clients in one system.

**Why**:
- Adds a `tenant_id` field to every model
- Requires filtering all queries by tenant
- Complicates testing and sample data
- The assignment doesn't mention multiple clients
- Single-client deployment is simpler

**What happens instead**:
- One database per client
- Or one database with all data mixed (not recommended)

**Cost of adding it later**: Moderate. We'd add `tenant_id` to IngestionBatch and filter all queries. The frontend would need a tenant selector.

**When we'd need it**: If Breathe wants to offer this as a SaaS product.

---

## 3. Emissions Calculation

**What we didn't build**: Automatic calculation of CO2 emissions from ingested data.

**Why**:
- Requires emission factors (kg CO2 per liter of fuel, per kWh, per km)
- Factors vary by region, fuel type, and electricity grid
- Calculation is complex (e.g., flight emissions depend on aircraft type, load factor, radiative forcing)
- The assignment asks for ingestion and review, not calculation
- Analysts might want to use their own emission factors

**What happens instead**:
- We ingest the raw data (fuel quantity, electricity consumption, distance)
- Analysts export the data and calculate emissions in Excel or their own system
- Or we add a separate emissions calculation service later

**Cost of adding it later**: High. We'd need to:
- Define emission factors for each fuel type, region, and travel mode
- Add a calculation engine
- Store calculated emissions in the database
- Expose them in the API and dashboard

**When we'd need it**: If the PM says "we need to show CO2 on the dashboard."

---

## Summary

These three features would add significant complexity without clear benefit for a prototype. They're all reasonable to add later if the PM asks for them. The current design prioritizes:
1. Getting data in
2. Letting analysts review it
3. Creating an audit trail

Calculation, versioning, and multi-tenancy are nice-to-haves, not must-haves for this phase.
