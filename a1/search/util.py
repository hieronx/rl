from os import system, name

def cls():
    return None
    """Clears the screen, depending on the OS level call"""
    if name == 'nt':
        temp = system('cls')
    else:
        temp = system('clear')