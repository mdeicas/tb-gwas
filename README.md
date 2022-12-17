# tb-gwas
This repository contains scripts, configs, and instructions to reproduce the 
results of a GWAS on tuberculosis transmissibility. 

## Requirements
- Docker (version) 
- Slurm

To run the scripts in this repo, replace all occurrences of `docker1` with 
`docker` and modify the file paths for your system. 


## Data Used 
This study used samples of *Mycobacterium tuberculosis* obtained from ____ in 
____. The raw data was processed to obtain mapped reads of SNPs and a phylogeny. 
All samples were tagged with discrete transmissibility values inferred from
sizes of infection clusters. The following data files were used:
- pyseer: Moldova_SNPs_QC.vcf, Moldova_1834_SNPs.tree, allclusterPheno_0.0005
- dbgwas: allclusterRankedPheno_0.0005.txt, individual (directory of fasta files for each sequence), Moldova_1834_SNPs.tree
- XGBOOST + SHAP:

## Instructions to reproduce
### Pyseer
Pyseer uses a matrix containing the phylogenetic distances between all pairs 
of samples to account for population structure. Use the `generate_distances.sh` 
slurm job script to generate this matrix from the phylogeny of the TB samples in 
newick-tree format. 

Next, use the `job.sh` slurm batch job script to run pyseer. The input is the SNPs
as a vcf file, the distance matrix generated in the previous step, and the 
phenotypes. 

The output is a list of samples with p-values, among other values. This output
file can be cleaned up and sorted by p-value for easier interpretation with 
the `process_output.sh` script. 

Finally, a manhattan plot can be created to visualize the results using `plot.py`.

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
