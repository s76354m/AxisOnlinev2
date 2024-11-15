"""UI pages initialization"""
from .dashboard import render_page as dashboard
from .project_management import render_page as project_management
from .csp_lob_management import render_page as csp_lob_management
from .competitor_management import render_page as competitor_management
from .service_area_management import render_page as service_area_management
from .y_line_management import render_page as y_line_management

__all__ = [
    'dashboard',
    'project_management',
    'csp_lob_management',
    'competitor_management',
    'service_area_management',
    'y_line_management'
]
