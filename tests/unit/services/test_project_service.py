"""Unit tests for Project service"""
import pytest
from sqlalchemy.orm import Session
from app.services.project_service import ProjectService
from app.schemas.project import ProjectCreate, ProjectUpdate
from app.models.project import ProjectStatus

# Reference CRUD tests from: