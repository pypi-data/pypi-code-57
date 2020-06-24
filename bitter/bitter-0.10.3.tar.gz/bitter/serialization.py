import tsv

class CSV:

    def __init__(self, outfile, fields=None, delimiter='\t', quoting=tsv.QUOTE_ALL, **kwargs):
        self.outfile = outfile
        writer = tsv.writer(outfile, quoting=quoting, delimiter=delimiter, **kwargs)
        if fields is None:
            # Print fields as header unless told otherwise
            print(delimiter.join(fields), file=outfile)
        fields = list(token.strip().split('.') for token in csv.split(','))

    def 
