#!/bin/bash
#SBATCH --time=5:00:00
#SBATCH --mem=32GB
#SBATCH -p russpold
#SBATCH --mail-type=ALL
#SBATCH --mail-user=joke.durnez@gmail.com
#SBATCH --output=unknownpleasures_extract.log
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=8

# load singularity
module load system
module load singularity/2.6.0

# define constants
export IMAGE=/share/PI/russpold/singularity_images/poldracklab_fmriprep_1.1.5-2018-09-07-1bd26e6330e0.img
export BASEDIR=/scratch/users/jdurnez/myconnectome/ # bids directory with myconnectome data
export SCRIPTLOC=/home/users/jdurnez/myconnectome/unknownpleasures_extract.py

export PYTHONPATH=""
singularity exec $IMAGE python -u $SCRIPTLOC --basedir=$BASEDIR
