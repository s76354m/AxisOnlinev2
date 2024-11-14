import pytest
from sqlalchemy.orm import Session
from app.services.competitor_service import CompetitorService
from app.services.service_area_service import ServiceAreaService
from app.schemas.competitor import CompetitorCreate, CompetitorUpdate
from app.schemas.service_area import ServiceAreaCreate, ServiceAreaUpdate

# Competitor Tests
def test_competitor_crud(db: Session):
    # Create
    competitor_data = CompetitorCreate(
        ProjectID="TEST001",
        Product="Test Product",
        Payor="Test Payor"
    )
    competitor = CompetitorService.create_competitor(db=db, competitor=competitor_data)
    assert competitor.ProjectID == "TEST001"
    
    # Read
    competitors = CompetitorService.get_competitors_by_project(db=db, project_id="TEST001")
    assert len(competitors) > 0
    
    # Update
    update_data = CompetitorUpdate(Product="Updated Product")
    updated_competitor = CompetitorService.update_competitor(
        db=db, record_id=competitor.RecordID, competitor=update_data
    )
    assert updated_competitor.Product == "Updated Product"
    
    # Delete
    deleted_competitor = CompetitorService.delete_competitor(db=db, record_id=competitor.RecordID)
    assert deleted_competitor is not None

# Service Area Tests
def test_service_area_crud(db: Session):
    # Create
    service_area_data = ServiceAreaCreate(
        ProjectID="TEST001",
        ServiceArea="Test Area",
        Mileage=10.5
    )
    service_area = ServiceAreaService.create_service_area(db=db, service_area=service_area_data)
    assert service_area.ProjectID == "TEST001"
    
    # Read
    service_areas = ServiceAreaService.get_service_areas_by_project(db=db, project_id="TEST001")
    assert len(service_areas) > 0
    
    # Update
    update_data = ServiceAreaUpdate(Mileage=15.5)
    updated_service_area = ServiceAreaService.update_service_area(
        db=db, record_id=service_area.RecordID, service_area=update_data
    )
    assert updated_service_area.Mileage == 15.5
    
    # Delete
    deleted_service_area = ServiceAreaService.delete_service_area(db=db, record_id=service_area.RecordID)
    assert deleted_service_area is not None 