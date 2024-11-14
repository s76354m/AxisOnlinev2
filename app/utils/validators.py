"""Validation utilities"""
from app.models.yline import YLineItem
from typing import Optional
from app.models import YLine
from datetime import datetime
from fastapi import HTTPException
from app.models.csp_lob import CSPLOB, LOBType, CSPStatus

def validate_yline_item(item: YLineItem) -> bool:
    """Validate Y-Line item"""
    if not item.ipa_number:
        raise ValueError("IPA number is required")
    
    if not item.product_code:
        raise ValueError("Product code is required")
    
    if item.pre_award and item.post_award:
        raise ValueError("Item cannot be both pre-award and post-award")
    
    return True 

def validate_ipa_number(ipa_number: str) -> bool:
    """Validate IPA number format"""
    if not ipa_number:
        return False
    # Add specific IPA number format validation rules
    return True

def validate_y_line_values(estimated_value: Optional[float], actual_value: Optional[float]) -> bool:
    """Validate Y-Line monetary values"""
    if estimated_value is not None and estimated_value < 0:
        return False
    if actual_value is not None and actual_value < 0:
        return False
    return True 

class CSPLOBValidator:
    @staticmethod
    def validate_dates(
        effective_date: datetime,
        termination_date: Optional[datetime]
    ) -> bool:
        """Validate effective and termination dates"""
        if termination_date and effective_date > termination_date:
            raise ValueError("Effective date must be before termination date")
        return True

    @staticmethod
    def validate_csp_code(csp_code: str) -> bool:
        """Validate CSP code format"""
        if not csp_code or len(csp_code) < 3:
            raise ValueError("CSP code must be at least 3 characters")
        if not csp_code.isalnum():
            raise ValueError("CSP code must be alphanumeric")
        return True

    @staticmethod
    def validate_status_transition(
        current_status: CSPStatus,
        new_status: CSPStatus
    ) -> bool:
        """Validate status transitions"""
        invalid_transitions = {
            CSPStatus.INACTIVE: [CSPStatus.PENDING],
            CSPStatus.ACTIVE: [CSPStatus.PENDING]
        }
        
        if current_status in invalid_transitions and \
           new_status in invalid_transitions[current_status]:
            raise ValueError(f"Invalid status transition from {current_status} to {new_status}")
        return True

    @staticmethod
    def validate_lob_compatibility(
        project_id: int,
        lob_type: LOBType,
        db_session
    ) -> bool:
        """Validate LOB type compatibility with project"""
        # Add project-specific validation logic here
        return True