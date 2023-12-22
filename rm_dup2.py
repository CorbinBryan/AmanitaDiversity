from Bio import SeqIO
import sys

input_file = sys.argv[1]
output_file = sys.argv[2]

seen_ids = set()
records = []

for record in SeqIO.parse(input_file, "fasta"):
    if record.id not in seen_ids:
        seen_ids.add(record.id)
        records.append(record)
    else:
        print(f"Duplicate sequence name found and excluded: {record.id}")

SeqIO.write(records, output_file, "fasta")