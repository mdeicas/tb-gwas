#!/bin/bash
#
#SBATCH --job-name=xgboost_shap_job
#SBATCH --output=xgboost_shap_job_output.txt
#
#SBATCH --ntasks=1

docker1 run biohpc_wl428/xgb-shap-plt python /workdir/xgboost_shap.py