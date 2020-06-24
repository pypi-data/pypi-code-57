# Copyright (c) 2010-2019 Andrew Dalke Scientific, AB (Sweden)
# See the contents of "chemfp/__init__.py" for full license details.

# This is backported from chemfp-3.1.

from __future__ import with_statement, print_function
import math
import sys
import itertools
import time
import re

import chemfp

from .. import argparse
from .. import io, SOFTWARE, bitops
from .. import search

from . import cmdsupport

# Suppose you have a 4K fingerprint.
#   1/4096 = 0.000244140625.
#   2/4096 = 0.00048828125
# You only need to show "0.0002" and "0.0005" to
# disambiguate the scores. I don't like seeing only
# the minimum resolution, so I also show at least
# the next bit.
#   For 4096 the float_formatter is %.5f and the
# above values are 0.00024 and 0.00049.
# This also prevents the results from being shown
# in scientific notation.
def get_float_formatter(num_bytes):
    num_digits = int(math.log10(num_bytes*8)) + 2
    float_formatter = "%." + str(num_digits) + "f"
    return float_formatter

def make_output_type(pattern, k=None, threshold=None):
    s = pattern % {"name": "Tanimoto", "k": k, "threshold": threshold}
    assert "None" not in s # safety check
    return s

def write_simsearch_magic(outfile):
    outfile.write(b"#Simsearch/1\n")

def write_count_magic(outfile):
    outfile.write(b"#Count/1\n")

def write_simsearch_header(outfile, d):
    lines = []
    for name in ("num_bits", "type", "software", "queries", "targets"):
        value = d.get(name, None)
        if value is not None:
            lines.append(("#%s=%s\n" % (name, value)).encode("utf8"))
    for name in ("query_sources", "target_sources"):
        for value in d.get(name, []):
            lines.append(("#%s=%s\n" % (name[:-1], value)).encode("utf8"))
    outfile.writelines(lines)

#### The NxM cases

# Helper class to keep track of the times
class ElapsedTime(object):
    __slots__ = ("read_time", "search_time", "output_time")
    def __init__(self):
        self.read_time = 0.0
        self.search_time = 0.0
        self.output_time = 0.0
    
def report_threshold(outfile, query_arenas, targets, threshold, elapsed_time):
    float_formatter = get_float_formatter(targets.metadata.num_bytes)
    def search_function(query_arena):
        return chemfp.threshold_tanimoto_search(query_arena, targets, threshold=threshold)
    _report_search(outfile, float_formatter, query_arenas, search_function, elapsed_time)

def report_knearest(outfile, query_arenas, targets, k, threshold, elapsed_time):
    float_formatter = get_float_formatter(targets.metadata.num_bytes)
    def search_function(query_arena):
        return chemfp.knearest_tanimoto_search(query_arena, targets, k=k, threshold=threshold)
    _report_search(outfile, float_formatter, query_arenas, search_function, elapsed_time)

def _report_search(outfile, float_formatter, query_arenas, search_function, elapsed_time):
    hit_formatter = "\t%s\t" + float_formatter
    search_time = output_time = 0.0
    start_time = time.time()
    for query_arena in query_arenas:
        t1 = time.time()
        result = search_function(query_arena)
        t2 = time.time()
        search_time += t2-t1
        for query_id, row in result:
            outfile.write(b"%d\t%s" % (len(row), query_id.encode("utf8")))
            for hit in row.get_ids_and_scores():
                outfile.write((hit_formatter % hit).encode("utf8"))
            outfile.write(b"\n") # XXX flush?
        t3 = time.time()
        output_time += t3-t2
    end_time = time.time()

    elapsed_time.search_time = search_time
    elapsed_time.output_time = output_time
    elapsed_time.read_time = (end_time - start_time) - (output_time + search_time)


