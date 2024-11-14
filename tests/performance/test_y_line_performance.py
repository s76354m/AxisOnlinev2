import pytest
import time
from app.services.y_line_service import YLineService

class TestYLinePerformance:
    def test_bulk_creation_performance(self, db_session):
        """Test performance of bulk Y-Line creation"""
        service = YLineService(db_session)
        start_time = time.time()
        
        # Create 100 Y-Lines
        y_lines_data = [
            {
                "ipa_number": f"PERF-{i}",
                "product_code": f"TEST-{i}",
                "estimated_value": 1000.00 * i
            } for i in range(100)
        ]
        
        service.bulk_create_y_lines(1, y_lines_data)
        end_time = time.time()
        
        execution_time = end_time - start_time
        assert execution_time < 2.0  # Should complete within 2 seconds

    def test_filtering_performance(self, db_session):
        """Test performance of Y-Line filtering"""
        service = YLineService(db_session)
        start_time = time.time()
        
        results = service.get_filtered_y_lines(
            min_value=50000.00,
            status="ACTIVE",
            search_term="TEST"
        )
        
        end_time = time.time()
        execution_time = end_time - start_time
        assert execution_time < 1.0  # Should complete within 1 second 