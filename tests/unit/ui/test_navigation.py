import pytest
from app.ui.main import AxisProgramUI
from app.utils.session_state_manager import SessionStateManager

def test_navigation_consistency():
    """Test navigation consistency across components"""
    app = AxisProgramUI()
    
    # Test navigation items match routes
    nav_items = app.render_navigation()
    assert set(nav_items) == set(PAGE_ROUTES.keys())
    
    # Test breadcrumb accuracy
    for page in PAGE_ROUTES.keys():
        SessionStateManager.set('current_page', page)
        assert st.session_state.get('current_page') == page

def test_navigation_state_persistence():
    """Test navigation state persists correctly"""
    app = AxisProgramUI()
    
    # Test state persistence
    test_pages = list(PAGE_ROUTES.keys())
    for page in test_pages:
        SessionStateManager.set('current_page', page)
        app.run()
        assert st.session_state.get('current_page') == page 