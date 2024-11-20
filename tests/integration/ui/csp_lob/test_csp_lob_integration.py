"""Integration tests for csp_lob"""
import pytest
from app.services.csp_lob_service import CSPLOBService
from app.schemas.csp_lob import CSPLOBCreate, CSPLOBBulkCreate
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from tests.ui.base_test import BaseUITest

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

class TestCSPLOBIntegration(BaseUITest):
    def setup(self):
        self.driver.get("/csp-lob")
        
    def test_mapping_interface(self):
        """Test CSP LOB mapping interface"""
        # Setup mock data
        self.mock_services.csp_service.get_mapping_rules.return_value = [
            {"id": "R1", "source": "CSP1", "target": "LOB1"},
            {"id": "R2", "source": "CSP2", "target": "LOB2"}
        ]
        
        # Test creation workflow
        create_btn = self.wait_for_clickable(By.ID, "create-mapping")
        create_btn.click()
        
        # Fill mapping form
        source = self.driver.find_element(By.ID, "source-csp")
        target = self.driver.find_element(By.ID, "target-lob")
        
        source.send_keys("NewCSP")
        target.send_keys("NewLOB")
        
        # Submit and verify
        submit = self.driver.find_element(By.ID, "submit-mapping")
        submit.click()
        
        # Verify backend call
        assert self.mock_services.csp_service.create_mapping.called
        
    def test_data_operations(self):
        """Test CSP LOB data operations"""
        # Test import functionality
        import_btn = self.wait_for_clickable(By.ID, "import-data")
        import_btn.click()
        
        # Upload test file
        file_input = self.driver.find_element(By.ID, "file-upload")
        file_input.send_keys("test_data.csv")
        
        # Verify import
        success_message = self.wait_for_element(By.CLASS_NAME, "success-message")
        assert "Import successful" in success_message.text
