import os
import sys
import time
import math
import random
import time

def cls():
    """Clears the screen, depending on the OS level call, this is merely a small utility function"""
    if os.name == 'nt':
        temp = os.system('cls')
    else:
        temp = os.system('clear')

def model_data_preparation(env, num_games, steps_per_game, score_requirement):
    training_data = []

    for _ in progressbar(range(num_games), desc="Preparing model data"):
        score = 0
        game_memory = []
        previous_observation = []

        for _ in range(steps_per_game):
            action = random.randrange(0, 3)
            observation, reward, done, _ = env.step(action)

            # This is going in the right direction, so we should reward it
            if observation[0] > -0.2: reward = 1

            game_memory.append((previous_observation, action))
            previous_observation = observation
            score += reward
            
            if done: break

        if score >= score_requirement:
            for previous_observation, action in game_memory:
                if len(previous_observation) > 0:
                    # Turn into one-hot encoding
                    output = [0, 0, 0]
                    output[action] = 1
                    
                    # Store tuple of "what was observed and which action was undertaken"
                    training_data.append((previous_observation, output))

        env.reset()

    return training_data

class Namespace:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


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
