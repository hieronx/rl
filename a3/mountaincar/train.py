import logging
import random

import gym
import numpy as np
from stable_baselines.common import make_vec_env, set_global_seeds
from stable_baselines.common.vec_env import SubprocVecEnv

from mountaincar.model import build_model, get_best_action
from mountaincar.util import Namespace, create_random_training_data, progressbar

def train(args):
    """Starts training with the one and only number as the random seed"""
    np.random.seed(42)

    # Load training data
    training_data = create_random_training_data(args)

    # Train model`
    X = np.array([previous_observation for previous_observation, _ in training_data]).reshape(-1, len(training_data[0][0]))
    y = np.array([action for _, action in training_data]).reshape(-1, len(training_data[0][1]))
    model = build_model(input_size=len(X[0]), output_size=len(y[0]))

    model.fit(X, y, epochs=5)
    evaluate(model, args)

def evaluate(model, args):
    """Starts evaluation on the provided model"""
    total_scores = []
    
    env = make_vec_env("MountainCar-v0", n_envs=args.num_threads, seed=0)
    env.seed(42)

    for _ in progressbar(range(args.num_games_eval // args.num_threads), "Evaluating"):
        rewards = [0] * args.num_threads
        previous_observations = env.reset()
        done_envs = [False] * args.num_threads

        for step_id in range(args.steps_per_game_eval):

            actions = [get_best_action(observation) for observation in previous_observations]

            new_observations, _, dones, _ = env.step(actions)
                        
            new_rewards = [0 if (dones[env_id] == True or done_envs[env_id] == True) else -1 for env_id, _ in enumerate(dones)]

            for env_id, _ in enumerate(dones):
                if dones[env_id] == True:
                    done_envs[env_id] = True

            previous_observations = new_observations
            rewards = np.add(rewards, new_rewards)

        total_scores.extend(rewards)

    print("Average score:", sum(total_scores) / len(total_scores))
