from Bio.Blast import NCBIWWW, NCBIXML
import os
import tqdm
import datetime
import sys

# Taxonomic information for microalgae, diatoms or cyanobacteria
#FROM: https://www.ncbi.nlm.nih.gov/taxonomy
taxon_query = (
    "(txid1117[ORGN] OR "  # Cyanobacteria
    "txid2836[ORGN] OR "  # Diatoms
    "txid3041[ORGN] OR "  # Chlorophyta (green algae)
    "txid2763[ORGN] OR "  # Rhodophyta (red algae)
    "txid2864[ORGN] OR "  # Dinoflagellates
    "txid2870[ORGN] OR "  # Phaeophyceae (brown algae)
    "txid261840[ORGN] OR " # Pyrophaceae
    "txid2825[ORGN] OR "  # Chrysophyceae (golden algae)
    "txid33849[ORGN])"     # Bacillariophyceae
)


# Search blast against PDB database
def run_blast(sequence, database):
    '''
    Runs BLASTP for a given sequence
    '''
    entrez_query = taxon_query if database in ['pdb_taxon', 'nr'] else None
    database = 'pdb' if database == 'pdb_taxon' else database
    result_handle = NCBIWWW.qblast('blastp', database, sequence,
                                   entrez_query=entrez_query,
                                   hitlist_size=500)
    return result_handle

# https://pmc.ncbi.nlm.nih.gov/articles/PMC3820096/
def parse_save_results(result_handle, output_filename, E_VALUE_THRESH=1e-10, IDENTITY_THRESH=0.30):
    blast_record = NCBIXML.read(result_handle)
    
    with open(output_filename, 'w') as txt_file:
        txt_file.write(f'{datetime.datetime.now()}\n\n')
        txt_file.write(f"Query Length: {blast_record.query_length}\n")
        txt_file.write(f"E-value threshold: {E_VALUE_THRESH}\n")
        txt_file.write(f"Identity threshold: {IDENTITY_THRESH}\n\n")
        
        hits_found = False
        for i, alignment in enumerate(blast_record.alignments, 1):
            for hsp in alignment.hsps:
                identity = float(hsp.identities) / float(hsp.align_length)
                e_value = hsp.expect  # E-value of the hit
                coverage = float(hsp.align_length) / float(blast_record.query_length)  # Query coverage

                # Check both the E-value and Identity threshold
                if e_value <= E_VALUE_THRESH and identity >= IDENTITY_THRESH:  
                    hits_found = True
                    txt_file.write(f"\nHit #{i}\n{'-'*30}\n")
                    txt_file.write(f"Title: {alignment.title}\n")
                    txt_file.write(f"Percent Identity: {identity:.2%}\n")
                    txt_file.write(f"Coverage: {coverage:.2%}\n")  # Added coverage info
                    txt_file.write(f"E-value: {e_value}\n")
                    txt_file.write(f"Query/Sbjct Length: {hsp.align_length}\n")
                    txt_file.write("Alignment:\n")
                    txt_file.write(f"Query: {hsp.query}\n")
                    txt_file.write(f"Match: {hsp.match}\n")
                    txt_file.write(f"Sbjct: {hsp.sbjct}\n\n")
        
        if not hits_found:
            txt_file.write("\nNo significant hits found meeting the E-value and Identity thresholds.\n")
def blast_result_exist(results_dir, filename):
    '''
    Check if BLAST already exist for a given sequence
    '''
    result_filename = os.path.join(results_dir, filename.replace('.fasta','.txt'))
    return os.path.exists(result_filename)

def main():
    if len(sys.argv) != 2:
        print('Usage: python BLAST_search <database>')
        print('Possible databases: pdb, pdb_taxon, nr')
        print('pdb: runs againt all the PDB database, to find possible templates for homology modeling')
        print('pdb_taxon: finds new potential enzymes with structure available')
        print('nr: runs againt the non-redundant database for microalgar, find potential new sequences ')

    database = sys.argv[1]
    if database not in ['pdb', 'pdb_taxon', 'nr']:
        print('Invalid database: pdb, pdb_taxon, nr')
        print('Possible databases: pdb, pdb_taxon, nr')
        print('pdb: runs againt all the PDB database, to find possible templates for homology modeling')
        print('pdb_taxon: finds new potential enzymes with structure available')
        print('nr: runs againt the non-redundant database for microalgar, find potential new sequences ')
    
    # Create results directory
    results_dir = f'blast_results/{database}'
    os.makedirs(results_dir, exist_ok=True)

    base_dir = 'sequences'
    count = 0
    for filename in tqdm.tqdm(os.listdir(base_dir)):
        filepath = os.path.join(base_dir, filename)
         
        if blast_result_exist(results_dir, filename):
            continue

        with open(filepath, 'r') as file:
            sequence = file.read()

        # Run BLAST search
        result_handle = run_blast(sequence, database)
        count += 1

        if result_handle:
            output_filename = os.path.join(results_dir, filename.replace('.fasta','.txt'))
            parse_save_results(result_handle, output_filename)

    print(f'\n\n {count} new BLAST searches completed.')
    print(f'\n\n\BLAST searches completes. Results saved in {results_dir}')

if __name__ == '__main__':
    main()
