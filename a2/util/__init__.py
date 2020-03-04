from os import system, name

def cls():
    """Clears the screen, depending on the OS level call, this is merely a small utility function"""
    if name == 'nt':
        temp = system('cls')
    else:
        temp = system('clear')