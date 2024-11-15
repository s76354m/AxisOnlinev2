"""Unit tests for database models"""
import pytest
from datetime import datetime
from app.models.project import Project, ProjectStatus, ProjectType
from app.models.csp_lob import CSPLOB, LOBType
from app.models.y_line import YLine, YLineStatus
from app.models.competitor import Competitor
from sqlalchemy.exc import IntegrityError
