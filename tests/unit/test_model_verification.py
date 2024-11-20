import pytest
from app.utils.model_verification import verify_model_schema, verify_all_models
from app.models import Project, CSPLOB, YLine

def test_verify_project_model():
    """Test Project model verification"""
    result = verify_model_schema(Project)
    assert result['table_name'] == Project.__tablename__
    assert not result['missing_columns'], "No columns should be missing"
    
def test_verify_all_models():
    """Test verification of all models"""
    results = verify_all_models()
    assert len(results) > 0, "Should have verification results"
    assert all('error' not in r for r in results), "No models should have errors"

def test_model_column_types():
    """Test column type verification"""
    result = verify_model_schema(Project)
    assert any(col[0] == 'ProjectID' for col in result['column_types'])
    assert any(col[0] == 'Status' for col in result['column_types']) 