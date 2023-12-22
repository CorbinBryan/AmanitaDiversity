from Bio import SeqIO
import sys
import os 

input_file = sys.argv[1]
output_file = sys.argv[2]

seen = set()
records = []

for record in SeqIO.parse(input_file, "fasta"):  
    if record.seq not in seen:
        seen.add(record.seq)
        records.append(record)

SeqIO.write(records, output_file, "fasta")