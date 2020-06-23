from io import StringIO
from unittest.mock import patch

import pytest

from qc_utils import parsers, qcmetric

STAR_LOG = """                                 Started job on | Feb 16 23:45:04
                         Started mapping on |   Feb 16 23:49:02
                                Finished on |   Feb 17 00:16:34
   Mapping speed, Million of reads per hour |   115.09

                      Number of input reads |   52815760
                  Average input read length |   202
                                UNIQUE READS:
               Uniquely mapped reads number |   49542908
                    Uniquely mapped reads % |   93.80%
                      Average mapped length |   201.00
                   Number of splices: Total |   20633562
        Number of splices: Annotated (sjdb) |   20453258
                   Number of splices: GT/AG |   20442117
                   Number of splices: GC/AG |   154577
                   Number of splices: AT/AC |   11212
           Number of splices: Non-canonical |   25656
                  Mismatch rate per base, % |   0.30%
                     Deletion rate per base |   0.02%
                    Deletion average length |   1.51
                    Insertion rate per base |   0.01%
                   Insertion average length |   1.37
                         MULTI-MAPPING READS:
    Number of reads mapped to multiple loci |   2218531
         % of reads mapped to multiple loci |   4.20%
    Number of reads mapped to too many loci |   7303
         % of reads mapped to too many loci |   0.01%
                              UNMAPPED READS:
   % of reads unmapped: too many mismatches |   0.00%
             % of reads unmapped: too short |   1.95%
                 % of reads unmapped: other |   0.03%
                              CHIMERIC READS:
                   Number of chimeric reads |   0
                        % of chimeric reads |   0.00%"""

SAMTOOLS_FLAGSTAT = """424886248 + 0 in total (QC-passed reads + QC-failed reads)
0 + 0 duplicates
413471158 + 0 mapped (97.31%:-nan%)
424886248 + 0 paired in sequencing
212443124 + 0 read1
212443124 + 0 read2
413471158 + 0 properly paired (97.31%:-nan%)
413471158 + 0 with itself and mate mapped
0 + 0 singletons (0.00%:-nan%)
0 + 0 with mate mapped to a different chr
0 + 0 with mate mapped to a different chr (mapQ>=5)"""

ILLUMINA_TRIMSTATS = (
    "Total read-pairs processed: 179710367; Total read-pairs trimmed: 8621991"
)

BAMCOUNTS = """paired-nuclear-align 208933956
qc-flagged 0
u 263952413
u-pf 263952413
u-pf-n 259418766
u-pf-n-mm2 259189714
u-pf-n-mm2-mito  240666871
chr1 22465899
chr10 11223351
chr11 12368547
chr11_KI270721v1_random 422
chr12 11792546
chr13 6786761
chr14 8023861
chr14_GL000009v2_random 2699
"""

PRESEQ_TARGETS = """preseq-est-for-20000000 21000000
preseq-est-for-30000000  31000000
preseq-est-for-40000000  42000000
preseq-est-for-100000000 107000000
preseq-est-for-150000000 165000000
preseq-est-for-250000000 285000000
preseq-est-max 752199191
"""
HOTSPOT1_SPOT_SCORE = """  total tags  hotspot tags    SPOT
     5000000       2209334  0.4418\n"""

PICARD_DUPLICATION_METRICS = """## htsjdk.samtools.metrics.StringHeader
# picard.sam.markduplicates.MarkDuplicatesWithMateCigar MINIMUM_DISTANCE=300 INPUT=[/cromwell_root/dnase/dnase/a707c686-ca59-4eed-91f1-a287f72154a0/call-dnase_replicate/shard-0/dnase_replicate/6f9d8f96-9920-4930-940b-9876fcded62a/call-merge_mark_and_filter_bams/merge_mark_and_filter_bams/25a1ee0c-184e-4526-bf62-c55c16633184/call-mark/mark/85f77336-810b-40fb-abd3-f0c72201fc4e/call-add_mate_cigar_to_bam/add_mate_cigar_to_bam/7f0df874-11a9-47b1-93fd-c4a98f967638/call-revert_original_base_qualities_and_add_mate_cigar/mate_cigar.bam] OUTPUT=marked.bam METRICS_FILE=MarkDuplicates.picard ASSUME_SORTED=true READ_NAME_REGEX=[a-zA-Z0-9]+:[0-9]+:[a-zA-Z0-9]+:[0-9]+:([0-9]+):([0-9]+):([0-9]+).* VALIDATION_STRINGENCY=SILENT    SKIP_PAIRS_WITH_NO_MATE_CIGAR=true BLOCK_SIZE=100000 REMOVE_DUPLICATES=false DUPLICATE_SCORING_STRATEGY=TOTAL_MAPPED_REFERENCE_LENGTH PROGRAM_RECORD_ID=MarkDuplicates PROGRAM_GROUP_NAME=MarkDuplicatesWithMateCigar OPTICAL_DUPLICATE_PIXEL_DISTANCE=100 VERBOSITY=INFO QUIET=false COMPRESSION_LEVEL=5 MAX_RECORDS_IN_RAM=500000 CREATE_INDEX=false CREATE_MD5_FILE=false GA4GH_CLIENT_SECRETS=client_secrets.json
## htsjdk.samtools.metrics.StringHeader
# Started on: Mon May 04 00:58:33 UTC 2020

## METRICS CLASS picard.sam.DuplicationMetrics
LIBRARY	UNPAIRED_READS_EXAMINED	READ_PAIRS_EXAMINED	SECONDARY_OR_SUPPLEMENTARY_RDS	UNMAPPED_READS	UNPAIRED_READ_DUPLICATES	READ_PAIR_DUPLICATES	READ_PAIR_OPTICAL_DUPLICATES	PERCENT_DUPLICATION	ESTIMATED_LIBRARY_SIZE
Unknown Library	54238976	137746811	0	16929897	22741788	17466587	0	0.174914	496198880

## HISTOGRAM	java.lang.Double
"""

