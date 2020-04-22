import os
import pickle
import random
import sys
import time

import numpy as np
import tensorflow as tf


def load_from_saved_state():
    folder = 'breakout/output/'

    print("Loading meta data from saved training state...")
    with open(folder + 'meta.p', "rb") as f:
        start_iteration, stats = pickle.load(f)
    
    print('Start iteration is %d' % start_iteration)

    print("Loading model from saved training state...")
    model = tf.keras.models.load_model(folder + 'model.h5')
    target_model = tf.keras.models.load_model(folder + 'model.h5')

    print("Loading replay buffer from saved training state...")
    with open(folder + 'replay_buffer.p', "rb") as f:
        replay_buffer = pickle.load(f)
    
    return start_iteration, stats, model, target_model, replay_buffer

def to_grayscale(img):
    """Converts the second axis of RGB color (GREEN) to a 8-bit unsigned integer 0-255, this is done to save memory"""
    return np.mean(img, axis=2).astype(np.uint8)

def downsample(img):
    """Grabs half of all the pixels, making the input of the neural network a little smaller"""
    return img[::2, ::2]

def preprocess(img):
    """Does the full preprocess process on the provided image RGB array. This includes downsampling and grayscale"""
    return to_grayscale(downsample(img))

def moveto(fp, n):
    """
    Moves the filepointer inside of a file, or file-like buffer like the console
    Based on https://github.com/tqdm/tqdm/blob/master/tqdm/std.py#L1401
    """
    fp.write(str("\n" * n + ("" if (os.name == "nt") else "\x1b[A") * -n))
    fp.flush()

def get_epsilon_for_iteration(iteration, num_total_steps):
    """Returns the given epsilon for the provided iteration and num_total_steps"""
    if iteration > num_total_steps * 0.1: return 0.1
    else: return 0.9 * (1.0 - (iteration / (num_total_steps * 0.1))) + 0.1


# Based on https://stackoverflow.com/questions/3160699/python-progress-bar
def progressbar(it, desc="", position=None, size=None, start=0, total=None, file=sys.stdout):
    """Rewrote our own progressbar to get rid of the dependency on tqdm. This is necessary to provide feedback on the progress."""
    count = total or len(it)

    def show(j, ips, sec_elapsed_total):
        # f = os.popen("stty size", "r")
        # _, columns = f.read().split()
        # f.close()

        columns = 120

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
        sec_total = int((count / ips) + 1) - sec_elapsed_total if ips > 0 else 0
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
    
class Namespace:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
