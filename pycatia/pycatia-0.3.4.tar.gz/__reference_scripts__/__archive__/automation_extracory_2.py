import datetime
from pathlib import Path
from pprint import PrettyPrinter

from bs4 import BeautifulSoup

from helper_classes.automation_class import CATIA

now = datetime.datetime.now()
pp = PrettyPrinter(indent=4).pprint

doc_path = Path(
    '/home/evereux/python/projects/pycatia/__reference_scripts__/v5automation_files-r25/generated/interfaces')
test_doc = Path(
    '/home/evereux/python/projects/pycatia/__reference_scripts__/v5automation_files-r25/generated/interfaces/CATGSMIDLItf/interface_HybridShapeCurveSmooth_33499.htm')


def read_file(file):
    method_string = None
    with open(file, 'r') as f:
        soup = BeautifulSoup(f, 'html.parser')
        text = soup.text
        print(text)
        # text = text.strip()
        # text = text.replace('\n\n\n\n\n', '\n\n')
        # text = text.rsplit('\n', 1)[0]
        # text = text.strip()

        # if "Methods" in text:
        #     method_string = text.split("Methods", 1)[1].strip()
        #     method_string = '\n' + method_string
        #     methods = method_string.split('\no ')
        #     for method in methods:
        #         print(method)


if __name__ == "__main__":
    htm_file = test_doc

    read_file(htm_file)
