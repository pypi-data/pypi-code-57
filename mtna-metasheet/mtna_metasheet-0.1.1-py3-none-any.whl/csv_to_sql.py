import argparse
import os
import sys

record_index=0
field_count_header=0
field_count_min=0
field_count_max=sys.maxsize

args = None

def process_header(line_in):
    global field_count_header
    field_count_header = len(line_in.split(','))
    return line_in

def process_line(line_in):
    line_out = ""
    field_index = 0
    is_new_field = True
    for char_index, char in enumerate(line_in):
        if is_new_field:
            field_index += 1
            value_index = 0
            is_quoted = 0
            is_new_field = False
        value_index += 1
        if char == args.delimiter:
            if value_index == 1:
                # this value is empty, insert NULL
                line_out += "NULL"
                is_new_field = True
            elif not is_quoted:
                # this is the end of the field
                is_new_field = True
            else:
                # ignore delimiter in quoted value
                pass
        elif char==args.quotechar:
            if value_index==1:
                # this value is quoted
                is_quoted = 1 
            elif is_quoted == 1 and line_in[char_index+1] == args.quotechar:
                is_quoted += 1
            else:
                is_quoted -= 1
        line_out += char
    #print(record_index, field_index)
    if field_index != field_count_header:
        pass
        raise Exception("Field count mismatch")
    return line_out

def convert(f,delimiter=",",newline='',quotechar='"'):
    global record_index
    infile = open(f, newline=newline, encoding=args.encoding)
    outfile = open(os.path.splitext(f)[0]+".sql.csv","w",newline=newline, encoding='utf8')
    line = infile.readline()
    if not args.noheader:
        outfile.write(process_header(line))
        line = infile.readline()
    record_index = 1
    while line:
        if record_index % 1000 == 0:
            print(record_index)
        if args.start >= record_index:
            continue;
        newline = process_line(line)
        outfile.write(newline)
        line = infile.readline()
        record_index += 1
    outfile.close()
    infile.close()

# MAIN
if __name__ == '__main__':
    """Main"""
    parser = argparse.ArgumentParser()
    parser.add_argument("infile",nargs='+')
    parser.add_argument("-d","--delimiter", default=',')
    parser.add_argument("-e","--encoding", default='latin1')
    parser.add_argument("-qc","--quotechar", default='"', help="Quote character")
    parser.add_argument("-nh","--noheader", action='store_true')
    parser.add_argument("-s","--start", default=0)
    parser.add_argument("-n","--nrecords", help="Number of records to process")
    args = parser.parse_args()

    print(args)

    for f in args.infile:
        convert(f)
