Convert `.csv` to `.fasta` with the following:
```bash
awk -F "," '$1 ~ /^Amanita/{print ">"$1"\r"$2}' Amanita_seq_pudlished.csv | sed 's/ /_/g' > pubd_seq.fa
```
Deduplicate with simple Seqkit operation:
```bash
AmanitaDiversity % seqkit rmdup -n < pubd_seq.fa > no_dup.fa

# [INFO] 217 duplicated records removed
```
Seqkit has issues, and for some reason does NOT remove duplicates. Accordingly, we'll use a python script to parse and remove the duplicate entries. 
```python
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
```
Above script actually results in removal of duplicate sequences, but will not remove entries with duplicate names. Accordingly, the following script can be used: 
```python
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
```


Use ITSx to extract the ITS region from each deduplicated sequence. I'm lazy and there aren't that many sequences, so we'll just HMMs implemented in ITSx 
```bash
ITSx -i no_dup.fa -o no_dup_ITS1 # does not work 
```
ITSx doesn't work well for *Amanita* sequences, which have a number of common and large in/dels at the rDNA cistron. I'll proceed with making a blast database for a reciprocal all-v-all blast.
```bash
makeblastdb -dbtype nucl -in no_dup.fa -parse_seqids -title "Amanita rDNA" -out Amanita_no_dup
```
We'll blast the full published seq set against this database. 
```bash
blastn -query pubd_seq.fa -db /Users/corbinbryan/Desktop/AmanitaDiversity/Amanita_no_dup -outfmt 6 -out full_v_nodup.tsv -max_target_seqs 1
```