def report_counts(outfile, query_arenas, targets, threshold, elapsed_time):
    search_time = output_time = 0.0
    start_time = time.time()
    for query_arena in query_arenas:
        t1 = time.time()
        counts = chemfp.count_tanimoto_hits(query_arena, targets, threshold)
        t2 = time.time()
        search_time += t2-t1
        for query_id, hit_count in counts:
            outfile.write(b"%d\t%s\n" % (hit_count, query_id.encode("utf8")))
        t3 = time.time()
        output_time += t3-t2
    end_time = time.time()

    elapsed_time.search_time = search_time
    elapsed_time.output_time = output_time
    elapsed_time.read_time = (end_time - start_time) - (output_time + search_time)


#### The NxN cases

class UnchangedDict(object):
    def __getitem__(self, x):
        return x

unchanged_dict = UnchangedDict()

class OriginalIds(object):
    def __init__(self, ids):
        self.ids = ids
    def __iter__(self):
        return iter(self.ids)
    def __getitem__(self, x):
        return x

def do_NxN_searches(args, k, threshold, target_filename):
    start_time = time.time()

    # load_fingerprints sorts the fingerprints based on popcount
    # I want the output to be in the same order as the input.
    # This means I need to do some reordering. Consider:
    #   0003  ID_A
    #   010a  ID_B
    #   1000  ID_C
    # I use this to generate:
    #   original_ids = ["ID_A", "ID_B", "ID_C"]
    #   targets.ids = [2, 0, 1]
    #   original_index_to_current_index = {2:0, 0:1, 1:2}
    #   current_index_to_original_index = {0:2, 1:0, 2:1}

    try:
        fps = chemfp.open(target_filename)
    except (IOError, ValueError) as err:
        sys.stderr.write("Cannot open targets file: %s\n" % (err,))
        raise SystemExit(1)
    
    t1 = time.time()
    open_time = t1-start_time

    # If the file is empty then the num_bytes is None.  This will
    # cause downstream code to fail. The easiest solution (perhaps a
    # hack) is to force it to have 1 byte.
    if fps.metadata.num_bytes is None:
        fps.metadata = fps.metadata.copy(num_bytes=1)
        
    if getattr(fps, "popcount_indices", ""):
        # Already ordered; don't need to reorder
        targets = fps.copy()
        original_ids = OriginalIds(fps.ids)
        original_index_to_current_index = current_index_to_original_index = unchanged_dict
    else:
        # preserve alignment, if present
        alignment = getattr(fps, "alignment", None)
        # Either the input is an unordered FPB or an FPS
        original_ids = []
        def get_index_to_id(fps):
            for i, (id, fp) in enumerate(fps):
                original_ids.append(id)
                yield i, fp

        targets = chemfp.load_fingerprints(get_index_to_id(fps), fps.metadata, alignment=alignment)
        original_index_to_current_index = dict((id, i) for (i, id) in enumerate(targets.ids))
        current_index_to_original_id = dict((i, original_ids[original_index])
                                                for i, original_index in enumerate(targets.ids))
    
    t2 = time.time()
    read_time = t2-t1
    try:
        outfile, close = io.open_binary_output(args.output)
    except (IOError, ValueError) as err:
        sys.stderr.write("Cannot open output file: %s\n" % (err,))
        raise SystemExit(1)

    if args.count:
        type = make_output_type("Count threshold=%(threshold)s NxN=full",
                                threshold=threshold)
        write_count_magic(outfile)
    else:
        type = make_output_type("%(name)s k=%(k)s threshold=%(threshold)s NxN=full",
                                k=k, threshold=threshold)
        write_simsearch_magic(outfile)

    write_simsearch_header(outfile, {
        "num_bits": targets.metadata.num_bits,
        "software": SOFTWARE,
        "type": type,
        "targets": target_filename,
        "target_sources": targets.metadata.sources})

    t3 = time.time()
    output_time = t3-t2

    if args.count:
        start_search_time = time.time()
        counts = search.count_tanimoto_hits_symmetric(targets, threshold,
                                                      batch_size=args.batch_size)
        end_search_time = time.time()
            
        for original_index, original_id in enumerate(original_ids):
            current_index = original_index_to_current_index[original_index]
            count = counts[current_index]
            outfile.write(b"%d\t%s\n" % (count, original_id.encode("utf8")))
        end_write_time = time.time()
    else:
        if 0:
            hit_formatter = "\t%s\t" + get_float_formatter(targets.metadata.num_bytes)
        else:
            precision = int(math.log10(targets.metadata.num_bytes*8)) + 2
        start_search_time = time.time()
        if k == "all":
            results = search.threshold_tanimoto_search_symmetric(targets, threshold,
                                                                 batch_size=args.batch_size)
        else:
           results = search.knearest_tanimoto_search_symmetric(targets, k, threshold,
                                                               batch_size=args.batch_size)
        end_search_time = time.time()

        for original_index, original_id in enumerate(original_ids):
            current_index = original_index_to_current_index[original_index]
            if 0:
                new_indices_and_scores = results[current_index].get_ids_and_scores()
                outfile.write(b"%d\t%s" % (len(new_indices_and_scores), original_id.encode("utf8")))
                for (new_index, score) in new_indices_and_scores:
                    original_id = original_ids[new_index]
                    outfile.write((hit_formatter % (original_id, score)).encode("utf8"))
            else:
                result = results[current_index]
                outfile.write(b"%d\t%s" % (len(result), original_id.encode("utf8")))
                if len(result) > 0:
                    target_ids = [original_ids[new_index] for new_index in result.get_ids()]
                    #print("len", len(result), target_ids, result.get_ids_and_scores(),file=open("/dev/stderr", "w"))
                    s = result.format_ids_and_scores_as_bytes(target_ids, precision)
                    outfile.write(b"\t")
                    outfile.write(s)
                
            outfile.write(b"\n") # XXX flush?
        end_write_time = time.time()

    output_time += end_write_time - end_search_time
    search_time = end_search_time - start_search_time
    
    if close is not None:
        close()
    total_time = time.time() - start_time
    if args.times:
        sys.stderr.write("open %.2f read %.2f search %.2f output %.2f total %.2f\n" % (
            open_time, read_time, search_time, output_time, total_time))

