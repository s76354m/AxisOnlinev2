from app.ui.pages.project_management import render_page as project_management_render
from app.ui.pages.competitor_management import render_page as competitor_management_render
from app.ui.pages.service_area_management import render_page as service_area_management_render
from app.ui.pages.y_line_management import render_page as y_line_management_render
from app.ui.pages.csp_lob_management import render_page as csp_lob_management_render

# Create module-level objects for each page
class PageModule:
    def __init__(self, render_func):
        self.render_page = render_func

project_management = PageModule(project_management_render)
competitor_management = PageModule(competitor_management_render)
service_area_management = PageModule(service_area_management_render)
y_line_management = PageModule(y_line_management_render)
csp_lob_management = PageModule(csp_lob_management_render)

__all__ = [
    'project_management',
    'competitor_management',
    'service_area_management',
    'y_line_management',
    'csp_lob_management'
]
