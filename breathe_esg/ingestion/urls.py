from django.urls import path, include
from rest_framework.routers import DefaultRouter
from ingestion.views import (
    DataSourceViewSet, IngestionBatchViewSet,
    SAPRecordViewSet, UtilityRecordViewSet, TravelRecordViewSet
)

router = DefaultRouter()
router.register(r'sources', DataSourceViewSet)
router.register(r'batches', IngestionBatchViewSet)
router.register(r'sap-records', SAPRecordViewSet)
router.register(r'utility-records', UtilityRecordViewSet)
router.register(r'travel-records', TravelRecordViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
