import csv
from decimal import Decimal
from datetime import datetime
from django.core.exceptions import ValidationError
from ingestion.models import SAPRecord, IngestionBatch


class SAPParser:
    """
    Parses SAP exports in flat file format (CSV).
    
    SAP exports typically come as:
    - IDoc format (XML-like, complex)
    - Flat file/CSV (most common for exports)
    - OData service (API)
    
    We're handling flat file CSV because it's the most common export format
    that analysts actually use. The format expects these columns:
    
    For Fuel records:
    - plant_code, document_number, posting_date, fuel_type, quantity, unit
    
    For Procurement records:
    - plant_code, document_number, posting_date, material_code, 
      material_description, amount, currency
    """
    
    def __init__(self, batch):
        self.batch = batch
        self.errors = []
        self.warnings = []
    
    def parse_file(self, file_path):
        """Parse a CSV file and create SAPRecord objects"""
        records = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                
                for row_num, row in enumerate(reader, start=2):  # start=2 because header is row 1
                    try:
                        record = self._parse_row(row)
                        if record:
                            records.append(record)
                    except ValidationError as e:
                        self.errors.append(f"Row {row_num}: {str(e)}")
                    except Exception as e:
                        self.errors.append(f"Row {row_num}: Unexpected error - {str(e)}")
        
        except FileNotFoundError:
            raise ValidationError(f"File not found: {file_path}")
        except Exception as e:
            raise ValidationError(f"Failed to read file: {str(e)}")
        
        return records
    
    def _parse_row(self, row):
        """Parse a single row and return a SAPRecord or None if invalid"""
        # Determine record type based on presence of fuel_type or material_code
        is_fuel = bool(row.get('fuel_type', '').strip())
        is_procurement = bool(row.get('material_code', '').strip())
        
        if not (is_fuel or is_procurement):
            raise ValidationError("Row must have either fuel_type or material_code")
        
        # Common fields
        plant_code = row.get('plant_code', '').strip()
        document_number = row.get('document_number', '').strip()
        posting_date_str = row.get('posting_date', '').strip()
        
        if not all([plant_code, document_number, posting_date_str]):
            raise ValidationError("Missing required fields: plant_code, document_number, posting_date")
        
        # Parse date - handle multiple formats
        posting_date = self._parse_date(posting_date_str)
        
        record_data = {
            'batch': self.batch,
            'plant_code': plant_code,
            'document_number': document_number,
            'posting_date': posting_date,
        }
        
        if is_fuel:
            record_data['record_type'] = 'fuel'
            record_data['fuel_type'] = row.get('fuel_type', '').strip()
            
            quantity_str = row.get('quantity', '').strip()
            if quantity_str:
                try:
                    record_data['quantity'] = Decimal(quantity_str)
                except:
                    raise ValidationError(f"Invalid quantity: {quantity_str}")
            
            record_data['unit'] = row.get('unit', '').strip()
            
            # Flag if quantity is suspiciously high (e.g., > 1M liters in a day)
            if record_data.get('quantity') and record_data['quantity'] > 1000000:
                record_data['is_flagged'] = True
                record_data['flag_reason'] = "Unusually high quantity"
        
        else:  # procurement
            record_data['record_type'] = 'procurement'
            record_data['material_code'] = row.get('material_code', '').strip()
            record_data['material_description'] = row.get('material_description', '').strip()
            
            amount_str = row.get('amount', '').strip()
            if amount_str:
                try:
                    record_data['amount'] = Decimal(amount_str)
                except:
                    raise ValidationError(f"Invalid amount: {amount_str}")
            
            record_data['currency'] = row.get('currency', 'USD').strip()
        
        return SAPRecord(**record_data)
    
    def _parse_date(self, date_str):
        """Parse date in multiple formats"""
        formats = [
            '%Y-%m-%d',      # 2024-01-15
            '%d.%m.%Y',      # 15.01.2024 (German format)
            '%m/%d/%Y',      # 01/15/2024
            '%d/%m/%Y',      # 15/01/2024
        ]
        
        for fmt in formats:
            try:
                return datetime.strptime(date_str, fmt).date()
            except ValueError:
                continue
        
        raise ValidationError(f"Could not parse date: {date_str}")
    
    def save_records(self, records):
        """Bulk save records to database"""
        if not records:
            return 0
        
        created = SAPRecord.objects.bulk_create(records)
        return len(created)




