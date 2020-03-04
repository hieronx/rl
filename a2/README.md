# Reinforcement Learning
Codebase for assignment 1 of the Reinforcement Learning course at Leiden University, by Mees Gelein (s1117378) and Jeroen Offerijns (s1738291).

## Setup
To install the Pip dependencies:

```pip install -r requirements.txt```

## How to use
To print the instructions on how to use the program:

```python main.py -h```

To run the unit tests:

```python test.py```

## Section 3 - Search
```python main.py play --eval random --depth 3 --disable-tt```

## Section 4 - Eval
```python main.py play --eval Dijkstra --depth 3 --disable-tt```

## Section 5 - Experiment
```python main.py trueskill --config random-vs-Dijkstra```

## Section 6 - Iterative Deepening and Transposition Tables
```python main.py trueskill --config depth-vs-time-limit```