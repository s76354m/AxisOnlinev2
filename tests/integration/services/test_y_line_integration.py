import pytest
from sqlalchemy.orm import Session
from app.services.y_line_service import YLineService
from app.models.y_line import YLine, YLineStatus
from app.schemas.y_line import YLineCreate, YLineUpdate

class TestYLineIntegration:
    @pytest.fixture(autouse=True)
    def setup(self, db_session: Session):
        self.db = db_session
        self.service = YLineService(self.db)
        self.test_project_id = self._create_test_project()

    def _create_test_project(self):
        # Create test project
        from app.models import Project
        project = Project(
            name="Test Integration Project",
            status="Active",
            service_area="North"
        )
        self.db.add(project)
        self.db.commit()
        return project.id

    def test_y_line_creation_with_project(self):
        """Test Y-Line creation with project relationship"""
        y_line_data = YLineCreate(
            ipa_number="INT-001",
            product_code="TEST-001",
            estimated_value=100000.00,
            status=YLineStatus.PENDING
        )
        
        y_line = self.service.create_y_line(self.test_project_id, y_line_data)
        assert y_line.project_id == self.test_project_id
        assert y_line.ipa_number == "INT-001"

    def test_bulk_y_line_operations(self):
        """Test bulk creation and updates"""
        # Create multiple Y-Lines
        y_lines_data = [
            YLineCreate(
                ipa_number=f"BULK-{i}",
                product_code=f"TEST-{i}",
                estimated_value=1000.00 * i,
                status=YLineStatus.PENDING
            ) for i in range(1, 4)
        ]
        
        created_y_lines = self.service.bulk_create_y_lines(
            self.test_project_id, 
            y_lines_data
        )
        assert len(created_y_lines) == 3

        # Test bulk status update
        y_line_ids = [y.id for y in created_y_lines]
        updated_y_lines = self.service.bulk_update_status(
            y_line_ids, 
            YLineStatus.ACTIVE
        )
        assert all(y.status == YLineStatus.ACTIVE for y in updated_y_lines)

    def test_y_line_filtering(self):
        """Test advanced filtering capabilities"""
        # Create test data
        test_y_lines = [
            YLineCreate(
                ipa_number="FILTER-1",
                product_code="HIGH-VALUE",
                estimated_value=100000.00,
                status=YLineStatus.ACTIVE
            ),
            YLineCreate(
                ipa_number="FILTER-2",
                product_code="LOW-VALUE",
                estimated_value=10000.00,
                status=YLineStatus.PENDING
            )
        ]
        
        for y_line_data in test_y_lines:
            self.service.create_y_line(self.test_project_id, y_line_data)

        # Test various filters
        high_value_y_lines = self.service.get_filtered_y_lines(
            min_value=50000.00
        )
        assert len(high_value_y_lines) == 1
        assert high_value_y_lines[0].product_code == "HIGH-VALUE"

        pending_y_lines = self.service.get_filtered_y_lines(
            status=YLineStatus.PENDING
        )
        assert len(pending_y_lines) == 1
        assert pending_y_lines[0].product_code == "LOW-VALUE" 