PICARD_INSERT_SIZE_METRICS = """## htsjdk.samtools.metrics.StringHeader
# picard.analysis.CollectInsertSizeMetrics HISTOGRAM_FILE=nuclear.CollectInsertSizeMetrics.picard.pdf INPUT=/cromwell_root/dnase/dnase/1b6c015b-4fa9-444d-864d-285c188c0b8f/call-dnase_replicate/shard-0/dnase_replicate/ab6fb07f-7419-4688-8e84-87e869a51ea5/call-merge_mark_and_filter_bams/merge_mark_and_filter_bams/1b2ff752-be3c-4544-8a33-950adf5a59ef/call-filter/filter/f39085ca-823f-4d64-bfbb-34d672980f20/call-filter_bam_reads_with_nonnuclear_flag/filter_bam_reads_with_nonnuclear_flag/e99d92cb-cb88-468b-a360-659c39a6a01b/call-view/nuclear.bam OUTPUT=nuclear.CollectInsertSizeMetrics.picard ASSUME_SORTED=true VALIDATION_STRINGENCY=LENIENT    DEVIATIONS=10.0 MINIMUM_PCT=0.05 METRIC_ACCUMULATION_LEVEL=[ALL_READS] INCLUDE_DUPLICATES=false STOP_AFTER=0 VERBOSITY=INFO QUIET=false COMPRESSION_LEVEL=5 MAX_RECORDS_IN_RAM=500000 CREATE_INDEX=false CREATE_MD5_FILE=false GA4GH_CLIENT_SECRETS=client_secrets.json
## htsjdk.samtools.metrics.StringHeader
# Started on: Thu Apr 23 17:17:19 UTC 2020

## METRICS CLASS	picard.analysis.InsertSizeMetrics
MEDIAN_INSERT_SIZE	MEDIAN_ABSOLUTE_DEVIATION	MIN_INSERT_SIZE	MAX_INSERT_SIZE	MEAN_INSERT_SIZE	STANDARD_DEVIATION	READ_PAIRS	PAIR_ORIENTATION	WIDTH_OF_10_PERCENT	WIDTH_OF_20_PERCENT	WIDTH_OF_30_PERCENT	WIDTH_OF_40_PERCENT	WIDTH_OF_50_PERCENT	WIDTH_OF_60_PERCENT	WIDTH_OF_70_PERCENT	WIDTH_OF_80_PERCENT	WIDTH_OF_90_PERCENT	WIDTH_OF_99_PERCENT	SAMPLE	LIBRARY	READ_GROUP
82	6	5	750	84.615764	11.674485	13631725	FR	3	7	9	11	13	17	19	31	93	517

## HISTOGRAM	java.lang.Integer
"""

