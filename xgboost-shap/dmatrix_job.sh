#!/bin/bash
#
#SBATCH --job-name=dmatrix_job
#SBATCH --output=dmatrix_job_output.txt
#
#SBATCH --ntasks=1
#SBATCH --time=04:00:00
#SBATCH --mem=16G
docker1 run biohpc_wl428/xgb-shap python /workdir/dmatrix_prep.py -fm /workdir/data/all_snps_filtered.fasta -fv /workdir/allclusterRankedPheno_0.0005.txt -fi /workdir/data/info.txt