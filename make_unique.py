from Bio import SeqIO
import sys

input_file = sys.argv[1]
output_file = sys.argv[2]

seen_headers = set()
records = []

for record in SeqIO.parse(input_file, "fasta"):
    original_header = record.id
    species = original_header.split('_')[-1]  # Extracting the species epithet
    new_header = f"{original_header}_{len(seen_headers) + 1}"  # Appending an integer

    while new_header in seen_headers:
        new_header = f"{original_header}_{len(seen_headers) + 1}"

    seen_headers.add(new_header)
    record.id = new_header
    record.description = ""  # Clear the description to keep only the modified header
    records.append(record)

SeqIO.write(records, output_file, "fasta")