import os
import sys
import time
import math

def cls():
    """Clears the screen, depending on the OS level call, this is merely a small utility function"""
    if os.name == 'nt':
        temp = os.system('cls')
    else:
        temp = os.system('clear')

# Based on https://stackoverflow.com/questions/3160699/python-progress-bar
def progressbar(it, desc="", position=None, size=None, start=0, total=None, file = sys.stdout):

    count = total or len(it)

    def show(j, ips, sec_elapsed_total):
        _, columns = os.popen('stty size', 'r').read().split()

        # Terminal width - description length - spacing - completed count - spacing - total count - spacing - time - ips
        width = size or (int(columns) - len(desc) - 5 - len(str(start + j)) - 1 - len(str(count)) - 2 - 11 - 12) 

        min_elapsed, sec_elapsed = divmod(sec_elapsed_total, 60)
        sec_total = math.ceil(count / ips) - sec_elapsed_total if ips > 0 else 0
        min_rem, sec_rem = divmod(sec_total, 60)
        
        x = int(width * (start + j) / count)
        if position: moveto(file, position)
        file.write("%s: |%s%s| %i/%i [%02d:%02d<%02d:%02d, %.2fit/s]\r" % (desc, "█" * x, " " * (width - x), start + j, count, min_elapsed, sec_elapsed, min_rem, sec_rem, ips))
        file.flush()
        if position: moveto(file, -position)

    start_time = time.time()
    show(0, 0, 0)
    for i, item in enumerate(it):
        yield item
        sec_elapsed = time.time() - start_time
        ips = (i + 1) / sec_elapsed
        show(i + 1, ips, sec_elapsed)
    
    file.write("\n")
    file.flush()

# Based on https://github.com/tqdm/tqdm/blob/master/tqdm/std.py#L1401
def moveto(fp, n):
    fp.write(str('\n' * n + ('' if (os.name == 'nt') else '\x1b[A') * -n))
    fp.flush()


def print_progressbar(desc="", completed=0, start_time=None, total=0, position=None, file=sys.stdout):
    _, columns = os.popen('stty size', 'r').read().split()

    # Terminal width - description length - spacing - completed count - spacing - total count - spacing - time - ips
    width = (int(columns) - len(desc) - 5 - len(str(completed)) - 1 - len(str(total)) - 2 - 11 - 13) 

    sec_elapsed_total = time.time() - start_time
    ips = completed / sec_elapsed_total

    min_elapsed, sec_elapsed = divmod(sec_elapsed_total, 60)
    sec_total = math.ceil(total / ips) - sec_elapsed_total if ips > 0 else 0
    min_rem, sec_rem = divmod(sec_total, 60)
    
    x = int(width * completed / total)
    if position: moveto(file, position)
    file.write("%s: |%s%s| %i/%i [%02d:%02d<%02d:%02d, %.2fit/s]\r" % (desc, "█" * x, " " * (width - x), completed, total, min_elapsed, sec_elapsed, min_rem, sec_rem, ips))
    file.flush()
    if position: moveto(file, -position)