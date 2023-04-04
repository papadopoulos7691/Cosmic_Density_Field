#!/bin/bash
#SBATCH -p all
#SBATCH --job-name=overdensities
#SBATCH -o Logs/overdens.log
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=12
#SBATCH --time=5-00:00:00
##SBATCH --mem=128G 
# email notifications (NONE, BEGIN, END, FAIL, REQUEUE, ALL) 
#SBATCH --mail-type=All 
#SBATCH --mail-user=s1838846@ed.ac.uk
#################
ntasks=1
nthreads=12

cd ${SLURM_SUBMIT_DIR} 

source /home/brs/tmox/tmox_conda
tmox_activate
conda activate yt

srun -n ${ntasks} -c ${nthreads} python Overdensities.py
