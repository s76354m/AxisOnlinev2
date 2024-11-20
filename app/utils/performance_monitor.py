import time
from contextlib import contextmanager
from typing import Dict, Optional
import streamlit as st

class PerformanceMonitor:
    def __init__(self):
        self.metrics: Dict[str, float] = {}
        self.thresholds = {
            'page_load': 3.0,  # seconds
            'api_response': 1.0,  # seconds
            'database_query': 0.5  # seconds
        }
    
    @contextmanager
    def measure(self, operation_name: str):
        start_time = time.time()
        try:
            yield
        finally:
            duration = time.time() - start_time
            self.metrics[operation_name] = duration
            self._check_threshold(operation_name, duration)
    
    def _check_threshold(self, operation: str, duration: float):
        threshold = self.thresholds.get(operation)
        if threshold and duration > threshold:
            st.warning(f"Performance warning: {operation} took {duration:.2f}s") 