####

def int_or_all(s):
    if s == "all":
        return s
    return int(s)

# the "2fps" options need a way to say "get the options from --reference"
# ob2fps --reference targets.fps | simsearch -k  5 --threshold 0.5 targets.fps

parser = argparse.ArgumentParser(
    description="Search an FPS or FPB file for similar fingerprints")
parser.add_argument("-k" ,"--k-nearest", metavar="INT",
                    help="select the k nearest neighbors (use 'all' for all neighbors)",
                    default=None, type=int_or_all)
parser.add_argument("-t" ,"--threshold", metavar="FLOAT",
                    help="minimum similarity score threshold",
                    default=None, type=float)
parser.add_argument("--queries", "-q", metavar="FILENAME",
                    help="filename containing the query fingerprints")
parser.add_argument("--NxN", action="store_true",
                    help="use the targets as the queries, and exclude the self-similarity term")
parser.add_argument("--query", metavar="STRING",
                    help="query as a structure record (default format: 'smi')")
parser.add_argument("--hex-query", metavar="HEX",
                    help="query in hex")
parser.add_argument("--query-id", default=None, metavar="ID",
                    help="id for the query or hex-query (default: 'Query1'")
parser.add_argument("--query-structures", "-S", metavar="FILENAME",
                    help="read strutures ")
parser.add_argument("--query-format", "--in", metavar="FORMAT", dest="query_format",
                    help="input query format (default uses the file extension, else "
                        "'fps' for --queries and 'smi' for query structures)")
parser.add_argument("--target-format", metavar="FORMAT", dest="target_format",
                    help="input target format (default uses the file extension, else 'fps')")
parser.add_argument(
    "--id-tag", metavar="NAME",
    help="tag containing the record id if --query-structures is an SD file)")
parser.add_argument(
    "--errors", choices=["strict", "report", "ignore"], default="ignore",
    help="how should structure parse errors be handled? (default=ignore)")

