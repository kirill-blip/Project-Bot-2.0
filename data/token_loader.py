import os
import json

def TryParseToken():
    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        token_file_path = os.path.join(current_dir, 'tokens.json')
        
        with open(token_file_path, 'r') as f:
            token = f.read().strip()
            
        return True
    except:
        pass
    
    return False
    
def ParseToken(bot_type:str):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    token_file_path = os.path.join(current_dir, 'tokens.json')
        
    with open(token_file_path, 'r') as f:
        tokens = json.load(f)
            
    return tokens[bot_type]