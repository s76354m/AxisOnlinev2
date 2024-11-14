"""Validation utilities"""
from app.models.yline import YLineItem

def validate_yline_item(item: YLineItem) -> bool:
    """Validate Y-Line item"""
    if not item.ipa_number:
        raise ValueError("IPA number is required")
    
    if not item.product_code:
        raise ValueError("Product code is required")
    
    if item.pre_award and item.post_award:
        raise ValueError("Item cannot be both pre-award and post-award")
    
    return True 