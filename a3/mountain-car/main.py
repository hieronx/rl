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

score_requirement = -198
num_games_train = 10000
num_games_eval = 100
steps_per_game_train = 200
steps_per_game_eval = 200

def main():
    # Load training data
    if os.path.isfile("training_data.p"):
        logger.info("Loading training data from cache...")
        with open("training_data.p", "rb") as f:
            training_data = pickle.load(f)

    else:
        training_data = model_data_preparation(
            env, num_games_train, steps_per_game_train, score_requirement
        )
        with open("training_data.p", "wb") as training_data_file:
            pickle.dump(training_data, training_data_file)

    print(training_data[0])

    # Train model
    arr = np.array([previous_observation for previous_observation, _ in training_data])
    print(arr.shape)

    X = np.array([previous_observation for previous_observation, _ in training_data]).reshape(-1, len(training_data[0][0]))
    y = np.array([action for _, action in training_data]).reshape(-1, len(training_data[0][1]))
    model = build_model(input_size=len(X[0]), output_size=len(y[0]))

    model.fit(X, y, epochs=5)

    # Evaluate model
    scores = []
    choices = []
    for _ in progressbar(range(num_games_eval), "Evaluating"):
        score = 0
        previous_observation = []

        for _ in range(steps_per_game_eval):
            # Uncomment this line if you want to see how our bot playing
            env.render()

            # First perform a random action, and then start using the model to predict the next action
            if len(previous_observation) == 0:
                action = random.randrange(0, 2)
            else:
                action = np.argmax(
                    model.predict(previous_observation.reshape(-1, len(previous_observation)))[0]
                )

            observation, reward, done, _ = env.step(action)

            choices.append(action)
            previous_observation = observation
            score += reward

            if done: break

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
