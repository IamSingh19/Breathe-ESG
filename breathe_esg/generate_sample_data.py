import csv
import random
from datetime import datetime, timedelta
from pathlib import Path


class SampleDataGenerator:
    """Generate realistic sample data for testing"""
    
    @staticmethod
    def generate_sap_data(filename='sample_sap.csv', num_records=50):
        """Generate sample SAP data"""
        fuel_types = ['Diesel', 'Petrol', 'Natural Gas', 'LPG']
        units = ['L', 'kg', 'm3']
        plant_codes = ['PLANT001', 'PLANT002', 'PLANT003', 'PLANT004']
        
        with open(filename, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=[
                'plant_code', 'document_number', 'posting_date',
                'fuel_type', 'quantity', 'unit',
                'material_code', 'material_description', 'amount', 'currency'
            ])
            writer.writeheader()
            
            for i in range(num_records):
                is_fuel = random.choice([True, False])
                posting_date = datetime.now() - timedelta(days=random.randint(1, 90))
                
                row = {
                    'plant_code': random.choice(plant_codes),
                    'document_number': f"DOC{1000000 + i}",
                    'posting_date': posting_date.strftime('%Y-%m-%d'),
                    'fuel_type': random.choice(fuel_types) if is_fuel else '',
                    'quantity': random.randint(100, 5000) if is_fuel else '',
                    'unit': random.choice(units) if is_fuel else '',
                    'material_code': f"MAT{100000 + i}" if not is_fuel else '',
                    'material_description': f"Material {i}" if not is_fuel else '',
                    'amount': random.randint(1000, 50000) if not is_fuel else '',
                    'currency': 'USD',
                }
                writer.writerow(row)
        
        print(f"Generated {filename} with {num_records} records")
    
    @staticmethod
    def generate_utility_data(filename='sample_utility.csv', num_records=30):
        """Generate sample utility data"""
        facilities = ['HQ Building', 'Warehouse A', 'Warehouse B', 'Office Park', 'Manufacturing Plant']
        tariff_types = ['Commercial', 'Industrial', 'Standard']
        
        with open(filename, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=[
                'meter_id', 'facility_name', 'billing_start_date', 'billing_end_date',
                'consumption_kwh', 'tariff_type', 'rate_per_kwh', 'total_charge', 'currency'
            ])
            writer.writeheader()
            
            for i in range(num_records):
                billing_end = datetime.now() - timedelta(days=random.randint(1, 90))
                billing_start = billing_end - timedelta(days=30)
                consumption = random.randint(5000, 50000)
                rate = round(random.uniform(0.08, 0.15), 4)
                
                row = {
                    'meter_id': f"METER{100000 + i}",
                    'facility_name': random.choice(facilities),
                    'billing_start_date': billing_start.strftime('%Y-%m-%d'),
                    'billing_end_date': billing_end.strftime('%Y-%m-%d'),
                    'consumption_kwh': consumption,
                    'tariff_type': random.choice(tariff_types),
                    'rate_per_kwh': rate,
                    'total_charge': round(consumption * rate, 2),
                    'currency': 'USD',
                }
                writer.writerow(row)
        
        print(f"Generated {filename} with {num_records} records")
    
    @staticmethod
    def generate_travel_data(filename='sample_travel.csv', num_records=40):
        """Generate sample travel data"""
        travel_types = ['flight', 'hotel', 'ground']
        flight_classes = ['Economy', 'Business', 'First']
        vehicle_types = ['Taxi', 'Rental Car', 'Uber', 'Lyft']
        cities = ['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix', 'Miami', 'Seattle', 'Boston']
        
        with open(filename, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=[
                'travel_type', 'employee_id', 'trip_date', 'origin', 'destination',
                'distance_km', 'flight_class', 'check_in_date', 'check_out_date', 'nights',
                'vehicle_type', 'distance_miles', 'cost', 'currency'
            ])
            writer.writeheader()
            
            for i in range(num_records):
                travel_type = random.choice(travel_types)
                trip_date = datetime.now() - timedelta(days=random.randint(1, 90))
                
                row = {
                    'travel_type': travel_type,
                    'employee_id': f"EMP{100000 + random.randint(0, 100)}",
                    'trip_date': trip_date.strftime('%Y-%m-%d'),
                    'origin': random.choice(cities),
                    'destination': random.choice(cities),
                    'distance_km': random.randint(500, 5000) if travel_type == 'flight' else '',
                    'flight_class': random.choice(flight_classes) if travel_type == 'flight' else '',
                    'check_in_date': trip_date.strftime('%Y-%m-%d') if travel_type == 'hotel' else '',
                    'check_out_date': (trip_date + timedelta(days=random.randint(1, 5))).strftime('%Y-%m-%d') if travel_type == 'hotel' else '',
                    'nights': random.randint(1, 5) if travel_type == 'hotel' else '',
                    'vehicle_type': random.choice(vehicle_types) if travel_type == 'ground' else '',
                    'distance_miles': round(random.uniform(5, 50), 2) if travel_type == 'ground' else '',
                    'cost': random.randint(200, 2000) if travel_type == 'flight' else (
                        random.randint(100, 500) if travel_type == 'hotel' else random.randint(20, 100)
                    ),
                    'currency': 'USD',
                }
                writer.writerow(row)
        
        print(f"Generated {filename} with {num_records} records")


if __name__ == '__main__':
    SampleDataGenerator.generate_sap_data()
    SampleDataGenerator.generate_utility_data()
    SampleDataGenerator.generate_travel_data()
    print("All sample data generated successfully!")
