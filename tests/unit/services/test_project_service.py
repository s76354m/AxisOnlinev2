"""Unit tests for Project Service"""
import pytest
from app.services.project_service import ProjectService
from app.schemas.project import ProjectCreate, ProjectUpdate
from app.core.error_handler import AppError
from sqlalchemy.exc import IntegrityError

class TestProjectCreation:
    @pytest.fixture(autouse=True)
    def setup(self, db_session):
        self.service = ProjectService(db_session)
        self.test_projects = self._create_test_projects()
    
    def _create_test_projects(self):
        projects = []
        for i in range(3):
            project = self.service.create_project(ProjectCreate(
                ProjectType="T",
                ProjectDesc=f"Test Project {i}",
                Analyst="Test Analyst",
                PM="Test PM"
            ))
            projects.append(project)
        return projects
    
    def test_project_creation_validation(self):
        """Test project creation with validation"""
        # Test required fields
        with pytest.raises(ValueError) as exc:
            self.service.create_project(ProjectCreate())
        assert "ProjectType is required" in str(exc.value)
        
        # Test field validation
        with pytest.raises(ValueError) as exc:
            self.service.create_project(ProjectCreate(
                ProjectType="INVALID",
                ProjectDesc="Test"
            ))
        assert "Invalid project type" in str(exc.value)
    
    def test_project_creation_success(self):
        """Test successful project creation"""
        project = self.service.create_project(ProjectCreate(
            ProjectType="T",
            ProjectDesc="Test Project",
            Analyst="Test Analyst",
            PM="Test PM"
        ))
        assert project.ProjectType == "T"
        assert project.Status == "NEW"
    
    def test_project_creation_error_handling(self):
        """Test error handling during project creation"""
        # Test duplicate project
        self.service.create_project(ProjectCreate(
            ProjectType="T",
            ProjectDesc="Original"
        ))
        
        with pytest.raises(AppError) as exc:
            self.service.create_project(ProjectCreate(
                ProjectType="T",
                ProjectDesc="Duplicate"
            ))
        assert "Project already exists" in str(exc.value)

class TestProjectEdit:
    @pytest.fixture(autouse=True)
    def setup(self, db_session):
        self.service = ProjectService(db_session)
        self.test_project = self._create_test_project()
    
    def _create_test_project(self):
        project_data = ProjectCreate(
            ProjectType="T",
            ProjectDesc="Test Project",
            Analyst="Test Analyst",
            PM="Test PM"
        )
        return self.service.create_project(project_data)
    
    def test_field_updates(self):
        """Test individual field updates"""
        updated = self.service.update_project(
            self.test_project.ProjectID,
            ProjectUpdate(ProjectDesc="Updated Description")
        )
        assert updated.ProjectDesc == "Updated Description"
        assert updated.LastEditDate is not None
    
    def test_status_changes(self):
        """Test project status transitions"""
        # Test valid transition
        updated = self.service.update_project(
            self.test_project.ProjectID,
            ProjectUpdate(Status="ACTIVE")
        )
        assert updated.Status == "ACTIVE"
        
        # Test invalid transition
        with pytest.raises(ValueError):
            self.service.update_project(
                self.test_project.ProjectID,
                ProjectUpdate(Status="INVALID")
            )
    
    def test_history_tracking(self):
        """Test project history tracking"""
        history = self.service.get_project_history(self.test_project.ProjectID)
        initial_count = len(history)
        
        self.service.update_project(
            self.test_project.ProjectID,
            ProjectUpdate(Status="ACTIVE")
        )
        
        updated_history = self.service.get_project_history(self.test_project.ProjectID)
        assert len(updated_history) == initial_count + 1