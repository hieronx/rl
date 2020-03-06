import os
import sys
import time

def cls():
    """Clears the screen, depending on the OS level call, this is merely a small utility function"""
    if os.name == 'nt':
        temp = os.system('cls')
    else:
        temp = os.system('clear')

# Based on https://stackoverflow.com/questions/3160699/python-progress-bar
def progressbar(it, desc="", position=None, size=80, file = sys.stdout):
    count = len(it)

    def show(j, ips):
        x = int(size*j/count)
        if position: moveto(file, position)
        file.write("%s: |%s%s| %i/%i %.2fit/s\r" % (desc, "█"*x, " "*(size-x), j, count, ips))
        file.flush()
        if position: moveto(file, -position)

    start_time = time.time()
    show(0, 0)
    for i, item in enumerate(it):
        yield item
        ips = (i+1) / (time.time() - start_time)
        show(i+1, ips)
    
    file.write("\n")
    file.flush()

# Based on https://github.com/tqdm/tqdm/blob/master/tqdm/std.py#L1401
def moveto(fp, n):
    fp.write(str('\n' * n + ('' if (os.name == 'nt') else '\x1b[A') * -n))
    fp.flush()