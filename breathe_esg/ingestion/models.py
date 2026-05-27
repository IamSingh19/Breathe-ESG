from django.db import models
from django.core.validators import MinValueValidator
from datetime import datetime

class DataSource(models.Model):
    """Represents a data source (SAP, Utility, Travel)"""
    SOURCE_TYPES = [
        ('sap', 'SAP'),
        ('utility', 'Utility'),
        ('travel', 'Travel'),
    ]
    
    name = models.CharField(max_length=255)
    source_type = models.CharField(max_length=20, choices=SOURCE_TYPES)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} ({self.get_source_type_display()})"


class IngestionBatch(models.Model):
    """Tracks a batch of ingested data"""
    STATUS_CHOICES = [
        ('pending', 'Pending Review'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    
    source = models.ForeignKey(DataSource, on_delete=models.CASCADE)
    batch_id = models.CharField(max_length=100, unique=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)
    reviewed_by = models.CharField(max_length=255, null=True, blank=True)
    notes = models.TextField(blank=True)
    
    class Meta:
        ordering = ['-uploaded_at']
    
    def __str__(self):
        return f"Batch {self.batch_id} - {self.status}"


class SAPRecord(models.Model):
    """SAP fuel and procurement data"""
    RECORD_TYPES = [
        ('fuel', 'Fuel'),
        ('procurement', 'Procurement'),
    ]
    
    batch = models.ForeignKey(IngestionBatch, on_delete=models.CASCADE, related_name='sap_records')
    record_type = models.CharField(max_length=20, choices=RECORD_TYPES)
    
    # Common fields
    plant_code = models.CharField(max_length=50)
    document_number = models.CharField(max_length=100)
    posting_date = models.DateField()
    
    # Fuel specific
    fuel_type = models.CharField(max_length=100, blank=True)  # e.g., "Diesel", "Petrol", "Natural Gas"
    quantity = models.DecimalField(max_digits=12, decimal_places=3, null=True, blank=True)
    unit = models.CharField(max_length=20, blank=True)  # L, kg, m3, etc.
    
    # Procurement specific
    material_code = models.CharField(max_length=100, blank=True)
    material_description = models.CharField(max_length=255, blank=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    currency = models.CharField(max_length=3, default='USD')
    
    # Data quality flags
    is_flagged = models.BooleanField(default=False)
    flag_reason = models.CharField(max_length=255, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-posting_date']
    
    def __str__(self):
        return f"SAP {self.record_type} - {self.document_number}"


class UtilityRecord(models.Model):
    """Electricity utility data"""
    batch = models.ForeignKey(IngestionBatch, on_delete=models.CASCADE, related_name='utility_records')
    
    meter_id = models.CharField(max_length=100)
    facility_name = models.CharField(max_length=255)
    
    # Billing period
    billing_start_date = models.DateField()
    billing_end_date = models.DateField()
    
    # Consumption
    consumption_kwh = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0)])
    
    # Tariff info
    tariff_type = models.CharField(max_length=100, blank=True)  # e.g., "Commercial", "Industrial"
    rate_per_kwh = models.DecimalField(max_digits=8, decimal_places=4, null=True, blank=True)
    
    # Charges
    total_charge = models.DecimalField(max_digits=12, decimal_places=2)
    currency = models.CharField(max_length=3, default='USD')
    
    # Data quality
    is_flagged = models.BooleanField(default=False)
    flag_reason = models.CharField(max_length=255, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-billing_end_date']
    
    def __str__(self):
        return f"Utility {self.meter_id} - {self.billing_end_date}"


class TravelRecord(models.Model):
    """Business travel data from corporate travel platform"""
    TRAVEL_TYPES = [
        ('flight', 'Flight'),
        ('hotel', 'Hotel'),
        ('ground', 'Ground Transportation'),
    ]
    
    batch = models.ForeignKey(IngestionBatch, on_delete=models.CASCADE, related_name='travel_records')
    
    travel_type = models.CharField(max_length=20, choices=TRAVEL_TYPES)
    employee_id = models.CharField(max_length=100)
    
    # Trip details
    trip_date = models.DateField()
    origin = models.CharField(max_length=255)
    destination = models.CharField(max_length=255)
    
    # Flight specific
    distance_km = models.IntegerField(null=True, blank=True)
    flight_class = models.CharField(max_length=50, blank=True)  # Economy, Business, First
    
    # Hotel specific
    check_in_date = models.DateField(null=True, blank=True)
    check_out_date = models.DateField(null=True, blank=True)
    nights = models.IntegerField(null=True, blank=True)
    
    # Ground transportation
    vehicle_type = models.CharField(max_length=100, blank=True)  # Taxi, Rental Car, etc.
    distance_miles = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    
    # Cost
    cost = models.DecimalField(max_digits=12, decimal_places=2)
    currency = models.CharField(max_length=3, default='USD')
    
    # Data quality
    is_flagged = models.BooleanField(default=False)
    flag_reason = models.CharField(max_length=255, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-trip_date']
    
    def __str__(self):
        return f"Travel {self.travel_type} - {self.trip_date}"
