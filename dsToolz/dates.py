def cleanOutOfBoundDates(string: str) -> str:
    
    if string == 'None':
        return None
    elif int(string[:4]) > 2099:
        return None
    else:
        return string