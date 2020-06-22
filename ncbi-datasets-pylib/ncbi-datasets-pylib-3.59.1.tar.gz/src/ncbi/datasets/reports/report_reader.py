
import yaml
import logging

from google.protobuf.json_format import ParseDict, SerializeToJsonError, ParseError

import ncbi.datasets.v1alpha1.reports.virus_pb2 as virus_report_pb2
import ncbi.datasets.v1alpha1.reports.assembly_pb2 as assembly_report_pb2
import ncbi.datasets.v1alpha1.reports.gene_pb2 as gene_report_pb2


logger = logging.getLogger()


class DatasetsReportReader():
    # Update this to no longer open the file
    def _load_and_parse_report(self, report_file_name, schema_pb):
        with open(report_file_name) as fh:
            try:
                report_dict = yaml.safe_load(fh.read())
                if not report_dict:
                    logger.error(f"Empty report from file: {report_file_name}")
                    return
                try:
                    ParseDict(report_dict, schema_pb, ignore_unknown_fields=False)
                except (SerializeToJsonError, ParseError) as e:
                    logger.error(f"Error converting yaml to schema: {e}")
            except yaml.YAMLError as e:
                logger.error(f"Error while loading yaml: {e}")

    def assembly_report_from_file(self, report_file_name):
        schema_pb = assembly_report_pb2.AssemblyDataReport()
        self._load_and_parse_report(report_file_name, schema_pb)
        return schema_pb

    def gene_report_from_file(self, report_file_name):
        schema_pb = gene_report_pb2.GeneDescriptors()
        self._load_and_parse_report(report_file_name, schema_pb)
        return schema_pb

    # Do we allow the slow (full report approach) for virus
    # or only the generator?  I'm inclined to say only the generator
    # if for no other reason than to keep api simple
    def virus_report_from_file(self, report_file_name):
        schema_pb = virus_report_pb2.VirusReport()
        self._load_and_parse_report(report_file_name, schema_pb)
        return schema_pb

    # return instance of VirusReport class (replace above function)
    def read_virus_report_from_file(self, report_file_name):
        pass

    # Keep above functions to support file-name requests and add the following functions to
    # support file-handles (note above functions will then call these functions after opening the file)
    def assembly_report(self, report_file_handle):
        pass

    def gene_report(self, report_file_handle):
        pass

    # return VirusReport object
    def read_virus_report(self, report_file_handle):
        pass


def GetDatasetObject(zip_file_or_directory, dataset_type):
    if dataset_type == 'ASSEMBLY':
        return AssemblyDataset(zip_file_or_directory)
    elif dataset_type == 'GENE':
        return GeneDataset(zip_file_or_directory)
    elif dataset_type == 'VIRUS':
        return VirusDataset(zip_file_or_directory)
    raise ValueError(dataset_type)


# maybe we have subclasses based on type - gene/virus/assembly - that would clean up report access (and maybe
# other things in the future)
class Dataset():
    def __init__(self, zip_file_or_directory):
        # shoud be obvious which is which
        pass

    # return json catalog from zip file
    def get_catalog(self):
        pass

    # Get names of all report files
    def get_report_files(self):
        pass

    # Specific functions for other types of files? (fna, faa, ....)
    # returns contents of any file, probably as a string
    # these 2 functions have to take hydration into account
    def get_file(self, file_name):
        pass

    def get_file_handle(self, file_name):
        pass


# Subclassing option - TBD
class AssemblyDataset():
    def __init__(self, zip_file_or_directory):
        pass

    # returns protobuf for single report.  Maybe defaults to first/only report
    def get_report(self, report_file=""):
        pass


class GeneDataset():
    def __init__(self, zip_file_or_directory):
        pass

    # returns protobuf for single report.  Maybe defaults to first/only report
    def get_report(self, report_file=""):
        pass


class VirusDataset():
    def __init__(self, zip_file_or_directory):
        pass

    # iterates over virus assemblies in report and returns them one at a time
    def read_report(self, report_file=""):
        # call DataSetsReportReader with file handle
        # for 'virus assemblies in report file':
        #   yield VirusAssembly
        pass
