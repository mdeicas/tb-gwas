# tb-gwas
This repository contains scripts, configs, and instructions to reproduce the 
results of a GWAS on tuberculosis transmissibility. 

## Requirements
- Docker 
- Python, matplotlib, and numpy 
- Slurm 
- Anaconda 
- git 

To run the scripts in this repo, replace all occurrences of `docker1` with 
`docker` and modify the file paths for your system. Slurm is used throughout
the repo, but code could be modified to remove that requirement. 


## Data Used 
This study used samples of *Mycobacterium tuberculosis* (private data). 
The raw data was processed to obtain mapped reads of SNPs and a phylogeny. 
All samples were tagged with binary transmissibility values inferred from
sizes of infection clusters. The following data files were used:
- pyseer: Moldova_SNPs_QC.vcf, Moldova_1834_SNPs.tree, allclusterPheno_0.0005.txt
- dbgwas: allclusterRankedPheno_0.0005.txt, individual (directory of fasta files for each sequence), Moldova_1834_SNPs.tree
- XGBOOST + SHAP: all_snps_filtered.fasta, allclusterRankedPheno_0.0005.txt, info.txt

## Instructions to reproduce
### Pyseer
1. Install Pyseer, with conda (https://pyseer.readthedocs.io/en/master/installation.html)
2. Clone this repo and set up working directories. 

```
git clone https://github.com/mdeicas/tb-gwas.git
cd tb-gwas/pyseer 
mkdir fixed_effects_wdir
mkdir enet_wdir
``` 
3. These scripts contain absolute file paths to data files and to anaconda. Before running, ensure 
that the file paths are updated, if necessary, to their corresponding locations on your system. 
4. Generate the distances matrix  
```
sbatch slurm_jobs/generate_distances.sh
```
5. Run the algorithms once the previous job has finished 
```
cd fixed_effects_wdir && sbatch ../slurm_jobs/fixed_effects_job.sh
cd ../enet_wdir && sbatch ../slurm_jobs/enet_model_job.sh
```
This results in two Manhattan Plots and SNPs sorted by p-values. 


### DBGWAS
To run the code, first have the necessary data files as specified by the README in the main repository. This should include:
- allclusterRankedPheno_0.0005.txt
- individual (directory containing fasta files for each sequence) 
- Moldova_1834_SNPs.tree

Once you have these data files, run the following commands:

```
docker pull leandroishilima/dbgwas
./create_final.sh
sbatch ./dbgwas.sh
```

This should submit the job to Slurm and you should get back a directory called output, which contains the DBGWAS output. To visualize, go to the visualizations directory within the output folder and go to index.html.

### XGBoost + SHAP
1. Create a Docker container with all the modules listed above, as well as XGBoost, SHAP, scipy, and sklearn.
2. Download and put your data files into a new directory. Our XGBoost-SHAP code uses three files, namely:
- all_snps_filtered.fasta (filtered TB sequences)
- allclusterRankedPheno_0.0005.txt (transmissability values)
- info.txt (major/minor bases)
3. Intialize your Docker container and run the python .py files, alternatively, use the slurm command sbatch to schedule the shell .sh files.
   - First run dmatrix.py to process the data and then calculate and save the data matrix.
   - Afterwards, use xgboost_shap.py to run the xgboost-shap algorithm, which will output a couple graphs documenting the model, a saved json representation of the model, validation scores at each iteration, and SHAP values. 
   - Use parameter_search.py to grid-search or fine-tune XGBoost parameters.
