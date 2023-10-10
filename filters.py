
async def hasWords(text: str, key_words: list):     
    text = text.split(' ')
        
    if len(key_words) == 0:
        return True

    for word in key_words:
        for string in text:
            if str(word).lower() == string.lower():
                return True
    
    return False
