import re

# Parser functions


def parse_starlog(path_to_log):
    """Parse star logfile into a dict.
    Args:
        path_to_log: filepath containing the star run log
    Returns:
        dict that contains metrics from star log
    """
    qc_dict = {}
    with open(path_to_log) as f:
        for line in f:
            if "|" in line:
                tokens = line.split("|")
                qc_dict[tokens[0].strip()] = tokens[1].strip()
    return qc_dict


# format pergentage points


def percentage_to_float(line):
    return float(line.strip("%"))


def convert_string_with_commas_to_int(number_string):
    """Convert string of format xyz,tuv representing an int into an int.
    Args:
        number_string: str representing an int
    Returns:
        int represented by the number_string
    """
    return int(re.sub(",", "", number_string))


def try_converting_to_numeric(value):
    """Try converting to numeric.
    Attempts to convert to int, and if that fails, to float
    and as a last resort keep as str.
    Args:
        value: str input value from qc
    Returns:
        value converted to numeric if applicable.
    """
    assert type(value) == str
    try:
        converted_value = int(value)
    except ValueError:
        try:
            converted_value = float(value)
        except ValueError:
            converted_value = value
    return converted_value


def parse_flagstats(filePath):
    """Parse samtools flagstat file into a dict
    Args:
        filePath: path to samtools flagstat file
    Returns:
        dict that contains metrics from flagstats
    """
    pairs = {}
    numbers_type = int
    with open(filePath, "r") as fh:
        while True:
            line = fh.readline()
            if line is None:
                break
            line.strip()
            if line == "":
                continue
            # 2826233 + 0 in total (QC-passed reads + QC-failed reads)
            if line.find("QC-passed reads") > 0:
                # 2826233 + 0 in total (QC-passed reads + QC-failed reads)
                parts = line.split()
                pairs["total"] = numbers_type(parts[0])
                pairs["total_qc_failed"] = numbers_type(parts[2])
            # 0 + 0 duplicates
            elif line.find("duplicates") > 0:
                parts = line.split()
                pairs["duplicates"] = numbers_type(parts[0])
                pairs["duplicates_qc_failed"] = numbers_type(parts[2])
            # 2826233 + 0 mapped (100.00%:-nan%)
            elif "mapped" not in pairs and line.find("mapped") > 0:
                parts = line.split()
                pairs["mapped"] = numbers_type(parts[0])
                pairs["mapped_qc_failed"] = numbers_type(parts[2])
                val = parts[4][1:].split(":")[0]
                pairs["mapped_pct"] = percentage_to_float(val)
            # 2142 + 0 paired in sequencing
            elif line.find("paired in sequencing") > 0:
                parts = line.split()
                if int(parts[0]) <= 0:  # Not paired-end, so nothing more needed
                    break
                pairs["paired"] = numbers_type(parts[0])
                pairs["paired_qc_failed"] = numbers_type(parts[2])
            # 107149 + 0 read1
            elif line.find("read1") > 0:
                parts = line.split()
                pairs["read1"] = numbers_type(parts[0])
                pairs["read1_qc_failed"] = numbers_type(parts[2])
            # 107149 + 0 read2
            elif line.find("read2") > 0:
                parts = line.split()
                pairs["read2"] = numbers_type(parts[0])
                pairs["read2_qc_failed"] = numbers_type(parts[2])
            # 2046 + 0 properly paired (95.48%:-nan%)
            elif line.find("properly paired") > 0:
                parts = line.split()
                pairs["paired_properly"] = numbers_type(parts[0])
                pairs["paired_properly_qc_failed"] = numbers_type(parts[2])
                val = parts[5][1:].split(":")[0]
                pairs["paired_properly_pct"] = percentage_to_float(val)
            # 0 + 0      singletons (0.00%:-nan%)
            elif line.find("singletons") > 0:
                parts = line.split()
                pairs["singletons"] = numbers_type(parts[0])
                pairs["singletons_qc_failed"] = numbers_type(parts[2])
                val = parts[4][1:].split(":")[0]
                pairs["singletons_pct"] = percentage_to_float(val)
            # 2046212 + 0 with itself and mate mapped
            elif line.find("with itself and mate mapped") > 0:
                parts = line.split()
                pairs["with_itself"] = numbers_type(parts[0])
                pairs["with_itself_qc_failed"] = numbers_type(parts[2])
            # 0 + 0 with mate mapped to a different chr (mapQ>=5)
            elif line.find("with mate mapped to a different chr") > 0:
                parts = line.split()
                pairs["diff_chroms"] = numbers_type(parts[0])
                pairs["diff_chroms_qc_failed"] = numbers_type(parts[2])
                break
    return pairs


def parse_key_value_tsv(path_to_tsv, sep=None):
    """Parse 2-column tsv file with string key, valuetype value into a dict.
    Args:
        path_to_tsv: path to file containing the tsv
        sep: column separator String, default: None (will split on any whitespace)
    Raises:
        AssertionError if a row that splits into number of tokens other than 2
    """
    qc_dict = {}
    with open(path_to_tsv) as f:
        for line in f:
            tokens = line.split(sep)
            assert len(tokens) == 2
            qc_dict[tokens[0]] = try_converting_to_numeric(tokens[1])
    return qc_dict


