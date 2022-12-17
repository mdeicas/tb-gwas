#!/bin/bash
#
#SBATCH --job-name=dbgwas
#SBATCH --output=output.txt
#
#SBATCH --ntasks=1
#SBATCH --time=48:00:00
#SBATCH --mem=16G
docker1 run -v /workdir/jj523/:/jj523 leandroishilima/dbgwas:0.5.4 -strains /jj523/converted_text.txt -output /jj523/output -newick /jj523/base_data/Moldova_1834_SNPs.tree
