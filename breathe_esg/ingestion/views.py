from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError
import uuid
import os
from ingestion.models import DataSource, IngestionBatch, SAPRecord, UtilityRecord, TravelRecord
from ingestion.serializers import (
    DataSourceSerializer, IngestionBatchSerializer, 
    SAPRecordSerializer, UtilityRecordSerializer, TravelRecordSerializer
)
from ingestion.parsers import SAPParser, UtilityParser, TravelParser


class DataSourceViewSet(viewsets.ModelViewSet):
    queryset = DataSource.objects.all()
    serializer_class = DataSourceSerializer


class IngestionBatchViewSet(viewsets.ModelViewSet):
    queryset = IngestionBatch.objects.all()
    serializer_class = IngestionBatchSerializer
    parser_classes = (MultiPartParser, FormParser, JSONParser)
    
    @action(detail=False, methods=['post'])
    def upload(self, request):
        """Upload and ingest data file"""
        source_id = request.data.get('source_id')
        file = request.FILES.get('file')
        
        if not source_id or not file:
            return Response(
                {'error': 'source_id and file are required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        source = get_object_or_404(DataSource, id=source_id)
        
        # Create batch
        batch_id = f"{source.source_type}_{uuid.uuid4().hex[:8]}"
        batch = IngestionBatch.objects.create(
            source=source,
            batch_id=batch_id
        )
        
        # Save file temporarily
        temp_path = f"/tmp/{batch_id}_{file.name}"
        os.makedirs(os.path.dirname(temp_path), exist_ok=True)
        
        with open(temp_path, 'wb+') as f:
            for chunk in file.chunks():
                f.write(chunk)
        
        try:
            # Parse based on source type
            if source.source_type == 'sap':
                parser = SAPParser(batch)
                records = parser.parse_file(temp_path)
                count = parser.save_records(records)
            elif source.source_type == 'utility':
                parser = UtilityParser(batch)
                records = parser.parse_file(temp_path)
                count = parser.save_records(records)
            elif source.source_type == 'travel':
                parser = TravelParser(batch)
                records = parser.parse_file(temp_path)
                count = parser.save_records(records)
            else:
                return Response(
                    {'error': f'Unknown source type: {source.source_type}'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            return Response({
                'batch_id': batch.id,
                'batch_number': batch.batch_id,
                'records_ingested': count,
                'errors': parser.errors if hasattr(parser, 'errors') else []
            }, status=status.HTTP_201_CREATED)
        
        except ValidationError as e:
            batch.delete()
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        finally:
            # Clean up temp file
            if os.path.exists(temp_path):
                os.remove(temp_path)
    
    @action(detail=True, methods=['get'])
    def records(self, request, pk=None):
        """Get all records in a batch"""
        batch = self.get_object()
        
        sap_records = SAPRecord.objects.filter(batch=batch)
        utility_records = UtilityRecord.objects.filter(batch=batch)
        travel_records = TravelRecord.objects.filter(batch=batch)
        
        data = {
            'batch_id': batch.id,
            'batch_number': batch.batch_id,
            'status': batch.status,
            'sap_records': SAPRecordSerializer(sap_records, many=True).data,
            'utility_records': UtilityRecordSerializer(utility_records, many=True).data,
            'travel_records': TravelRecordSerializer(travel_records, many=True).data,
            'total_records': sap_records.count() + utility_records.count() + travel_records.count(),
            'flagged_records': (
                sap_records.filter(is_flagged=True).count() +
                utility_records.filter(is_flagged=True).count() +
                travel_records.filter(is_flagged=True).count()
            )
        }
        
        return Response(data)
    
    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        """Approve a batch"""
        batch = self.get_object()
        batch.status = 'approved'
        batch.reviewed_by = request.data.get('reviewed_by', 'Unknown')
        batch.notes = request.data.get('notes', '')
        from datetime import datetime
        batch.reviewed_at = datetime.now()
        batch.save()
        
        return Response(IngestionBatchSerializer(batch).data)
    
    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        """Reject a batch"""
        batch = self.get_object()
        batch.status = 'rejected'
        batch.reviewed_by = request.data.get('reviewed_by', 'Unknown')
        batch.notes = request.data.get('notes', '')
        from datetime import datetime
        batch.reviewed_at = datetime.now()
        batch.save()
        
        return Response(IngestionBatchSerializer(batch).data)
    
    @action(detail=True, methods=['post'])
    def reset(self, request, pk=None):
        """Reset batch status to pending"""
        batch = self.get_object()
        batch.status = 'pending'
        batch.reviewed_by = None
        batch.notes = ''
        batch.reviewed_at = None
        batch.save()
        
        return Response(IngestionBatchSerializer(batch).data)


class SAPRecordViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = SAPRecord.objects.all()
    serializer_class = SAPRecordSerializer
    
    def get_queryset(self):
        batch_id = self.request.query_params.get('batch_id')
        if batch_id:
            return SAPRecord.objects.filter(batch_id=batch_id)
        return SAPRecord.objects.all()


class UtilityRecordViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = UtilityRecord.objects.all()
    serializer_class = UtilityRecordSerializer
    
    def get_queryset(self):
        batch_id = self.request.query_params.get('batch_id')
        if batch_id:
            return UtilityRecord.objects.filter(batch_id=batch_id)
        return UtilityRecord.objects.all()


class TravelRecordViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = TravelRecord.objects.all()
    serializer_class = TravelRecordSerializer
    
    def get_queryset(self):
        batch_id = self.request.query_params.get('batch_id')
        if batch_id:
            return TravelRecord.objects.filter(batch_id=batch_id)
        return TravelRecord.objects.all()
