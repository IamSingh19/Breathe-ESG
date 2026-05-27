from rest_framework import serializers
from ingestion.models import DataSource, IngestionBatch, SAPRecord, UtilityRecord, TravelRecord


class DataSourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataSource
        fields = ['id', 'name', 'source_type', 'created_at']


class SAPRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = SAPRecord
        fields = [
            'id', 'batch', 'record_type', 'plant_code', 'document_number',
            'posting_date', 'fuel_type', 'quantity', 'unit', 'material_code',
            'material_description', 'amount', 'currency', 'is_flagged',
            'flag_reason', 'created_at'
        ]


class UtilityRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = UtilityRecord
        fields = [
            'id', 'batch', 'meter_id', 'facility_name', 'billing_start_date',
            'billing_end_date', 'consumption_kwh', 'tariff_type', 'rate_per_kwh',
            'total_charge', 'currency', 'is_flagged', 'flag_reason', 'created_at'
        ]


class TravelRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = TravelRecord
        fields = [
            'id', 'batch', 'travel_type', 'employee_id', 'trip_date', 'origin',
            'destination', 'distance_km', 'flight_class', 'check_in_date',
            'check_out_date', 'nights', 'vehicle_type', 'distance_miles', 'cost',
            'currency', 'is_flagged', 'flag_reason', 'created_at'
        ]


class IngestionBatchSerializer(serializers.ModelSerializer):
    source_name = serializers.CharField(source='source.name', read_only=True)
    source_type = serializers.CharField(source='source.source_type', read_only=True)
    
    class Meta:
        model = IngestionBatch
        fields = [
            'id', 'batch_id', 'source', 'source_name', 'source_type', 'status',
            'uploaded_at', 'reviewed_at', 'reviewed_by', 'notes'
        ]
