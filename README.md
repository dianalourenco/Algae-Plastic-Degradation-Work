# Algae-Plastic-Degradation-Work
A bioinformatics pipeline for microalgae plastic-degrading enzyme analysis, including article search from Google Scholar, sequence retrieval from NCBI and BLAST analysis for microplastic biodegradation studies.

## 1. Articles Search with Google Scholar

### Script: *articles_search.py*

This script automates the process of searching and extracting article titles and URLs from Google Scholar using predefined keywords.

## Usage

### Running the Script
Execute the script from the command line:
```bash
python articles_search.py
```
### Output
The script saves articles in a file named ```articles.txt```. In the format:
```bash
####################
Articles searched on: YYYY-MM-DD HH:MM:SS
####################

1. Title: Example Article Title
   Link: https://example.com/article1

2. Title: Another Example Article
   Link: https://example.com/article2
```


## 2. NCBI Sequence Retrieval

### Script: *NCBI_seq_retrieval.py*

This script is design to retrieve protein sequences from the NCBI database on enzyme and species names provided in an input file.

## Usage

### Input File Format
The input file should be a plain text file with a comma-separated format:
```text
enzyme_name, species_name
example_enzyme, example_species
```
### Running the Script
Execute the script from the command line:
```bash
python NCBI_seq_retrieval.py input_file.txt
```
### Output
- The sequences are saved in the sequences directory.
- Each files contains the protein sequence in Fasta format.


## 3. BLAST Analysis

### Script: *BLAST_search.py*

This script is design to run a BLASTP search from the sequences available in the 'sequences' directory. 
It evaluates the potential of new plastic-degrading enzymes.

## Usage

### Running the Script
Execute the script from the command line:
```bash
python BLAST_search.py
```
### Output
- The BLAST results are saved in the 'blast_results' directory.
