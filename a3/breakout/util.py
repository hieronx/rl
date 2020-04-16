import math
import os
import random
import sys
import time

import numpy as np


def to_grayscale(img):
    return np.mean(img, axis=2).astype(np.uint8)

def downsample(img):
    return img[::2, ::2]

def preprocess(img):
    return to_grayscale(downsample(img))

def transform_reward(reward):
    return np.sign(reward)

class Namespace:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

def sample_batch(replay_buffer, batch_size):
    random_start_idx = random.randint(0, len(replay_buffer) - 1)
    return [replay_buffer[idx % len(replay_buffer)] for idx in range(random_start_idx, random_start_idx + batch_size)]


# Based on https://stackoverflow.com/questions/3160699/python-progress-bar
def progressbar(
    it, desc="", position=None, size=None, start=0, total=None, file=sys.stdout
):
    """Rewrote our own progressbar to get rid of the dependency on tqdm. This is necessary to provide feedback on the progress."""
    count = total or len(it)

    def show(j, ips, sec_elapsed_total):
        _, columns = os.popen("stty size", "r").read().split()

        # Terminal width - description length - spacing - completed count - spacing - total count - spacing - time - ips
        width = size or (
            int(columns)
            - len(desc)
            - 5
            - len(str(start + j))
            - 1
            - len(str(count))
            - 2
            - 11
            - 10
            - len(str(int(ips)))
            - 1
        )

        min_elapsed, sec_elapsed = divmod(sec_elapsed_total, 60)
        sec_total = math.ceil(count / ips) - sec_elapsed_total if ips > 0 else 0
        min_rem, sec_rem = divmod(sec_total, 60)

        x = int(width * (start + j) / count)
        if position:
            moveto(file, position)
        file.write(
            "%s: |%s%s| %i/%i [%02d:%02d<%02d:%02d, %.2fit/s]\r"
            % (
                desc,
                "█" * x,
                " " * (width - x),
                start + j,
                count,
                min_elapsed,
                sec_elapsed,
                min_rem,
                sec_rem,
                ips,
            )
        )
        file.flush()
        if position:
            moveto(file, -position)

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
    """Moves the filepointer inside of a file, or file-like buffer like the console"""
    fp.write(str("\n" * n + ("" if (os.name == "nt") else "\x1b[A") * -n))
    fp.flush()
