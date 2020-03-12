# Reinforcement Learning
Codebase for assignment 2 of the Reinforcement Learning course at Leiden University, by Mees Gelein (s1117378) and Jeroen Offerijns (s1738291).

## Setup
To install the Pip dependencies:

```pip install -r requirements.txt```

## How to use
To print the instructions on how to use the program:

```python main.py -h```

To run the unit tests:

```python test.py```

## Section 2 - MCTS Hex
```python main.py play mcts --num_iterations 5000```

## Section 3 - Experiment
```python main.py trueskill --config minimax-vs-mcts --plot```

## Section 4 - Tune
```python main.py tune```