SAMTOOLS_STATS = """CHK	b4f24be5	5ef36d97	450ccdce
# Summary Numbers. Use `grep ^SN | cut -f 2-` to extract this part.
SN	raw total sequences:	137377422
SN	filtered sequences:	0
SN	sequences:	137377422
SN	is sorted:	0
SN	1st fragments:	137377422
SN	last fragments:	0
SN	reads mapped:	133755927
SN	reads mapped and paired:	0	# paired-end technology bit set + both mates mapped
SN	reads unmapped:	3621495
SN	reads properly paired:	0	# proper-pair bit set
SN	reads paired:	0	# paired-end technology bit set
SN	reads duplicated:	0	# PCR or optical duplicate bit set
SN	reads MQ0:	27952198	# mapped and MQ=0
SN	reads QC failed:	0
SN	non-primary alignments:	0
SN	total length:	4945587192	# ignores clipping
SN	total first fragment length:	4945587192	# ignores clipping
SN	total last fragment length:	0	# ignores clipping
SN	bases mapped:	4815213372	# ignores clipping
SN	bases mapped (cigar):	4815213372	# more accurate
SN	bases trimmed:	0
SN	bases duplicated:	0
SN	mismatches:	15823799	# from NM fields
SN	error rate:	3.286209e-03	# mismatches / bases mapped (cigar)
SN	average length:	36
SN	average first fragment length:	36
SN	average last fragment length:	0
SN	maximum length:	36
SN	maximum first fragment length:	36
SN	maximum last fragment length:	0
SN	average quality:	65.8
SN	insert size average:	0.0
SN	insert size standard deviation:	0.0
SN	inward oriented pairs:	0
SN	outward oriented pairs:	0
SN	pairs with other orientation:	0
SN	pairs on different chromosomes:	0
SN	percentage of properly paired reads (%):	0.0
# First Fragment Qualities. Use `grep ^FFQ | cut -f 2-` to extract this part.
"""

INSERT_SIZE_INFO = """insert-ls-ratio	2983.1667
insert-ft-eleven	0.0912
"""

CUTADAPT_TRIMSTATS = """This is cutadapt 2.10 with Python 3.6.9
Command line parameters: -a AGATCGGAAGAGCGTCGTGTAGGGAAAGAGTGTTAATCTTAGTGTAGATCTCGGTGGTCGCCGTATCATT -A AGATCGGAAGAGCACACGTCTGAACTCCAGTCACGAATTCGTATCTCGTATGCCGTCTTCTGCTTG --cores=1 --pair-filter both --output trim.R1.fastq.gz --paired-output trim.R2.fastq.gz /cromwell-executions/test_trim_adapters_on_fastq_pair/17e8270e-032d-4e3c-a8fb-0fe19403b4ea/call-trim_adapters_on_fastq_pair/trim_adapters_on_fastq_pair/a8d935d2-9fd0-401a-afcf-d3d6b0471438/call-cutadapt/inputs/797577134/r1.fastq.gz /cromwell-executions/test_trim_adapters_on_fastq_pair/17e8270e-032d-4e3c-a8fb-0fe19403b4ea/call-trim_adapters_on_fastq_pair/trim_adapters_on_fastq_pair/a8d935d2-9fd0-401a-afcf-d3d6b0471438/call-cutadapt/inputs/797577134/r2.fastq.gz
Processing reads on 1 core in paired-end mode ...
Finished in 6.40 s (48 us/read; 1.25 M reads/minute).

=== Summary ===

Total read pairs processed:            133,435
  Read 1 with adapter:                  10,359 (7.8%)
  Read 2 with adapter:                  10,403 (7.8%)
Pairs written (passing filters):       133,435 (100.0%)

Total basepairs processed:     9,607,320 bp
  Read 1:     4,803,660 bp
  Read 2:     4,803,660 bp
Total written (filtered):      9,483,944 bp (98.7%)
  Read 1:     4,741,946 bp
  Read 2:     4,741,998 bp

=== First read: Adapter 1 ===

Sequence: AGATCGGAAGAGCGTCGTGTAGGGAAAGAGTGTTAATCTTAGTGTAGATCTCGGTGGTCGCCGTATCATT; Type: regular 3'; Length: 70; Trimmed: 10359 times

No. of allowed errors:
0-9 bp: 0; 10-19 bp: 1; 20-29 bp: 2; 30-39 bp: 3; 40-49 bp: 4; 50-59 bp: 5; 60-69 bp: 6; 70 bp: 7

Bases preceding removed adapters:
  A: 23.0%
  C: 31.4%
  G: 33.0%
  T: 12.5%
  none/other: 0.0%
"""


@patch("builtins.open", return_value=StringIO(STAR_LOG))
def test_parse_starlog(mock_open):
    star_log_dict = parsers.parse_starlog("path")
    assert len(star_log_dict) == 29


def test_percentage_to_float():
    percentage_line = "94.67%"
    formatted = parsers.percentage_to_float(percentage_line)
    assert isinstance(formatted, float)
    assert formatted == 94.67


@patch("builtins.open", return_value=StringIO(SAMTOOLS_FLAGSTAT))
def test_parse_flagstats(mock_open):
    flagstat_dict = parsers.parse_flagstats("path")
    assert len(flagstat_dict) == 23