parser.add_argument("-o", "--output", metavar="FILENAME",
                    help="output filename (default is stdout)")

parser.add_argument("-c", "--count", help="report counts", action="store_true")

parser.add_argument("-b", "--batch-size", metavar="INT",
                    help="batch size",
                    default=100, type=int)

parser.add_argument("--scan", help="scan the file to find matches (low memory overhead)",
                    action="store_true")
parser.add_argument("--memory", help="build and search an in-memory data structure (faster for multiple queries)",
                    action="store_true")

parser.add_argument("--times", help="report load and execution times to stderr",
                    action="store_true")

cmdsupport.add_version(parser)

parser.add_argument("target_filename", nargs=1, help="target filename", default=None)

## Something to enable multi-threading
#parser.add_argument("-j", "--jobs", help="number of jobs ",
#                    default=10, type=int)


def _get_query_id(id1, id2=None):
    if id1 is not None:
        return id1
    if id2 is not None:
        return id2
    return "Query1"

def run():
    cmdsupport.run(main)

def main(args=None):
    args = parser.parse_args(args)
    target_filename = args.target_filename[0]

    threshold = args.threshold
    k = args.k_nearest

    if args.count and k is not None and k != "all":
        parser.error("--count search does not support --k-nearest")

    # People should not use this without setting parameters.  On the
    # other hand, I don't want an error message if there are no
    # parameters. This solution seems to make sense.

    if threshold is None:
        if k is None:
            # If nothing is set, use defaults of --threshold 0.7 -k 3
            threshold = 0.7
            k = 3
        else:
            # only k is set; search over all possible matches
            threshold = 0.0
    else:
        if k is None:
            # only threshold is set; search for all hits above that threshold
            k = "all"

    if k == "all":
        pass
    elif k < 0:
        parser.error("--k-nearest must be non-negative or 'all'")

    if not (0.0 <= threshold <= 1.0):
        parser.error("--threshold must be between 0.0 and 1.0, inclusive")

    if args.batch_size < 1:
        parser.error("--batch-size must be positive")

    bitops.use_environment_variables()

    if args.NxN:
        if args.scan:
            parser.error("Cannot specify --scan with an --NxN search")
        if args.query:
            parser.error("Cannot specify --query with an --NxN search")
        if args.hex_query:
            parser.error("Cannot specify --hex-query with an --NxN search")
        if args.queries:
            parser.error("Cannot specify --queries with an --NxN search")
        if args.query_structures:
            parser.error("Cannot specify --query-structures with an --NxN search")
        do_NxN_searches(args, k, threshold, target_filename)
        return
            
    if args.scan and args.memory:
        parser.error("Cannot specify both --scan and --memory")

    if bool(args.query) + bool(args.hex_query) + bool(args.queries) + bool(args.query_structures) > 1:
        parser.error("Can only specify at most one of --query, --hex-query, --queries, or --query-structures")

    # Verify that the query_id, if present, is in the valid format
    query_id = args.query_id
    if query_id is not None:
        for c, name in ( ("\t", "tab"),
                         ("\n", "newline"),
                         ("\r", "control-return"),
                         ("\0", "NUL")):
            if c in query_id:
                parser.error("--query-id must not contain the %s character" %
                             (name,))
                
    # Open the target file. This reads just enough to get the header.
    if target_filename is not None and target_filename.lower().endswith(".flush"):
        cmdsupport.die("Simsearch cannot use flush files as input. Use chemfp_converters to convert it to FPS or FPB format.")

    try:
        targets = chemfp.open(target_filename, format=args.target_format)
    except chemfp.ChemFPError as err:
        sys.stderr.write("Cannot parse targets file: %s\n" % (err,))
        raise SystemExit(1)
    except (IOError, ValueError) as err:
        sys.stderr.write("Cannot open targets file: %s\n" % (err,))
        raise SystemExit(1)

    if args.hex_query is not None:
        query_id = _get_query_id(query_id)
        try:
            query_fp = bitops.hex_decode(args.hex_query)
        except (TypeError, Exception) as err:
            parser.error("--hex-query is not a hex string: %s" % (err,))

        for problem in chemfp.check_fingerprint_problems(query_fp, targets.metadata,
                                                         query_name="query fingerprint",
                                                         target_name=repr(target_filename)):
            if problem.severity == "error":
                parser.error(problem.description)

        num_bits = targets.metadata.num_bits
        if num_bits is None:
            num_bits = len(query_fp) * 8
        query_metadata = chemfp.Metadata(num_bits=num_bits, num_bytes=len(query_fp))
        queries = chemfp.Fingerprints(query_metadata,
                                      [(query_id, query_fp)])
        query_filename = None

    elif args.query is not None:
        # This is rather a hack as chemfp 1.x does not support the toolkit interface.
        # Instead, save to a file and parse.
        import tempfile
        from .. import types
        type_str = targets.metadata.type
        if not type_str:
            errmsg = "Unable to use the fingerprint type from %r: " % (target_filename,)
            errmsg += "ERROR: Must specify a fingerprint type string\n"
            sys.stderr.write(errmsg)
            raise SystemExit(1)
        opener = types.get_fingerprint_family(type_str)()

        format = args.query_format
        if format is None:
            format = "smi"

        record = args.query
        if format in ("smi", "can", "ism", "usm",
                      "smistring", "canstring", "ismstring", "usmstring"):
            terms = record.split(None, 1)
            if not terms:
                parser.error("Missing --query SMILES string")
            if len(terms) == 1:
                if query_id:
                    record = terms[0] + " " + query_id + "\n"
                else:
                    record = terms[0] + " " + "Query1\n"
            format = "smi"
            
        # Save to a tmp file
        named_temp_file = tempfile.NamedTemporaryFile(
            prefix="chemfp", suffix="." + format)
        named_temp_file.write(record)
        named_temp_file.flush()
        named_temp_file.seek(0)

        # Need to dig into the undocumented API
        error_handler = io.get_parse_error_handler(args.errors)
        if args.errors == "strict":
            id_error_handler = error_handler
        else:
            id_error_handler = io.get_parse_error_handler("report")
        location = io.Location.from_source(None)
        try:
            reader = opener.read_molecule_fingerprints(
                named_temp_file.name, format, args.id_tag, {}, args.errors)
        except ValueError as err:
            sys.stderr.write("Cannot use the --query: %s" % (err,))
            raise SystemExit(1)
        except (IOError, ValueError) as err:
            sys.stderr.write("Cannot use the --query: toolkit cannot parse the record\n")
            raise SystemExit(1)

        metadata = reader.metadata
        # Remove the sources because it's a fake name
        metadata.sources = []

        # Get the first fingerprint ... if there is one.
        try:
            id, query_fp = next(reader)
        except StopIteration:
            sys.stderr.write("Cannot use the --query: toolkit cannot parse the record\n")
            raise SystemExit(1)
        except chemfp.ParseError as err:
            sys.stderr.write("Cannot use the --query: %s\n" % (err,))
            raise SystemExit(1)
        query_id = _get_query_id(query_id, id)
        
        queries = chemfp.Fingerprints(metadata,
                                      [(query_id, query_fp)])
        query_filename = None
            
    elif args.query_structures:
        from .. import types
        type_str = targets.metadata.type
        if not type_str:
            errmsg = "Unable to use the fingerprint type from %r: " % (target_filename,)
            errmsg += "ERROR: Must specify a fingerprint type string\n"
            sys.stderr.write(errmsg)
            raise SystemExit(1)
        try:
            reader = chemfp.read_molecule_fingerprints(
                type_str, args.query_structures, args.query_format,
                args.id_tag, {}, args.errors)
        except ValueError as err:
            sys.stderr.write("Cannot read --query-structures file %r: %s\n" % (
                args.query_structures, err))
            raise SystemExit(1)
        queries = reader
        metadata = queries.metadata
        query_filename = args.query_structures
        
    else:
        query_filename = args.queries
        try:
            queries = chemfp.open(query_filename, format=args.query_format)
        except chemfp.ChemFPError as err:
            sys.stderr.write("Cannot parse queries file: %s\n" % (err,))
            raise SystemExit(1)
        except (IOError, ValueError) as err:
            sys.stderr.write("Cannot open queries file: %s\n" % (err,))
            raise SystemExit(1)

    batch_size = args.batch_size
    # If the targets file is empty then the number of bytes is None.
    # The metadata check between the queries and targets will fail.
    # The solution is easy - replace the targets metadata.
    if targets.metadata.num_bytes is None:
        targets.metadata = targets.metadata.copy(num_bytes=queries.metadata.num_bytes)
    
    query_arena_iter = queries.iter_arenas(batch_size)
    
    start_time = t1 = time.time()

    first_query_arena = None
    try:
        for first_query_arena in query_arena_iter:
            break
    except chemfp.ChemFPError as err:
        sys.stderr.write("Cannot parse queries file: %s\n" % (err,))
        raise SystemExit(1)

    if args.scan:
        # Leave the targets as-is
        pass
    elif args.memory:
        targets = chemfp.load_fingerprints(targets)
    if not first_query_arena:
        # No input. Leave as-is
        pass
    elif len(first_query_arena) < min(20, batch_size):
        # Figure out the optimal search. If there is a
        # small number of inputs (< ~20) then a scan
        # of the FPS file is faster than an arena search.
        pass
    else:
        targets = chemfp.load_fingerprints(targets)

    problems = chemfp.check_metadata_problems(queries.metadata, targets.metadata,
                                              query_name="queries", target_name="targets")
    for problem in problems:
        if problem.severity == "error":
            parser.error(problem.description)
        elif problem.severity == "warning":
            sys.stderr.write("WARNING: " + problem.description + "\n")

    t2 = time.time()
    open_time = t2 - t1
    t1 = t2
    try:
        outfile, close = io.open_binary_output(args.output)
    except (IOError, ValueError) as err:
        sys.stderr.write("Cannot open output file: %s\n" % (err,))
        raise SystemExit(1)

    if args.count:
        type = make_output_type("Count threshold=%(threshold)s",
                                threshold=threshold)
        write_count_magic(outfile)
    else:
        type = make_output_type("%(name)s k=%(k)s threshold=%(threshold)s",
                                k=k, threshold=threshold)
        write_simsearch_magic(outfile)

    write_simsearch_header(outfile, {
        "num_bits": targets.metadata.num_bits,
        "software": SOFTWARE,
        "type": type,
        "queries": query_filename,
        "targets": target_filename,
        "query_sources": queries.metadata.sources,
        "target_sources": targets.metadata.sources})

    t2 = time.time()
    output_time = t2-t1

    elapsed_time = ElapsedTime()
    if first_query_arena:
        query_arenas = itertools.chain([first_query_arena],
                                       query_arena_iter)

        try:
            if args.count:
                report_counts(outfile, query_arenas, targets,
                              threshold = threshold, elapsed_time=elapsed_time)
            elif k == "all":
                report_threshold(outfile, query_arenas, targets,
                                 threshold = threshold, elapsed_time=elapsed_time)
            else:
                report_knearest(outfile, query_arenas, targets,
                                k = k, threshold = threshold, elapsed_time=elapsed_time)
        except chemfp.ChemFPError as err:
            sys.stderr.write("Cannot parse targets file: %s\n" % (err,))
            raise SystemExit(1)
            
                
    if close is not None:
        close()
    output_time += elapsed_time.output_time
    total_time = time.time() - start_time

    if args.times:
        sys.stderr.write("open %.2f read %.2f search %.2f output %.2f total %.2f\n" % (
            open_time, elapsed_time.read_time, elapsed_time.search_time, output_time, total_time))

if __name__ == "__main__":
    main()
