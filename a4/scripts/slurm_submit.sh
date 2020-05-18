#!/bin/sh

#SBATCH --partition=gpu-medium
#SBATCH --ntasks=1
#SBATCH --ntasks-per-node=1
#SBATCH --gres=gpu:1
#SBATCH --time=24:00:00
#SBATCH --export=none
#SBATCH --signal=SIGUSR1@90
#SBATCH --cpus-per-task=6

export HOME_DIR="/home/s1738291/rl-a4"
export JOB_DIR="/data/s1738291/rl-a4"

cd $HOME_DIR
module load PyTorch/1.3.1-fosscuda-2019b-Python-3.7.4

pip install --user  trueskill==0.4.5 \
    matplotlib==3.1.3 \
    pandas==1.0.1 \
    scikit-learn==0.22.2 \
    numpy==1.18.4 \
    PyYAML==5.3.1

python main.py train alphazero