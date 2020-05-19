#!/bin/bash
python main.py tournament --max-threads 2 --sigma-threshold 0.85 --config 50_50_temp_mcts_minimax
python main.py tournament --max-threads 2 --sigma-threshold 0.85 --config 50_50_mcts_minimax
python main.py tournament --max-threads 2 --sigma-threshold 0.85 --config 50_50_500_mcts_minimax
