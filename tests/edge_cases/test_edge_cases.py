import pytest
from unittest.mock import Mock, patch
import streamlit as st
import time

class TestEdgeCases:
    def test_large_data_handling(self):
        """Test handling of large datasets"""
        large_dataset = [Mock() for _ in range(10000)]
        with patch('app.services.data_service.DataService') as mock_service:
            mock_service.get_data.return_value = large_dataset
            start_time = time.time()
            # Perform operation
            assert time.time() - start_time < 5
    
    def test_concurrent_operations(self):
        """Test concurrent operation handling"""
        import threading
        
        def concurrent_operation():
            st.session_state.counter = st.session_state.get('counter', 0) + 1
        
        threads = [threading.Thread(target=concurrent_operation) for _ in range(10)]
        [t.start() for t in threads]
        [t.join() for t in threads]
        
        assert st.session_state.counter == 10 