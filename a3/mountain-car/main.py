import gym
import random, pickle, os, logging
import numpy as np

from model import build_model
from util import model_data_preparation, progressbar

logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%H:%M:%S",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

env = gym.make("MountainCar-v0")
env.reset()
goal_steps = 200
score_requirement = -198
intial_games = 10000


def main():
    # Load training data
    if os.path.isfile("training_data.p"):
        logger.info("Loading training data from cache...")
        with open("training_data.p", "rb") as f:
            training_data = pickle.load(f)

    else:
        training_data = model_data_preparation(
            env, intial_games, goal_steps, score_requirement
        )
        with open("training_data.p", "wb") as training_data_file:
            pickle.dump(training_data, training_data_file)

    # Train model
    X = np.array([i[0] for i in training_data]).reshape(-1, len(training_data[0][0]))
    y = np.array([i[1] for i in training_data]).reshape(-1, len(training_data[0][1]))
    model = build_model(input_size=len(X[0]), output_size=len(y[0]))

    model.fit(X, y, epochs=5)

    # Evaluate model
    scores = []
    choices = []
    for each_game in progressbar(range(100), "Evaluating"):
        score = 0
        prev_obs = []
        for step_index in range(goal_steps):
            # Uncomment this line if you want to see how our bot playing
            #         env.render()
            if len(prev_obs) == 0:
                action = random.randrange(0, 2)
            else:
                action = np.argmax(
                    model.predict(prev_obs.reshape(-1, len(prev_obs)))[0]
                )

            choices.append(action)
            new_observation, reward, done, info = env.step(action)
            prev_obs = new_observation
            score += reward
            if done:
                break

        env.reset()
        scores.append(score)

    print(scores)
    print("Average Score:", sum(scores) / len(scores))
    print(
        "choice 1:{}  choice 0:{} choice 2:{}".format(
            choices.count(1) / len(choices),
            choices.count(0) / len(choices),
            choices.count(2) / len(choices),
        )
    )


if __name__ == "__main__":
    main()
