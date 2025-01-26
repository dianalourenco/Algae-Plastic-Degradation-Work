from Bio.Blast import NCBIWWW
import os
import datetime

def run_blast(sequence):
    '''
    Runs BLASTP for a given sequence
    '''
    result_handle = NCBIWWW.qblast('blastp', 'nr',sequence)
    return result_handle



def save_results(result_handle, output_filename):
    '''
    Save BLAST results to a file
    '''
    with open(output_filename, 'w') as f:
        f.write(result_handle.read())
    print(f'Results saved to {output_filename}')


def main():
    # Create results directory
    time = datetime.datetime.now().strftime('%Y%m%d')
    results_dir = f'blast_results_{time}'
    os.makedirs(results_dir, exist_ok=True)

    base_dir = 'sequences'



if __name__ == '__main__':
    main()