class UtilityParser:
    """
    Parses utility data from CSV exports.
    
    Utility companies typically provide:
    - Portal CSV exports (most common)
    - PDF bills (requires OCR, not handling here)
    - API access (varies by utility)
    
    We handle CSV format with columns:
    - meter_id, facility_name, billing_start_date, billing_end_date,
      consumption_kwh, tariff_type, rate_per_kwh, total_charge, currency
    """
    
    def __init__(self, batch):
        self.batch = batch
        self.errors = []
    
    def parse_file(self, file_path):
        """Parse utility CSV file"""
        records = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                
                for row_num, row in enumerate(reader, start=2):
                    try:
                        record = self._parse_row(row)
                        if record:
                            records.append(record)
                    except ValidationError as e:
                        self.errors.append(f"Row {row_num}: {str(e)}")
        
        except FileNotFoundError:
            raise ValidationError(f"File not found: {file_path}")
        except Exception as e:
            raise ValidationError(f"Failed to read file: {str(e)}")
        
        return records
    
    def _parse_row(self, row):
        """Parse utility record row"""
        from ingestion.models import UtilityRecord
        
        meter_id = row.get('meter_id', '').strip()
        facility_name = row.get('facility_name', '').strip()
        billing_start_str = row.get('billing_start_date', '').strip()
        billing_end_str = row.get('billing_end_date', '').strip()
        consumption_str = row.get('consumption_kwh', '').strip()
        total_charge_str = row.get('total_charge', '').strip()
        
        if not all([meter_id, facility_name, billing_start_str, billing_end_str, consumption_str, total_charge_str]):
            raise ValidationError("Missing required fields")
        
        billing_start = self._parse_date(billing_start_str)
        billing_end = self._parse_date(billing_end_str)
        
        try:
            consumption_kwh = Decimal(consumption_str)
            total_charge = Decimal(total_charge_str)
        except:
            raise ValidationError("Invalid consumption or charge values")
        
        if consumption_kwh < 0:
            raise ValidationError("Consumption cannot be negative")
        
        record_data = {
            'batch': self.batch,
            'meter_id': meter_id,
            'facility_name': facility_name,
            'billing_start_date': billing_start,
            'billing_end_date': billing_end,
            'consumption_kwh': consumption_kwh,
            'total_charge': total_charge,
            'currency': row.get('currency', 'USD').strip(),
            'tariff_type': row.get('tariff_type', '').strip(),
        }
        
        # Parse rate if provided
        rate_str = row.get('rate_per_kwh', '').strip()
        if rate_str:
            try:
                record_data['rate_per_kwh'] = Decimal(rate_str)
            except:
                pass
        
        # Flag anomalies
        if billing_start >= billing_end:
            record_data['is_flagged'] = True
            record_data['flag_reason'] = "Billing start date is after or equal to end date"
        
        # Flag unusually high consumption (> 100k kWh per day)
        days = (billing_end - billing_start).days
        if days > 0:
            daily_avg = consumption_kwh / days
            if daily_avg > 100000:
                record_data['is_flagged'] = True
                record_data['flag_reason'] = "Unusually high daily consumption"
        
        return UtilityRecord(**record_data)
    
    def _parse_date(self, date_str):
        """Parse date in multiple formats"""
        formats = [
            '%Y-%m-%d',
            '%d.%m.%Y',
            '%m/%d/%Y',
            '%d/%m/%Y',
        ]
        
        for fmt in formats:
            try:
                return datetime.strptime(date_str, fmt).date()
            except ValueError:
                continue
        
        raise ValidationError(f"Could not parse date: {date_str}")
    
    def save_records(self, records):
        """Bulk save records"""
        if not records:
            return 0
        
        from ingestion.models import UtilityRecord
        created = UtilityRecord.objects.bulk_create(records)
        return len(created)


