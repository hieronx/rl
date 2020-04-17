import logging
import os
import pickle
import random

import gym
import numpy as np
from stable_baselines.common import make_vec_env, set_global_seeds
from stable_baselines.common.vec_env import SubprocVecEnv

from mountaincar.model import build_model
from mountaincar.util import Namespace, model_data_preparation, progressbar

logger = logging.getLogger(__name__)

def train(args):
    # Load training data
    if os.path.isfile("training_data.p"):
        logger.info("Loading training data from cache...")
        with open("training_data.p", "rb") as f:
            training_data = pickle.load(f)

    else:
        env = gym.make("MountainCar-v0")
        env.reset()

        training_data = model_data_preparation(
            env, args.num_games_train, args.steps_per_game_train, args.score_requirement
        )
        with open("training_data.p", "wb") as training_data_file:
            pickle.dump(training_data, training_data_file)

    # Train model`
    X = np.array([previous_observation for previous_observation, _ in training_data]).reshape(-1, len(training_data[0][0]))
    y = np.array([action for _, action in training_data]).reshape(-1, len(training_data[0][1]))
    model = build_model(input_size=len(X[0]), output_size=len(y[0]))

    model.fit(X, y, epochs=20)

    # Evaluate model
    total_scores = []
    
    env = make_vec_env("MountainCar-v0", n_envs=args.num_threads, seed=0)

    for _ in progressbar(range(args.num_games_eval // args.num_threads), "Evaluating"):
        rewards = [0] * args.num_threads
        previous_observations = env.reset()
        done_envs = [False] * args.num_threads

        for step_id in range(args.steps_per_game_eval):
            # env.render('human')

            actions = [np.argmax(
                model.predict(previous_observation.reshape(-1, len(previous_observation)))[0]
            ) for previous_observation in previous_observations]

            new_observations, _, dones, _ = env.step(actions)
            
            new_rewards = [0 if (dones[env_id] == True or done_envs[env_id] == True) else -1 for env_id, _ in enumerate(dones)]

            for env_id, _ in enumerate(dones):
                if dones[env_id] == True:
                    done_envs[env_id] = True

            previous_observations = new_observations
            rewards = np.add(rewards, new_rewards)

        total_scores.extend(rewards)
        print("Average score:", sum(total_scores) / len(total_scores))

    print("Average score:", sum(total_scores) / len(total_scores))