def parse_illumina_trimstats(path_to_trimstats):
    """Parse illumina trimstats into a dict.
    Args:
        path_to_trimstats: path to file that contains illumina trimstats
    Returns:
        dict with trimstats qc metrics
    Raises:
        AssertionError if a row that splits into number of tokens other than 2
        ValueError if some value is not suitable for converting into int
    """
    qc_dict = {}
    with open(path_to_trimstats) as f:
        rawstats = f.readline()
    tokens = rawstats.split(";")
    qc_dict["Total read-pairs processed"] = int(tokens[0].split()[-1])
    qc_dict["Total read-pairs trimmed"] = int(tokens[1].split()[-1])
    return qc_dict


def parse_bamcounts(path_to_bamcounts):
    """Parse bamcounts into a dict.
    Args:
        path_to_bamcounts: path to file that contains bamcounts/tagcounts
    Returns:
        dict with bamcounts qc metrics
    Raises:
        AssertionError if a row that splits into number of tokens other than 2
    """
    return parse_key_value_tsv(path_to_bamcounts)


def parse_preseq_targets(path_to_preseq_targets):
    """Parse preseq targets into a dict.
    Args:
        path_to_preseq_targets: path to file that contains preeq targets
    Returns:
        dict with preseq targets qc metrics
    Raises:
        AssertionError if a row that splits into number of tokens other than 2
    """
    return parse_key_value_tsv(path_to_preseq_targets)


def parse_hotspot1_spot_score(path_to_hotspot1_spot_score):
    """Parse hotspot1 spot score into a dict.
    Args:
        path_to_hotspot1_spot_score: path to file that contains hotspot1 spot score
    Returns:
        dict with hotspot1 spot score qc metrics
    """
    qc_dict = {}
    with open(path_to_hotspot1_spot_score) as f:
        next(f)
        raw_values = f.readline()
    values = raw_values.strip().split()
    qc_dict["total tags"] = try_converting_to_numeric(values[0])
    qc_dict["hotspot tags"] = try_converting_to_numeric(values[1])
    qc_dict["SPOT"] = try_converting_to_numeric(values[2])
    return qc_dict


def parse_picard_metrics(path_to_metrics):
    """Parse picard metrics into a dict.
    Args:
        path_to_metrics: path to a file that contains picard etrics
    Returns:
        dict with picard metrics
    """
    qc_dict = {}
    with open(path_to_metrics) as f:
        lines = []
        for _ in range(8):
            lines.append(f.readline())
    keys = lines[6].split("\t")
    values = lines[7].split("\t")
    keys = [key.strip() for key in keys]
    values = [value.strip() for value in values]
    for key, value in zip(keys, values):
        qc_dict[key] = try_converting_to_numeric(value)
    return qc_dict


def parse_picard_duplication_metrics(path_to_duplication_metrics):
    """Parse picard duplication metrics into a dict.
    Args:
        path_to_duplication_metrics: path to a file that contains picard duplication metrics
    Returns:
        dict with picard duplication metrics
    """
    return parse_picard_metrics(path_to_duplication_metrics)


def parse_picard_insert_size_metrics(path_to_insert_size_metrics):
    """Parse picard insert size metrics into a dict.
    Args:
        path_to_insert_size_metrics: path to a file that contains picard insert size metrics
    Returns:
        dict with picard insert size metrics
    """
    return parse_picard_metrics(path_to_insert_size_metrics)


def parse_insert_size_info(path_to_insert_size_info):
    return parse_key_value_tsv(path_to_insert_size_info)


def parse_samtools_stats(path_to_samtools_stats):
    """Parse samtools stats metrics into a dict.
    Args:
        path_to_samtools_stats: path to a file that contains samtools stats metrics
    Returns:
        dict with samtools stats metrics
    """
    with open(path_to_samtools_stats) as f:
        stats_lines = [
            line.split("\t") for line in f.readlines() if line.startswith("SN")
        ]
    qc_dict = {
        line[1].strip(":"): try_converting_to_numeric(line[2]) for line in stats_lines
    }
    return qc_dict


def parse_cutadapt_trimstats(path_to_cutadapt_trimstats):
    """Parse cutadapt trimstats metrics into a dict.
    Args:
        path_to_cutadapt_trimstats: path to a file that contains cutadapt trimstats metrics
    Returns:
        dict with cutadapts trimstats metrics
    """
    qc_dict = {}
    with open(path_to_cutadapt_trimstats) as f:
        trimstats_lines = f.readlines()
    qc_dict["Total read pairs processed"] = convert_string_with_commas_to_int(
        trimstats_lines[7].split()[-1]
    )
    qc_dict["Read 1 with adapter"] = convert_string_with_commas_to_int(
        trimstats_lines[8].split()[-2]
    )
    qc_dict["Read 2 with adapter"] = convert_string_with_commas_to_int(
        trimstats_lines[9].split()[-2]
    )
    return qc_dict
