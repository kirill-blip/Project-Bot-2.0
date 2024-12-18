def validate_name(name: str) -> bool:
    if not name.isalpha():
        return False
    
    if not (2 <= len(name) <= 20):
        return False
    
    return True
