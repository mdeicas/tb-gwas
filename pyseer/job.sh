#!/bin/bash
#SBATCH --job-name=pyseer
#SBATCH --output=job.out
#SBATCH --time=60

phenotypes="/workdir/moldova/transmission/cluster/allclusterPheno_0.0005.txt" 
vcf="/workdir/moldova/base_data/Moldova_INDELs_QC.vcf"
distances="/workdir/mdd227/data/distances.tsv"
out="assoc.out"

echo "Starting Job"
source /programs/miniconda3/bin/activate pyseer	
srun pyseer --phenotypes $phenotypes --vcf $vcf --distances $distances --min-af 0.02 --max-af 0.98 > $out
conda deactivate
echo "Finished Job"