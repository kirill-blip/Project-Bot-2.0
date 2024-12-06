def validate_name(name: str) -> bool:
    if not name.isalpha():
        return False
    
    if not (3 <= len(name) <= 20):
        return False
    
    return True
