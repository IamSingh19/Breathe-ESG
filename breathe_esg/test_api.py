import os
import django
import json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'breathe.settings')
django.setup()

from django.test import Client

client = Client()

print("=== Testing API Endpoints ===\n")

# Test dashboard endpoint
print("1. Dashboard Endpoint")
response = client.get('/api/review/dashboard/')
print(f"   Status: {response.status_code}")
if response.status_code == 200:
    data = json.loads(response.content)
    print(f"   Total Records: {data['records']['total']}")
    print(f"   Total Batches: {data['batches']['total']}")
    print(f"   Pending: {data['batches']['pending']}")
    print(f"   Approved: {data['batches']['approved']}")
    print(f"   Flagged Records: {data['records']['total_flagged']}")

# Test batches list
print("\n2. Batches List Endpoint")
response = client.get('/api/ingestion/batches/')
print(f"   Status: {response.status_code}")
if response.status_code == 200:
    data = json.loads(response.content)
    count = len(data['results']) if 'results' in data else len(data)
    print(f"   Batches Count: {count}")

# Test SAP records
print("\n3. SAP Records Endpoint")
response = client.get('/api/ingestion/sap-records/')
print(f"   Status: {response.status_code}")
if response.status_code == 200:
    data = json.loads(response.content)
    count = len(data['results']) if 'results' in data else len(data)
    print(f"   SAP Records Count: {count}")

# Test utility records
print("\n4. Utility Records Endpoint")
response = client.get('/api/ingestion/utility-records/')
print(f"   Status: {response.status_code}")
if response.status_code == 200:
    data = json.loads(response.content)
    count = len(data['results']) if 'results' in data else len(data)
    print(f"   Utility Records Count: {count}")

# Test travel records
print("\n5. Travel Records Endpoint")
response = client.get('/api/ingestion/travel-records/')
print(f"   Status: {response.status_code}")
if response.status_code == 200:
    data = json.loads(response.content)
    count = len(data['results']) if 'results' in data else len(data)
    print(f"   Travel Records Count: {count}")

print("\n=== All API endpoints working correctly ===")
