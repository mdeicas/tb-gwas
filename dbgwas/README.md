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
