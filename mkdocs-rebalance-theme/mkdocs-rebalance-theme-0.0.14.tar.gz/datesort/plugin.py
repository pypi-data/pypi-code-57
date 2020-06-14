import os
import sys
import copy
import shutil
import logging
import datetime

import yaml

from operator import attrgetter, itemgetter

from mkdocs.plugins import BasePlugin
from mkdocs.structure.pages import Page
from mkdocs.structure.files import File, Files
from mkdocs.structure.nav import Section
from mkdocs.commands.build import _build_page
from mkdocs.config.config_options import Type


log = logging.getLogger(__name__)

DEBUG=False

class DatesortPlugin(BasePlugin):

    config_scheme = (
        ('format', Type(str, default='%d/%m/%Y')),
        ('reverse', Type(bool, default=True))
    )


    def on_config(self, config):
        self.date_format = self.config.get('format')
        self.reverse = self.config.get('reverse')
        print(self.config)


    def on_files(self, files, config):
        print(files)

        out_files = []
        md_files = []

        # Scan the list of files to extract tags from meta
        for f in files:
            if not f.is_documentation_page():
                print(f.src_path)
                out_files.append(f)
                continue

            metadata = get_metadata(f.src_path, config["docs_dir"])
            print(metadata)
        
            file_date = metadata.get('date')
            if file_date:
                file_datetime = datetime.datetime.strptime(file_date,
                        self.date_format)
                f.datestamp = file_datetime
            else:
                f.datestamp = datetime.datetime.fromtimestamp(os.path.getmtime(os.path.join(
                    config["docs_dir"],
                    f.src_path
                )))

            md_files.append(f)
            print(f.datestamp)

        sorted_files = sorted(md_files, key=attrgetter('datestamp'),
                reverse=self.reverse)

        print("REVERSE:", self.reverse)
        out_files.extend(sorted_files)
        return Files(out_files)



def get_metadata(name, path):
    # Extract metadata from the yaml at the beginning of the file
    def extract_yaml(f):
        result = []
        c = 0
        for line in f:
            if line.strip() == "---":
                c +=1
                continue
            if c==2:
                break
            if c==1:
                result.append(line)
        return "".join(result)

    with open(os.path.join(path, name)) as f:
        metadata = extract_yaml(f)
        if metadata:
            meta = yaml.load(metadata, Loader=yaml.FullLoader)
            meta.update(filename=name)
            return meta
