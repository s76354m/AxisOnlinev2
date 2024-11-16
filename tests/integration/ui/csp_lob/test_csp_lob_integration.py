"""Integration tests for csp_lob"""
import pytest
from app.services.csp_lob_service import CSPLOBService
from app.schemas.csp_lob import CSPLOBCreate, CSPLOBBulkCreate
import pandas as pd

class TestCSPLOBOperations:
    @pytest.fixture(autouse=True)
    def setup(self, db_session):
        self.service = CSPLOBService(db_session)
        self.test_data = self._create_test_data()
    
    def test_import_functionality(self):
        """Test importing CSP LOB mappings"""
        # Create test CSV
        df = pd.DataFrame({
            'csp_code': ['IMP001', 'IMP002'],
            'lob_type': ['Medical', 'Dental'],
            'description': ['Import Test 1', 'Import Test 2']
        })
        csv_path = 'test_import.csv'
        df.to_csv(csv_path, index=False)
        
        # Import data
        result = self.service.import_mappings(csv_path)
        assert result.success_count == 2
        assert len(result.errors) == 0
    
    def test_export_functionality(self):
        """Test exporting CSP LOB mappings"""
        export_data = self.service.export_mappings()
        assert isinstance(export_data, pd.DataFrame)
        assert len(export_data) > 0
        assert all(col in export_data.columns for col in ['csp_code', 'lob_type'])
    
    def test_bulk_updates(self):
        """Test bulk update operations"""
        update_data = {'status': 'Inactive'}
        csp_codes = ['TEST001', 'TEST002']
        
        results = self.service.bulk_update(csp_codes, update_data)
        assert all(r.status == 'Inactive' for r in results)