@patch("builtins.open", return_value=StringIO(ILLUMINA_TRIMSTATS))
def test_parse_illumina_trimstats(mock_open):
    trimstat_dict = parsers.parse_illumina_trimstats("path")
    assert len(trimstat_dict) == 2
    assert trimstat_dict["Total read-pairs processed"] == 179710367
    assert trimstat_dict["Total read-pairs trimmed"] == 8621991


@patch("builtins.open", return_value=StringIO(BAMCOUNTS))
def test_parse_bamcounts(mock_open):
    bamstat_dict = parsers.parse_bamcounts("path")
    assert len(bamstat_dict) == 15
    assert "u-pf-n-mm2-mito" in bamstat_dict
    assert bamstat_dict["chr14_GL000009v2_random"] == 2699


@patch("builtins.open", return_value=StringIO("chr1 123 456"))
def test_parse_bamcounts_bad_input_raises_AssertionError(mock_open):
    with pytest.raises(AssertionError):
        parsers.parse_bamcounts("path")


@patch("builtins.open", return_value=StringIO(PRESEQ_TARGETS))
def test_parse_preseq_targets(mock_open):
    preseq_targets_dict = parsers.parse_preseq_targets("path")
    assert len(preseq_targets_dict) == 7
    assert "preseq-est-for-100000000" in preseq_targets_dict
    assert preseq_targets_dict["preseq-est-max"] == 752199191


@patch("builtins.open", return_value=StringIO(HOTSPOT1_SPOT_SCORE))
def test_parse_hotspot1_spot_score(mock_open):
    spot_score_dict = parsers.parse_hotspot1_spot_score("path")
    assert len(spot_score_dict) == 3
    assert spot_score_dict["hotspot tags"] == 2209334
    assert spot_score_dict["SPOT"] == 0.4418


@patch("builtins.open", return_value=StringIO(PICARD_DUPLICATION_METRICS))
def test_parse_picard_duplication_metrics(mock_open):
    duplication_metrics_dict = parsers.parse_picard_duplication_metrics("path")
    assert len(duplication_metrics_dict) == 10
    assert "UNMAPPED_READS" in duplication_metrics_dict
    assert duplication_metrics_dict["PERCENT_DUPLICATION"] == 0.174914


def test_try_converting_to_numeric_raises():
    with pytest.raises(AssertionError):
        parsers.try_converting_to_numeric(3.14)


def test_try_converting_to_numeric_int():
    assert parsers.try_converting_to_numeric("1") == 1


def test_try_converting_to_numeric_float():
    assert parsers.try_converting_to_numeric("3.14") == 3.14


def test_try_converting_to_numeric_str():
    assert parsers.try_converting_to_numeric("SPAM") == "SPAM"


@patch("builtins.open", return_value=StringIO(INSERT_SIZE_INFO))
def test_parse_insert_size_info(mock_open):
    insert_size_info_dict = parsers.parse_insert_size_info("path")
    assert len(insert_size_info_dict) == 2
    assert "insert-ft-eleven" in insert_size_info_dict
    assert insert_size_info_dict["insert-ls-ratio"] == 2983.1667


@patch("builtins.open", return_value=StringIO(PICARD_INSERT_SIZE_METRICS))
def test_parse_picard_insert_size_metrics(mock_open):
    insert_size_metrics_dict = parsers.parse_picard_insert_size_metrics("path")
    assert len(insert_size_metrics_dict) == 18
    assert "READ_PAIRS" in insert_size_metrics_dict
    assert insert_size_metrics_dict["MEAN_INSERT_SIZE"] == 84.615764
    assert insert_size_metrics_dict["MEDIAN_INSERT_SIZE"] == 82
    assert insert_size_metrics_dict["PAIR_ORIENTATION"] == "FR"


@patch("builtins.open", return_value=StringIO(SAMTOOLS_STATS))
def test_parse_samtools_stats(mock_open):
    stats_dict = parsers.parse_samtools_stats("path")
    assert len(stats_dict) == 38
    assert "percentage of properly paired reads (%)" in stats_dict
    assert stats_dict["error rate"] == 0.003286209
    assert stats_dict["1st fragments"] == 137377422


def test_convert_string_with_commas_to_int():
    assert parsers.convert_string_with_commas_to_int("123,456") == 123456
    assert parsers.convert_string_with_commas_to_int("123456") == 123456


@patch("builtins.open", return_value=StringIO(CUTADAPT_TRIMSTATS))
def test_parse_cutadapt_trimstats(mock_open):
    trimstats_dict = parsers.parse_cutadapt_trimstats("path")
    assert len(trimstats_dict) == 3
    assert "Total read pairs processed" in trimstats_dict
    assert trimstats_dict["Read 1 with adapter"] == 10359
