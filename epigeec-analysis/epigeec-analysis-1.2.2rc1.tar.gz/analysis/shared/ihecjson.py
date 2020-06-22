from __future__ import absolute_import, division, print_function

import json
import sys
import argparse

class IhecJson(object):
    """
    """
    def __init__(self):
        self.content = []
        self.count = 0

    @staticmethod
    def epigeec_format(ihec_json):
        """
        """
        ihec = IhecJson()
        ihec._load(ihec_json)
        return ihec.epigeec_dict()

    def load(self, ihec_json_file):
        """
        """
        self._load(json.load(ihec_json_file))

    def _load(self, ihec_json):
        """
        """
        hub_description = ihec_json['hub_description']
        datasets = ihec_json['datasets']

        publishing_group = hub_description["publishing_group"]
        releasing_group = hub_description.get("releasing_group", publishing_group)
        assembly = hub_description["assembly"]
        for dataset_name, data in datasets.items():
            ihecdata = data.get("ihec_data_portal", {})
            assay = ihecdata.get("assay", "N/A")
            assay_category = ihecdata.get("assay_category", "N/A")
            cell_type = ihecdata.get("cell_type", "N/A")
            cell_type_category = ihecdata.get("cell_type_category", "N/A")
            publishing_group = ihecdata.get('publishing_group', 'N/A')
            releasing_group = ihecdata.get('releasing_group', 'N/A')

            #signal type priority
            for signal_type in ["methylation_profile", "signal_forward", "signal_unstranded", "signal"]:
                signal_data = data.get("browser", {}).get(signal_type, [{}])[0]
                if signal_data:
                    break

            md5sum = signal_data.get("md5sum")
            if md5sum is None:
                continue
            unique_id = str(self.count)
            self.count += 1
            parsed_dataset = {
                "assembly": assembly,
                "publishing_group": publishing_group,
                "releasing_group": releasing_group,
                "assay": assay,
                "assay_category": assay_category,
                "cell_type": cell_type,
                "cell_type_category": cell_type_category,
                "file_name": dataset_name,
                "md5sum": md5sum,
                "id": unique_id,
            }
            parsed_dataset["virtual"] = (signal_type == "signal_forward")
            self.content.append(parsed_dataset)

    def epigeec_dict(self):
        """
        """
        return {"datasets":self.content}

    def __str__(self):
        """
        """
        return json.dumps(self.epigeec_dict())


def main():
    """
    """
    ihec_json_paths = sys.argv[1:]
    ihec_json = IhecJson()
    for ihec_json_path in ihec_json_paths:
        ihec_json.load(open(ihec_json_path))
    print(ihec_json)

if __name__ == "__main__":
    main()