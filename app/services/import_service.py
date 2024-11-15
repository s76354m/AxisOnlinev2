"""Import service for CSP LOB data"""
import pandas as pd
from typing import List, Dict
from app.utils.validators import CSPLOBValidator
from app.services.csp_lob_service import CSPLOBService
import logging

logger = logging.getLogger(__name__)

class ImportService:
    def __init__(self, db_session):
        self.db = db_session
        self.csp_lob_service = CSPLOBService(db_session)

    def validate_import_data(self, df: pd.DataFrame) -> List[Dict]:
        """Validate import data"""
        errors = []
        for idx, row in df.iterrows():
            try:
                CSPLOBValidator.validate_csp_code(row['csp_code'])
                CSPLOBValidator.validate_dates(
                    row['effective_date'],
                    row.get('termination_date')
                )
            except ValueError as e:
                errors.append({
                    'row': idx + 1,
                    'error': str(e)
                })
        return errors

    def process_import(self, df: pd.DataFrame) -> Dict:
        """Process import data"""
        results = {
            'success': 0,
            'failed': 0,
            'errors': []
        }

        for idx, row in df.iterrows():
            try:
                mapping_data = {
                    'csp_code': row['csp_code'],
                    'lob_type': row['lob_type'],
                    'description': row['description'],
                    'status': row['status'],
                    'effective_date': row['effective_date'],
                    'termination_date': row.get('termination_date')
                }
                self.csp_lob_service.create_csp_lob(mapping_data)
                results['success'] += 1
            except Exception as e:
                results['failed'] += 1
                results['errors'].append({
                    'row': idx + 1,
                    'error': str(e)
                })
                logger.error(f"Import error at row {idx + 1}: {str(e)}")

        return results 