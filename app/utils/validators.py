"""Validation utilities"""
from app.models.yline import YLineItem
from typing import Optional
from app.models import YLine

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