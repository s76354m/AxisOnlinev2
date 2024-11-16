"""UI components initialization"""
from .project_management import display_project_management
from .competitor_management import display_competitor_management
from .service_area_management import display_service_area_management
from .notes_management import display_notes_management
from .status_tracker import display_status_tracker

__all__ = [
    'display_project_management',
    'display_competitor_management',
    'display_service_area_management',
    'display_notes_management',
    'display_status_tracker'
] 