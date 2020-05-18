#!/bin/bash
cp alphazero/config_150it.yaml alphazero/config.yaml
python main.py train alphazero > output_150it.txt

cp alphazero/config_da2.2.yaml alphazero/config.yaml
python main.py train alphazero > output_da2.2.txt

poweroff