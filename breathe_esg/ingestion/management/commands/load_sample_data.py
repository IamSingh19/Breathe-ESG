from django.core.management.base import BaseCommand
from ingestion.models import DataSource, IngestionBatch
from ingestion.parsers import SAPParser, UtilityParser, TravelParser


class Command(BaseCommand):
    help = 'Load sample data into the database'
    
    def handle(self, *args, **options):
        # Create data sources
        sap_source, _ = DataSource.objects.get_or_create(
            name='SAP System',
            source_type='sap'
        )
        utility_source, _ = DataSource.objects.get_or_create(
            name='Utility Portal',
            source_type='utility'
        )
        travel_source, _ = DataSource.objects.get_or_create(
            name='Travel Platform',
            source_type='travel'
        )
        
        self.stdout.write(self.style.SUCCESS('Created data sources'))
        
        # Load SAP data
        sap_batch = IngestionBatch.objects.create(
            source=sap_source,
            batch_id='sap_sample_001'
        )
        sap_parser = SAPParser(sap_batch)
        sap_records = sap_parser.parse_file('sample_sap.csv')
        sap_count = sap_parser.save_records(sap_records)
        self.stdout.write(self.style.SUCCESS(f'Loaded {sap_count} SAP records'))
        
        # Load utility data
        utility_batch = IngestionBatch.objects.create(
            source=utility_source,
            batch_id='utility_sample_001'
        )
        utility_parser = UtilityParser(utility_batch)
        utility_records = utility_parser.parse_file('sample_utility.csv')
        utility_count = utility_parser.save_records(utility_records)
        self.stdout.write(self.style.SUCCESS(f'Loaded {utility_count} utility records'))
        
        # Load travel data
        travel_batch = IngestionBatch.objects.create(
            source=travel_source,
            batch_id='travel_sample_001'
        )
        travel_parser = TravelParser(travel_batch)
        travel_records = travel_parser.parse_file('sample_travel.csv')
        travel_count = travel_parser.save_records(travel_records)
        self.stdout.write(self.style.SUCCESS(f'Loaded {travel_count} travel records'))
        
        self.stdout.write(self.style.SUCCESS('Sample data loaded successfully!'))
