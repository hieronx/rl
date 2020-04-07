import os
import sys
import time
import math
import random


def play_a_random_game_first(env, goal_steps):
    for step_index in range(goal_steps):
        #         env.render()
        action = env.action_space.sample()
        observation, reward, done, info = env.step(action)
        print("Step {}:".format(step_index))
        print("action: {}".format(action))
        print("observation: {}".format(observation))
        print("reward: {}".format(reward))
        print("done: {}".format(done))
        print("info: {}".format(info))
        if done:
            break
    env.reset()


def model_data_preparation(env, intial_games, goal_steps, score_requirement):
    training_data = []
    accepted_scores = []
    for game_index in progressbar(range(intial_games), desc="Preparing model data"):
        score = 0
        game_memory = []
        previous_observation = []
        for step_index in range(goal_steps):
            action = random.randrange(0, 3)
            observation, reward, done, info = env.step(action)

            if len(previous_observation) > 0:
                game_memory.append([previous_observation, action])

            previous_observation = observation
            if observation[0] > -0.2:
                reward = 1

            score += reward
            if done:
                break

        if score >= score_requirement:
            accepted_scores.append(score)
            for data in game_memory:
                if data[1] == 1:
                    output = [0, 1, 0]
                elif data[1] == 0:
                    output = [1, 0, 0]
                elif data[1] == 2:
                    output = [0, 0, 1]
                training_data.append([data[0], output])

        env.reset()

    print(accepted_scores)

    return training_data


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
