from rest_framework.views import APIView
from rest_framework.response import Response
from ingestion.models import IngestionBatch, SAPRecord, UtilityRecord, TravelRecord


class DashboardView(APIView):
    """Dashboard showing ingestion status and data quality"""
    
    def get(self, request):
        """Get dashboard summary"""
        
        # Batch statistics
        total_batches = IngestionBatch.objects.count()
        pending_batches = IngestionBatch.objects.filter(status='pending').count()
        approved_batches = IngestionBatch.objects.filter(status='approved').count()
        rejected_batches = IngestionBatch.objects.filter(status='rejected').count()
        
        # Record statistics
        total_sap = SAPRecord.objects.count()
        flagged_sap = SAPRecord.objects.filter(is_flagged=True).count()
        
        total_utility = UtilityRecord.objects.count()
        flagged_utility = UtilityRecord.objects.filter(is_flagged=True).count()
        
        total_travel = TravelRecord.objects.count()
        flagged_travel = TravelRecord.objects.filter(is_flagged=True).count()
        
        # Recent batches
        recent_batches = IngestionBatch.objects.all()[:10]
        recent_data = []
        for batch in recent_batches:
            recent_data.append({
                'id': batch.id,
                'batch_id': batch.batch_id,
                'source': batch.source.name,
                'source_type': batch.source.source_type,
                'status': batch.status,
                'uploaded_at': batch.uploaded_at,
                'sap_count': SAPRecord.objects.filter(batch=batch).count(),
                'utility_count': UtilityRecord.objects.filter(batch=batch).count(),
                'travel_count': TravelRecord.objects.filter(batch=batch).count(),
                'flagged_count': (
                    SAPRecord.objects.filter(batch=batch, is_flagged=True).count() +
                    UtilityRecord.objects.filter(batch=batch, is_flagged=True).count() +
                    TravelRecord.objects.filter(batch=batch, is_flagged=True).count()
                )
            })
        
        # Flagged records by reason
        flagged_reasons = {}
        
        for record in SAPRecord.objects.filter(is_flagged=True):
            reason = record.flag_reason or 'Unknown'
            flagged_reasons[reason] = flagged_reasons.get(reason, 0) + 1
        
        for record in UtilityRecord.objects.filter(is_flagged=True):
            reason = record.flag_reason or 'Unknown'
            flagged_reasons[reason] = flagged_reasons.get(reason, 0) + 1
        
        for record in TravelRecord.objects.filter(is_flagged=True):
            reason = record.flag_reason or 'Unknown'
            flagged_reasons[reason] = flagged_reasons.get(reason, 0) + 1
        
        return Response({
            'batches': {
                'total': total_batches,
                'pending': pending_batches,
                'approved': approved_batches,
                'rejected': rejected_batches,
            },
            'records': {
                'sap': {
                    'total': total_sap,
                    'flagged': flagged_sap,
                },
                'utility': {
                    'total': total_utility,
                    'flagged': flagged_utility,
                },
                'travel': {
                    'total': total_travel,
                    'flagged': flagged_travel,
                },
                'total': total_sap + total_utility + total_travel,
                'total_flagged': flagged_sap + flagged_utility + flagged_travel,
            },
            'recent_batches': recent_data,
            'flagged_reasons': flagged_reasons,
        })
