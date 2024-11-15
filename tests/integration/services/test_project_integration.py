"""Integration tests for project service"""
import pytest
from sqlalchemy.orm import Session
from app.models.project import Project, ProjectStatus
from app.schemas.project import ProjectCreate
from app.schemas.csp_lob import CSPLOBCreate
from .base_service_test import BaseServiceTest

class TestProjectIntegration(BaseServiceTest):
    def test_complete_project_workflow(self):
