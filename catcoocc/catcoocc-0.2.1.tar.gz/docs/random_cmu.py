import csv
import random

def write_sample(rows, size):
    sample = random.sample(rows, size)
    sample = sorted(sample, key=lambda k:k['Orthography'])
    with open("cmudict.sample%i.tsv" % size, "w") as handler:
        handler.write("Orthography\tSegments\n")
        for entry in sample:
            handler.write(entry['Orthography'])
            handler.write("\t")
            handler.write(entry['Segments'])
            handler.write("\n")

with open("cmudict.tsv") as handler:
    reader = csv.DictReader(handler, delimiter="\t")
    rows = [line for line in reader]

    write_sample(rows, 100)
    write_sample(rows, 1000)
