# -*- coding: utf-8 -*-
"Process sequence file, using logging for asynchronous output"
# standard library imports
# stdlib imports
import zlib
from collections import defaultdict
from operator import itemgetter

# first-party imports
import numpy as np
from Bio import SeqIO
from Bio.Data import IUPACData

# module imports
from .common import AMBIG_NAME
from .common import DUP_NAME
from .common import LENGTH_NAME
from .common import SEQ_FILE_TYPE
from .common import SHORT_NAME
from .common import SUBSTRING_NAME

ALPHABET = IUPACData.protein_letters + "X" + "-"
LOGINT_FMT = "%s\t%s\t%s\t%d"
LOGFLOAT_FMT = "%s\t%s\t%s\t%f"
LOGSTR_FMT = "%s\t%s\t%s\t%s"


#
# Classes
#
class ShortCounter(object):
    """count sequences too short
    """

    def __init__(self, length=0, log=False, name=None):
        """

        :param length: minimum length
        :param log: logger object
        :param name: file name
        """
        self.count = 0
        self.log = log
        self.minlen = length
        self.name = name

    def test(self, s, id):
        """test and count if too short

        :param s: sequence
        :param id: ID of sequence for log
        :return: True if s is too short
        """
        if len(s) < self.minlen:
            self.count += 1
            if self.log:
                self.log.debug(LOGINT_FMT, self.name, id, SHORT_NAME, len(s))
            return True
        else:
            return False


class AmbigCounter(object):
    """count sequences with too high a fraction ambiguous
    """

    def __init__(self, frac=0.0, log=False, name=None):
        """

        :param frac: maximum fraction ambiguous
        :param log: logger object
        :param name: file name for log
        """
        self.count = 0
        self.log = log
        self.frac = frac
        self.name = name

    def test(self, s, id):
        """test for fraction ambiguous and count

        :param s: sequence
        :param id: ID of sequence for log
        :return: True if s is above fraction ambiguous
        """
        ambig = sum([i == "X" for i in s])
        if ambig > self.frac:
            self.count += 1
            if self.log:
                self.log.debug(
                    LOGFLOAT_FMT,
                    self.name,
                    id,
                    AMBIG_NAME,
                    ambig * 100.0 / len(s),
                )
            return True
        else:
            return False


class DuplicateIDDict(defaultdict):
    """A dictionary of lists with a get() that returns the surviving ID
    """

    def __init__(self, concat=False):
        self.concat = concat
        super().__init__(list)

    def get(self, k):
        if self.concat:
            return "|".join([k] + self[k])
        else:
            return k


class DuplicateCounter(object):
    """count sequences too short
    """

    def __init__(self, log=False, name=None, concat_names=False):
        self.exact_count = 0
        self.substring_count = 0
        self.log = log
        self.name = name
        self.hash_dict = {}
        self.dupDict = DuplicateIDDict(concat=concat_names)

    def exact(self, s, id):
        "test and count if exact duplicate"
        seq_hash = zlib.adler32(bytearray(str(s), "utf-8"))
        if seq_hash not in self.hash_dict:
            self.hash_dict[seq_hash] = id
            return False
        else:
            self.exact_count += 1
            first_ID = self.hash_dict[seq_hash]
            self.dupDict[first_ID].append(id)
            if self.log:
                self.log.debug(LOGSTR_FMT, self.name, id, DUP_NAME, first_ID)
            return True

    def index_by_length(self, items):
        length_idx = [(i, len(item)) for i, item in enumerate(items)]
        length_idx.sort(key=itemgetter(1))
        return [idx for idx, length in length_idx]

    def substring(self, seqs, remove=True):
        "find and optionally remove exact substring matches in set of seqs"
        removal_list = []
        ascending = self.index_by_length([r.seq for r in seqs])
        for item_num, idx in enumerate(ascending):
            test_seq = seqs[idx].seq
            test_id = seqs[idx].id
            # traverse from biggest to smallest to find the biggest match
            for record in [
                seqs[i] for i in reversed(ascending[item_num + 1 :])
            ]:
                if str(test_seq) in str(record.seq):
                    self.substring_count += 1
                    self.dupDict[record.id].append(test_id)
                    removal_list.append(idx)
                    if self.log:
                        self.log.debug(
                            LOGSTR_FMT,
                            self.name,
                            test_id,
                            SUBSTRING_NAME,
                            record.id,
                        )
                    break
        # Optionally remove exact substring matches
        if remove and len(removal_list) > 0:
            removal_list.sort()
            for item_num, idx in enumerate(removal_list):
                seqs.pop(idx - item_num)
        return seqs


