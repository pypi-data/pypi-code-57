from .clinvar_xml import ClinvarXMLSource
from .mitomap import MitomapFileSource
from .uniprot import UniprotFileSource

source_name_map = {
    "clinvar_xml": ClinvarXMLSource,
    "mitomap": MitomapFileSource,
    "uniprot": UniprotFileSource,
}

__all__ = ("ClinvarXMLSource", "MitomapFileSource", "UniprotFileSource")
