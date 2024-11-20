"""Integration tests for CSP LOB service"""
import pytest
from unittest.mock import Mock, patch
from app.services.csp_lob_service import CSPLOBService
from app.models.csp_lob import CSPLOB
from app.schemas.csp_lob import CSPLOBCreate

@pytest.mark.integration
class TestCSPLOBIntegration:
    @pytest.fixture(autouse=True)
    def setup(self, mock_dependencies):
        self.service = CSPLOBService()
        self.mock_db = mock_dependencies
    
    def test_complete_csp_lob_workflow(self):
        """Test complete CSP LOB workflow"""
        # Create mapping
        mapping_data = CSPLOBCreate(
            csp_code="WF001",
            lob_type="Medical",
            description="Workflow Test",
            project_id=self.project_id
        )
        mapping = self.service.create_csp_lob(mapping_data)
        assert mapping.csp_code == "WF001"
        
        # Update mapping
        updated = self.service.update_csp_lob(
            mapping.id,
            {"status": CSPLOBStatus.ACTIVE}
        )
        assert updated.status == CSPLOBStatus.ACTIVE
        
        # Verify relationships
        project_mappings = self.service.get_project_mappings(self.project_id)
        assert len(project_mappings) == 1
        assert project_mappings[0].csp_code == "WF001" 