# modeling the stochastic nature of alternative splicing
## manifest
### apc/
code that generates all possible combinations of isoforms from a given gene
default icost is derived from code in icost/
+ apc_isogen.py
	+ runs apc algorithm on a single gene
+ apc_model_lib.py
 	+ contains functions that are used to generate apc isoforms and probabilistic models
+ make_models.py
  	+ creates .tsv files for acceptor/donor pwms, exon/intron Markov models, and exon/intron length models
+ multi_apc.py
 	+ parallelizes apc_isogen.py to be used on every gene in the apc dataset
+ write_apc_cmds.py
	+ writes a text file with commands to be run in parallel  	   
### icost/
code that calculates the best intron cost for scoring isoforms
+ apc_pickler.py
	+ creates .pkl files from the output of aml.apc()
  	+ takes one gene as input
+ apc_score.py
	+ uses single a .pkl and fasta file
 	+ scores each isoform and writes to stout in gff format
+ icost_scoring.py
	+ returns .json file with all scored isoforms and tested icost values
	+ uses apc_score.py to score isoforms
+ mdist_lib.py
	+ functions to be called in icost_scoring.py
 + run_apc_pickler.py
  	+ creates .pkl files for all genes
	+ uses apc_pickler.py
+ avg_mdist.py
 	+ takes .json file from icost_scoring.py
	+ returns average Manhattan distance for each tested icost across all genes/isoforms
	+ view output to pick best icost
### gff_analysis/
code that parses through apc results and organizes isoforms
### mkmdls_out/
output of make_models.py in apc/, includes .tsv files for position weight 
matrix, Markov model and length models
### results/
code that generates svg/html files to view genes and isoforms, written by Ian
### data/
contains curated dataset for apc analysis, apc generated gff files and training sequences for apc models
### other/
stuff im trying to learn
## recipes
### unzipping files to be used
```
cd data/
mkdir build/
tar -xvf file.tar.gz -C build/
gunzip file.txt.gz -c > build/file.txt
```
### train probabilistic models
```
mkdir mkmdls_out/
cd apc/
python3 make_models.py --extxt ../data/build/exon.txt --intxt ../data/build/intron.txt --len_limit 500 --dntxt ../data/build/donor.txt --actxt ../data/build/acceptor.txt --outdir ../mkmdls_out/
```
### calculate icost
```
cd icost/
ln -s ../apc/apc_model_lib.py
python3 run_apc_pickler.py ../data/build/apc/ --outdir /home/ismael/Data/
python3 icost_scoring.py /home/ismael/Data/apc_pickles/ ../data/build/apc/ --exon_len ../mkmdls_out/exon_len.tsv --intron_len ../mkmdls_out/intron_len.tsv --intron_mm ../mkmdls_out/intron_mm.tsv --exon_mm ../mkmdls_out/exon_mm.tsv --intron_mm ../mkmdls_out/intron_mm.tsv --donor_pwm ../mkmdls_out/donor_pwm.tsv --acceptor_pwm ../mkmdls_out/acceptor_pwm.tsv --icost_range_up 50 --icost_step 1
```

### generate apc isoforms
```
cd apc/
python3 write_apc_cmds.py ../data/build/apc/ --outfile apc_cmds.txt --gff_out /home/ismael/Data/apcgen_gffs/ --gff_name apcgen.ws290 --exon_len ../mkmdls_out/exon_len.tsv --intron_len ../mkmdls_out/intron_len.tsv --exon_mm ../mkmdls_out/exon_mm.tsv --intron_mm ../mkmdls_out/intron_mm.tsv --donor_pwm ../mkmdls_out/donor_pwm.tsv --acceptor_pwm ../mkmdls_out/acceptor_pwm.tsv
python3 multi_apc.py apc_cmds.txt --cpus #
```
write_apc_cmps.py will output a text file with commands to run in multi_apc.py
make sure openturns is importable for apc_model_lib.py so apc runs correctly

need apc pickler
then icost scoring
then avg mdis


### arch/
+ old apc code
### arch2/ 
+ testing and devolpment scripts for rewriting apc code
## Directions for icost testing ##
+ apc_pickler.py
  	+ single apc gene fasta file as input
	+generates apc isoform .pkl files
  	+ places .pkl file in apc_pickles/
+ apc_score.py
  	+ scores isoforms in apc .pkl files
  	+ input single .pkl file
  	+ output single .gff file
+ icost_testing.py
  	+ input directory with apc pickle files
  	+ input directory with apc fasta files
  	+ input scoring model .tsv files
  	+ imports apc_score.py
     
## MANIFEST ##
### splicing/
+ modelib.py - apc function library
+ make_models.py - generates probabilistic models
+ pwm_scoring.py - scores donor and acceptor sites with pwm
+ isotyper.py - categorizes isoforms
### splicing/data/
+ copied from arch/
+ apc dataset, exon/intron sequences, donor/acceptor sequences
### splicing/mkmdls_out/
+ output of make_models.py
+ .tsv files for each model
### splicing/results/
+ output from Ian's code
+ svg files
+ kinda forget how this works
### splicing/arch/
+ isoform.py - library for most functions
+ geniso - generates isoforms
+ cmpiso - compares isoforms
+ optiso - optimizes parmeters for geniso
+ randomly.py - examines splicing in random sequences
+ data - directory training data and scripts
	+ extract_sequences.py - uses Lyman2020 favorites
	+ build_models.py - creates pwms, etc
 ### splicing/arch2/
 + devlopment scripts for apc rewrite



## To Do ##
- Compare Ian's apc code to rewrite
- Compare RNA-seq data with simulated data
- Compare RNA-seq data with gff-generated isoforms (biologically likely)
- Compare simulated data with gff-generated isoforms (biologically likely)
- Describe differences between APC 668 and WormBase, see (ask permission to view):
	https://docs.google.com/spreadsheets/d/1tzfDo145Nt0MtEyEqy__WnaV-PtKA79LN6mrsWuZbt0/edit#gid=0
