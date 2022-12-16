#!/bin/bash
#SBATCH --job-name=genDists
#SBATCH --output=genDists.out
#SBATCH --time=60

echo "Starting Job"
source /programs/miniconda3/bin/activate pyseer	
srun python3 /programs/pyseer-1.3.10/scripts/phylogeny_distance.py /workdir/moldova/base_data/Moldova_1834_SNPs.tree > distances.tsv
conda deactivate
echo "Finished Job"
