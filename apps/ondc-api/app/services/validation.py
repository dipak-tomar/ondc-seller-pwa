from typing import Optional, Dict

HSN_GST_MAPPING: Dict[str, float] = {
    "0101": 0.0,
    "0201": 0.0,
    "0301": 5.0,
    "0401": 5.0,
    "0501": 12.0,
    "0601": 5.0,
    "0701": 0.0,
    "0801": 5.0,
    "0901": 5.0,
    "1001": 5.0,
    "1101": 5.0,
    "1201": 5.0,
    "1301": 5.0,
    "1401": 5.0,
    "1501": 12.0,
    "1601": 12.0,
    "1701": 5.0,
    "1801": 5.0,
    "1901": 18.0,
    "2001": 12.0,
    "2101": 18.0,
    "2201": 12.0,
    "2301": 5.0,
    "2401": 28.0,
    "2501": 5.0,
}

class ValidationService:
    @staticmethod
    def validate_hsn_code(hsn_code: str) -> tuple[bool, Optional[float], Optional[str]]:
        if not hsn_code:
            return False, None, "HSN code is required"
        
        hsn_code = hsn_code.strip()
        
        if len(hsn_code) < 4 or len(hsn_code) > 8:
            return False, None, "HSN code must be 4-8 digits"
        
        if not hsn_code.isdigit():
            return False, None, "HSN code must contain only digits"
        
        hsn_prefix = hsn_code[:4]
        gst_rate = HSN_GST_MAPPING.get(hsn_prefix)
        
        if gst_rate is None:
            return True, 18.0, None
        
        return True, gst_rate, None
    
    @staticmethod
    def get_gst_rate(hsn_code: str) -> float:
        if not hsn_code or len(hsn_code) < 4:
            return 18.0
        
        hsn_prefix = hsn_code[:4]
        return HSN_GST_MAPPING.get(hsn_prefix, 18.0)

validation_service = ValidationService()