class TravelParser:
    """
    Parses business travel data from corporate travel platforms.
    
    Platforms like Concur, Navan, etc. typically export:
    - Flight bookings
    - Hotel stays
    - Ground transportation
    
    CSV format with columns:
    - travel_type, employee_id, trip_date, origin, destination,
      distance_km (flights), flight_class (flights),
      check_in_date, check_out_date, nights (hotels),
      vehicle_type, distance_miles (ground),
      cost, currency
    """
    
    def __init__(self, batch):
        self.batch = batch
        self.errors = []
    
    def parse_file(self, file_path):
        """Parse travel CSV file"""
        records = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                
                for row_num, row in enumerate(reader, start=2):
                    try:
                        record = self._parse_row(row)
                        if record:
                            records.append(record)
                    except ValidationError as e:
                        self.errors.append(f"Row {row_num}: {str(e)}")
        
        except FileNotFoundError:
            raise ValidationError(f"File not found: {file_path}")
        except Exception as e:
            raise ValidationError(f"Failed to read file: {str(e)}")
        
        return records
    
    def _parse_row(self, row):
        """Parse travel record row"""
        from ingestion.models import TravelRecord
        
        travel_type = row.get('travel_type', '').strip().lower()
        employee_id = row.get('employee_id', '').strip()
        trip_date_str = row.get('trip_date', '').strip()
        origin = row.get('origin', '').strip()
        destination = row.get('destination', '').strip()
        cost_str = row.get('cost', '').strip()
        
        if not all([travel_type, employee_id, trip_date_str, origin, destination, cost_str]):
            raise ValidationError("Missing required fields")
        
        if travel_type not in ['flight', 'hotel', 'ground']:
            raise ValidationError(f"Invalid travel_type: {travel_type}")
        
        trip_date = self._parse_date(trip_date_str)
        
        try:
            cost = Decimal(cost_str)
        except:
            raise ValidationError("Invalid cost value")
        
        if cost < 0:
            raise ValidationError("Cost cannot be negative")
        
        record_data = {
            'batch': self.batch,
            'travel_type': travel_type,
            'employee_id': employee_id,
            'trip_date': trip_date,
            'origin': origin,
            'destination': destination,
            'cost': cost,
            'currency': row.get('currency', 'USD').strip(),
        }
        
        # Type-specific fields
        if travel_type == 'flight':
            distance_str = row.get('distance_km', '').strip()
            if distance_str:
                try:
                    record_data['distance_km'] = int(distance_str)
                except:
                    raise ValidationError("Invalid distance_km")
            
            record_data['flight_class'] = row.get('flight_class', '').strip()
            
            # Flag if distance is unrealistic (> 20k km)
            if record_data.get('distance_km') and record_data['distance_km'] > 20000:
                record_data['is_flagged'] = True
                record_data['flag_reason'] = "Unrealistic flight distance"
        
        elif travel_type == 'hotel':
            check_in_str = row.get('check_in_date', '').strip()
            check_out_str = row.get('check_out_date', '').strip()
            
            if check_in_str:
                record_data['check_in_date'] = self._parse_date(check_in_str)
            if check_out_str:
                record_data['check_out_date'] = self._parse_date(check_out_str)
            
            nights_str = row.get('nights', '').strip()
            if nights_str:
                try:
                    record_data['nights'] = int(nights_str)
                except:
                    raise ValidationError("Invalid nights value")
            
            # Flag if check-in is after check-out
            if record_data.get('check_in_date') and record_data.get('check_out_date'):
                if record_data['check_in_date'] >= record_data['check_out_date']:
                    record_data['is_flagged'] = True
                    record_data['flag_reason'] = "Check-in date is after or equal to check-out date"
        
        elif travel_type == 'ground':
            record_data['vehicle_type'] = row.get('vehicle_type', '').strip()
            
            distance_str = row.get('distance_miles', '').strip()
            if distance_str:
                try:
                    record_data['distance_miles'] = Decimal(distance_str)
                except:
                    raise ValidationError("Invalid distance_miles")
        
        # Flag unusually high costs
        if cost > 10000:
            record_data['is_flagged'] = True
            record_data['flag_reason'] = "Unusually high cost"
        
        return TravelRecord(**record_data)
    
    def _parse_date(self, date_str):
        """Parse date in multiple formats"""
        formats = [
            '%Y-%m-%d',
            '%d.%m.%Y',
            '%m/%d/%Y',
            '%d/%m/%Y',
        ]
        
        for fmt in formats:
            try:
                return datetime.strptime(date_str, fmt).date()
            except ValueError:
                continue
        
        raise ValidationError(f"Could not parse date: {date_str}")
    
    def save_records(self, records):
        """Bulk save records"""
        if not records:
            return 0
        
        from ingestion.models import TravelRecord
        created = TravelRecord.objects.bulk_create(records)
        return len(created)
