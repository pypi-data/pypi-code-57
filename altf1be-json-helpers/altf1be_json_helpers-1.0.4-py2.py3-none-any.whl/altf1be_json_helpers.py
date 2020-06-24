# -*- coding: utf-8 -*-

import os
import json
from pathlib import Path

from datetime import datetime
from altf1be_helpers import AltF1BeHelpers


class AltF1BeJSONHelpers:
    """ Simple helper to load, save and save with date time a JSON file

    """
    @property
    def filename(self):
        return self.__filename

    @filename.setter
    def filename(self, filename):
        self.__filename = os.path.join(
            # AltF1BeHelpers.output_directory(), # TODO remove this line to generalize the management of the files
            filename
        )

    def __init__(self):
        pass

    def save_with_datetime(self, data, filename):
        filename_path = os.path.dirname(filename)
        filename = datetime.now().strftime(
            f'%Y-%m-%d_%H-%M-%S-{os.path.basename(filename)}'
        )
        self.save(
            data=data,
            filename=os.path.join(
                # AltF1BeHelpers.output_directory(
                #     ['api']
                # ),
                filename_path,
                filename
            )
        )

    def save(self, data, filename=None):
        """
            store json file under filename/credentials by default
        """
        if (filename):
            self.filename = filename

        Path(os.path.dirname(self.filename)).mkdir(
            parents=True, exist_ok=True)

        with open(self.filename, 'w', encoding='utf-8') as f:
            json.dump(json.loads(data), f, ensure_ascii=False, indent=4)

    def load(self, filename):
        if (filename):
            self.filename = filename

        with open(self.filename) as json_file:
            data = json.load(json_file)
        return data


if __name__ == "__main__":
    altF1BeJSONHelpers = AltF1BeJSONHelpers()
    data = altF1BeJSONHelpers.load(
        os.path.join(
            "data", "altf1be_sample.json"
        )
    )
    print(data)

    data_str = json.dumps(data)
    altF1BeJSONHelpers.save(
        data_str,
        os.path.join(
            "data", "altf1be_sample_output.json"
        )
    )

    altF1BeJSONHelpers.save_with_datetime(
        data_str,
        os.path.join(
            "data", "altf1be_sample_with_date_time_output.json"
        )
    )
