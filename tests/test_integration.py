import pytest
from sqlalchemy.orm import Session
from datetime import datetime
import pandas as pd
from app.db.session import get_db
from app.models import (
    Project,
    Competitor,
    ServiceArea,
    YLine,
    ProjectNote
)

class TestDatabaseOperations:
    @pytest.fixture
    def db(self):
        db = next(get_db())
        yield db
        db.close()

    def test_project_creation(self, db: Session):
        """Test creating a new project"""
        project_data = {
            'ProjectID': 'TEST001',
            'ProjectType': 'A',
            'ProjectDesc': 'Test Project',
            'Analyst': 'Test Analyst',
            'PM': 'Test PM',
            'Status': 'New'
        }
        
        # Create project
        project = Project(**project_data)
        db.add(project)
        db.commit()
        
        # Verify project exists
        db_project = db.query(Project).filter(Project.ProjectID == 'TEST001').first()
        assert db_project is not None
        assert db_project.ProjectID == 'TEST001'
        assert db_project.ProjectType == 'A'
        
        # Clean up
        db.delete(db_project)
        db.commit()

    def test_competitor_creation(self, db: Session):
        """Test creating a new competitor"""
        competitor_data = {
            'ProjectID': 'TEST001',
            'StrenuusProductCode': 'TEST',
            'Payor': 'Test Payor',
            'Product': 'Test Product',
            'EI': True,
            'CS': False,
            'MR': True
        }
        
        competitor = Competitor(**competitor_data)
        db.add(competitor)
        db.commit()
        
        db_competitor = db.query(Competitor).filter(
            Competitor.ProjectID == 'TEST001'
        ).first()
        assert db_competitor is not None
        assert db_competitor.Payor == 'Test Payor'
        
        db.delete(db_competitor)
        db.commit()

    def test_service_area_creation(self, db: Session):
        """Test creating a new service area"""
        service_area_data = {
            'ProjectID': 'TEST001',
            'Region': 'Test Region',
            'State': 'TX',
            'County': 'Test County',
            'ReportInclude': 'Y',
            'MaxMileage': 50
        }
        
        service_area = ServiceArea(**service_area_data)
        db.add(service_area)
        db.commit()
        
        db_service_area = db.query(ServiceArea).filter(
            ServiceArea.ProjectID == 'TEST001'
        ).first()
        assert db_service_area is not None
        assert db_service_area.State == 'TX'
        
        db.delete(db_service_area)
        db.commit()

    def test_yline_creation(self, db: Session):
        """Test creating a new Y-Line"""
        yline_data = {
            'ProjectID': 'TEST001',
            'NDB_Yline_ProdCd': 'A1',
            'NDB_Yline_IPA': 123,
            'NDB_Yline_MktNum': 456,
            'PreAward': 1
        }
        
        yline = YLine(**yline_data)
        db.add(yline)
        db.commit()
        
        db_yline = db.query(YLine).filter(
            YLine.ProjectID == 'TEST001'
        ).first()
        assert db_yline is not None
        assert db_yline.NDB_Yline_ProdCd == 'A1'
        
        db.delete(db_yline)
        db.commit()

    def test_note_creation(self, db: Session):
        """Test creating a new note"""
        note_data = {
            'ProjectID': 'TEST001',
            'Notes': 'Test Note',
            'ActionItem': 'Y',
            'ProjectCategory': 'Test Category'
        }
        
        note = ProjectNote(**note_data)
        db.add(note)
        db.commit()
        
        db_note = db.query(ProjectNote).filter(
            ProjectNote.ProjectID == 'TEST001'
        ).first()
        assert db_note is not None
        assert db_note.Notes == 'Test Note'
        
        db.delete(db_note)
        db.commit() 