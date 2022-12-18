#!/bin/bash
#SBATCH --job-name=pyseer
#SBATCH --output=job.out
#SBATCH --time=60

phenotypes="/workdir/moldova/transmission/cluster/allclusterPheno_0.0005.txt" 
vcf="/workdir/moldova/base_data/Moldova_SNPs.vcf"
distances="../distances.tsv"
out="assoc.out"

echo "Starting Job"
source /programs/miniconda3/bin/activate pyseer	
srun pyseer --phenotypes $phenotypes --vcf $vcf --distances $distances --min-af 0.02 --max-af 0.98 > $out
# sort by p-value to easily see significant SNPs
source ../analyze_data/process_output.sh $out
# plot
source ../analyze_data/plot.sh 
python3 ../analyze_data/plot.py 
conda deactivate
echo "Finished Job"
