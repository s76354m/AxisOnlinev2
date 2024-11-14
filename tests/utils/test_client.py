"""Custom Streamlit test client"""
import streamlit as st
from unittest.mock import MagicMock

class StreamlitTestClient:
    """Custom Streamlit test client"""
    def __init__(self):
        self.session_state = {}
        self.sidebar = MagicMock()
        self.markdown = MagicMock()
        self.write = MagicMock()
        self.error = MagicMock()
        self.success = MagicMock()
        self.info = MagicMock()
        self.warning = MagicMock()
        
    def text_input(self, label, value="", **kwargs):
        """Mock text input"""
        return value
    
    def selectbox(self, label, options, index=0, **kwargs):
        """Mock selectbox"""
        return options[index] if options else None
    
    def checkbox(self, label, value=False, **kwargs):
        """Mock checkbox"""
        return value
    
    def form(self, key):
        """Mock form"""
        class MockForm:
            def __enter__(self):
                return self
            def __exit__(self, *args):
                pass
        return MockForm()
    
    def form_submit_button(self, label):
        """Mock form submit button"""
        return False 