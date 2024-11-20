"""UI pages initialization"""
from typing import Dict, Callable
from .dashboard import render_page as dashboard_page
from .project_management import render_page as project_management_page
from .csp_lob_management import render_page as csp_lob_management_page
from .y_line_management import render_page as y_line_management_page
from .service_area_management import render_page as service_area_management_page
from .competitor_management import render_page as competitor_management_page

PAGE_ROUTES: Dict[str, Callable] = {
    "Dashboard": dashboard_page,
    "Project Management": project_management_page,
    "CSP LOB Management": csp_lob_management_page,
    "Y-Line Management": y_line_management_page,
    "Service Area Management": service_area_management_page,
    "Competitor Management": competitor_management_page
}

__all__ = ['PAGE_ROUTES']
