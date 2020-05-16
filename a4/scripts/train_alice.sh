export REMOTE_DIR="/home/s1738291/rl-a4"

rsync -a -P --info=progress2 --no-inc-recursive --exclude='/.git' --filter="dir-merge,- .gitignore" ./ hpc2:$REMOTE_DIR
ssh -t hpc2 'sbatch --chdir '"$REMOTE_DIR"' '"$REMOTE_DIR"'/scripts/slurm_submit.sh'
