from Bio import Entrez, SeqIO
import sys 
import os
import time 
import datetime

def fetch_protein_sequence(protein_name:str, species_name:str):
    '''
    Fetch protein sequences from NCBI database
    '''
    Entrez.email = "dianalourenco14@gmail.com"

    search_term = f"{protein_name} {species_name}"
    try:
        # Search for the protein
        handle = Entrez.esearch(db="protein", term=search_term, retmax=5)
        record = Entrez.read(handle)
        handle.close()

        if not record["IdList"]:
            print(f"No protein found for {protein_name} in {species_name}")
            return None
    
        protein_id = record["IdList"][0]
        # Fetch the protein sequence
        handle = Entrez.efetch(db="protein", id=protein_id, rettype="fasta", retmode="text")
        seq_record = SeqIO.read(handle, "fasta")
        handle.close()
        time.sleep(5)
        return seq_record

    except Exception as e:
        print(f'Error fetching protein for {protein_name} in {species_name}: {e}')


def save_seq_to_file(sequence_record, enzyme_name, species_name):
    '''
    Save sequence to a FASTA file
    '''
    #Makes directory
    os.makedirs('sequences', exist_ok=True)

    filename = f'{enzyme_name}_{species_name}'.replace(' ', '')
    filepath = os.path.join('sequences', f'{filename}.fasta')

    #Save sequence in FASTA format
    with open(filepath, 'w') as f:
        SeqIO.write(sequence_record,f,'fasta')
    return filepath

def main(file_path):    
    with open(file_path,'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    total_entries = len(lines[1:])
    processed = 0

    for line in lines[1:]:
        try:
            enzyme_name, species_name = [parts.strip() for parts in line.split(',')]
            processed += 1
            print(f'\nProcessing ({processed}/{total_entries}): {enzyme_name} from {species_name}')
                
            sequence_record = fetch_protein_sequence(enzyme_name, species_name)

            if sequence_record:
                filepath = save_seq_to_file(sequence_record, enzyme_name,species_name)
                print(f'Sequence saved to: {filepath}')
            time.sleep(1)
        except Exception as e:
            print(f'Error in input text file: {e}')


if __name__ == '__main__':
    input_file = sys.argv[1]
    main(input_file)