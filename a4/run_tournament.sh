#!/bin/bash
python main.py tournament --max-threads 2 --sigma-threshold 0.85 --config replay_buffer
python main.py tournament --max-threads 2 --sigma-threshold 0.85 --config training_length
python main.py tournament --max-threads 2 --sigma-threshold 0.85 --config dirichlet_alpha
python main.py tournament --max-threads 2 --sigma-threshold 0.85 --config still_not_working
python main.py tournament --max-threads 2 --sigma-threshold 0.85 --config finally_success