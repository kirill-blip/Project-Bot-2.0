def validate_phone(phone: str) -> bool:
    if phone.startswith("+"):
        phone = phone[1:]
    
    if not phone.isdigit():
        return False
    
    if not (10 <= len(phone) <= 15):
        return False
    
    return True
