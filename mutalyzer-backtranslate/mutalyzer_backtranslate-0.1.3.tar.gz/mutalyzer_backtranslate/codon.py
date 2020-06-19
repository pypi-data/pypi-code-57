from Bio.Data import CodonTable


for i in CodonTable.unambiguous_dna_by_id.keys():
    table = CodonTable.unambiguous_dna_by_id[i]
    forward_table = table.forward_table
    stop_codons = table.stop_codons

    if not set(forward_table.keys()) & set(stop_codons):
        full_table = sorted(
                list(forward_table.items()) + 
                list(map(lambda x: (x, '*'), stop_codons)))

        table_string = ''.join(map(lambda x: x[1], full_table))

        print('{:2d}: {} ({})'.format(i, table_string, len(full_table)))
    else:
        print('{:2d}: error'.format(i))