class Sanitizer(object):
    """clean up and count potential problems with sequence

       potential problems are:
          dashes:    (optional, removed if remove_dashes=True)
          alphabet:  if not in IUPAC set, changed to 'X'
    """

    def __init__(self, remove_dashes=False):
        self.remove_dashes = remove_dashes
        self.seqs_sanitized = 0
        self.chars_in = 0
        self.chars_removed = 0
        self.chars_fixed = 0
        self.endchars_removed = 0

    def char_remover(self, s, character):
        """remove positions with a given character

        :param s: mutable sequence
        :return: sequence with characters removed
        """
        removals = [i for i, j in enumerate(s) if j == character]
        self.chars_removed += len(removals)
        [s.pop(pos - k) for k, pos in enumerate(removals)]
        return s

    def fix_alphabet(self, s):
        """replace everything out of alphabet with 'X'

        :param s: mutable sequence, upper-cased
        :return: fixed sequence
        """
        fix_positions = [
            pos for pos, char in enumerate(s) if char not in ALPHABET
        ]
        self.chars_fixed = len(fix_positions)
        [s.__setitem__(pos, "X") for pos in fix_positions]
        return s

    def remove_char_on_ends(self, s, character):
        """remove leading/trailing ambiguous residues

        :param s: mutable sequence
        :return: sequence with characterss removed from ends
        """
        in_len = len(s)
        while s[-1] == character:
            s.pop()
        while s[0] == character:
            s.pop(0)
        self.endchars_removed += in_len - len(s)
        return s

    def sanitize(self, s):
        """sanitize alphabet use while checking lengths

        :param s: mutable sequence
        :return: sanitized sequence
        """
        self.seqs_sanitized += 1
        self.chars_in += len(s)
        if len(s) and self.remove_dashes:
            s = self.char_remover(s, "-")
        if len(s):
            s = self.fix_alphabet(s)
        if len(s):
            s = self.remove_char_on_ends(s, "X")
        return s


def process_file(
    file,
    logger=None,
    write=False,
    min_len=0,
    min_seqs=0,
    max_ambiguous=0,
    remove_dashes=False,
    remove_dups=False,
    remove_substrings=False,
    lengths=False,
):
    """fix alphabet and other problems in FASTA file

    :param file: path to sequence file
    :param logger: if True, logger object
    :param write:  if True, overwrite input files
    :param min_len: minimum length of sequences after trims
    :param min_seqs: minimum number of sequences after dedup
    :param max_ambiguous: maximum fraction of sequence that can be 'X'
    :param remove_dashes: if True, remove '-' characters
    :param remove_duplicates: if True, remove exact matches
    :param remove_substrings: if True, remove substring matches
    :param lengths: if True, write sequence lengths to log file
    :return:
    """
    if logger:
        logger.debug("processing %s", file)
    out_sequences = []
    sanitizer = Sanitizer(remove_dashes=remove_dashes)
    too_short = ShortCounter(length=min_len, log=logger, name=file.name)
    too_ambig = AmbigCounter(frac=max_ambiguous, log=logger, name=file.name)
    duplicated = DuplicateCounter(log=logger, name=file.name)
    with file.open("rU") as handle:
        for record in SeqIO.parse(handle, SEQ_FILE_TYPE):
            seq = record.seq.upper().tomutable()
            seq = sanitizer.sanitize(seq)
            if not len(seq):
                # zero-length string after sanitizing
                continue
            if too_short.test(seq, record.id):
                # delete sequences too short
                continue
            if too_ambig.test(seq, record.id):
                # delete sequences too ambig
                continue
            if duplicated.exact(seq, record.id) and remove_dups:
                # delete exact-duplicate sequences
                continue
            record.seq = seq.toseq()
            out_sequences.append(record)
    # Search for exact substring matches in the set
    if remove_dups and remove_substrings:
        out_sequences = duplicated.substring(out_sequences)
    # Indicate (in ID) records deduplicated
    if (remove_dups or remove_substrings) and len(duplicated.dupDict) > 0:
        for record in out_sequences:
            if record.id in duplicated.dupDict:
                record.id = duplicated.dupDict.get(record.id)
                record.description = ""
    # Check if file has enough sequences
    if len(out_sequences) < min_seqs:
        small = 1
        if write:  # Too small, remove if overwriting
            file.unlink()
    else:
        small = 0
        if lengths and logger:
            for record in out_sequences:
                logger.debug(
                    LOGINT_FMT,
                    file.name,
                    record.id,
                    LENGTH_NAME,
                    len(record.seq),
                )
        if write:
            with file.open("w") as output_handle:
                SeqIO.write(out_sequences, output_handle, SEQ_FILE_TYPE)
    lengths_arr = np.array([len(s) for s in out_sequences])
    length_std = lengths_arr.std()
    length_mean = lengths_arr.mean() + 0.5
    if np.isnan(length_std):
        length_std_percent = 0
    else:
        length_std_percent = int(round(length_std * 100 / length_mean))

    return (
        file.name,
        # character stats
        sanitizer.chars_in,
        lengths_arr.sum(),
        sanitizer.chars_removed,
        sanitizer.chars_fixed,
        sanitizer.endchars_removed,
        # sequence stats
        sanitizer.seqs_sanitized,
        len(out_sequences),
        too_ambig.count,
        too_short.count,
        duplicated.exact_count,
        duplicated.substring_count,
        # file stats
        length_std_percent,
        small,
    )
