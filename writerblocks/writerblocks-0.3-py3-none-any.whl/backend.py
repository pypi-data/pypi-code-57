"""Backend: find, read, and recombine data."""

import argparse
import configparser
import json
import logging
import os
import os.path
import pypandoc
import yaml

from copy import deepcopy
from typing import Callable, Dict, Iterable, List, Optional, Set, Tuple, Union
from writerblocks.common import (FORMAT_FILENAME, CONFIG_FILENAME, INDEX_FILENAME,
                                 DEFAULT_FMT, INI_FILENAME, INDEX_FNAME_BEST,
                                 INDEX_FNAME_BROAD, options)


def __list_dir(dirname: str) -> List[str]:
    """Wrap os.listdir (for ease of unit testing)."""
    return os.listdir(dirname)


def full_path(filename: str) -> str:
    """Given a relative path within the base directory, get absolute path."""
    if os.path.abspath(filename) == filename:
        return filename
    else:
        return os.path.abspath(os.path.join(options.base_dir, filename))


def get_index_file_path(filename: Optional[str] = None):
    """Locate index file to read information from."""
    if not filename:
        candidates = [fname for fname in __list_dir(options.base_dir) if
                      INDEX_FNAME_BROAD.match(fname.lower())]
        assert candidates, "Couldn't find index file in {}!".format(
            options.base_dir)
        best_candidates = [fname for fname in candidates if
                           INDEX_FNAME_BEST.match(fname.lower())]
        if best_candidates:
            filename = best_candidates[0]
        else:
            filename = candidates[0]
    logging.debug("Reading index file {} from directory {}".format(
        filename, options.base_dir))
    return full_path(filename=filename)


def split_tags(tags: Union[List[str], Set[str], str]) -> Set[str]:
    """Given a representation of tags, turn it into a set."""
    if isinstance(tags, set):
        return tags
    if isinstance(tags, str):
        tags = [tags]
    split = set()
    for line in tags:
        split = split.union({word.strip() for word in line.split(',') if
                             word.strip()})
    return split


def extract_tags(lines: List[str]) -> Tuple[Set[str], List[str]]:
    """Given a list of strings beginning with tags block, parse out the tags.

    :returns tags, list of remaining contents of lines.
    """
    tags = set()
    idx = 0
    if isinstance(lines, str):
        lines = [lines]
    if not lines or not lines[0].lower().startswith("tags:"):
        return set(), lines
    for idx, line in enumerate(lines):
        if idx == 0:
            # First line starts with meta tags:, cut that part.
            line = line.split(':', 1)[-1]
        line = line.strip()
        if not line:
            # Done with tags.
            idx += 1
            break
        tags.update([word.strip() for word in line.split(',') if word.strip()])
    return tags, lines[idx:]


def extract_tags_from_file(filename: str) -> Set[str]:
    """Given a filename, read the tags block and return its contents.

    Faster than reading the entire file.
    """
    lines = []
    with open(filename, 'r') as fd:
        line = fd.readline()
        while line.strip():
            lines.append(line)
            line = fd.readline()
    return extract_tags(lines=lines)[0]


def prepend_tags(tags: Set[str], text: str):
    """Combine tags and text into a form suitable for writing to a file."""
    output = ""
    if tags:
        output += "tags: {}\n\n".format(','.join(tags))
    output += text
    return output


def read_files(*filenames: str) -> Tuple[Set[str], List[str]]:
    """Given the names of some files, parse out their tags and contents.

    :returns set of all tags and list of strings; each element in the list is
        the contents of one file, less the tag block.
    """
    text = []
    all_tags = set()
    for filename in filenames:
        with open(filename, 'r') as fd:
            lines = fd.readlines()
        tags, lines = extract_tags(lines)
        text.append(''.join(lines).strip('\n'))
        all_tags.update(tags)
    return all_tags, text


def preamble_to_tex() -> str:
    """If title file is not LaTeX, pandoc gets confused making PDFs.

    Convert it accordingly and return the path to the new file.
    """
    filename = full_path(options.fmt['preamble'])
    if filename.lower().endswith(".tex"):
        return filename
    tex_filename = full_path('preamble.tex')
    logging.debug("Looking for title file {}".format(filename))
    if os.path.exists(filename):
        pypandoc.convert_file(source_file=filename, to='latex',
                              outputfile=tex_filename, format=options.in_fmt)
        logging.debug("Title file converted to .tex.")
    return tex_filename


def write_contents_to_file(text: str, filename: Optional[str] = None) -> None:
    """Write output using pandoc."""
    filename = filename or options.out_file
    filename = full_path(filename)
    if options.in_fmt == options.out_fmt:
        with open(filename, 'w') as outfile:
            outfile.write(text)
    else:
        pypandoc.convert_text(source=text, to=options.out_fmt,
                              format=options.in_fmt, outputfile=filename,
                              extra_args=options.pandoc_args)


def get_file_tags(*filenames: str) -> Dict[str, Set[str]]:
    """Extract the tags from the specified files.

    :returns a dictionary {filename: tags}.
    """
    return {filename: extract_tags_from_file(filename) for filename in filenames}


def get_files_tagged(filenames: List[str], tags: Iterable[str],
                     blacklist_tags: Optional[Iterable[str]] = None,
                     match_all: bool = False) -> List[str]:
    """Given the names of files, return all that have the specified tags.

    If match_all is set, return only files that have all of the specified tags;
    otherwise, return files that match one or more tags.

    If a blacklist is provided, files whose tags match the blacklist will be
    excluded.
    """
    if (not tags and not blacklist_tags) or not filenames:
        return filenames
    if not blacklist_tags:
        blacklist_tags = []
    file_tags = get_file_tags(*filenames)
    if isinstance(tags, str):
        tags = [tags]
    if isinstance(blacklist_tags, str):
        blacklist_tags = [blacklist_tags]
    matches = []
    check = all if match_all else any
    for filename in filenames:
        if any(tag in file_tags[filename] for tag in blacklist_tags):
            continue
        if check(tag in file_tags[filename] for tag in tags):
            matches.append(filename)
    return matches


def read_org_file(org_file: str) -> Union[Dict, List]:
    """Read a JSON or YAML file containing organization information.

    Used for index, config and format files.
    """
    if org_file.lower().endswith("json"):
        reader = json.load
    else:
        reader = yaml.safe_load
    with open(org_file, 'r') as index:
        return reader(index)


class DataInfo(object):
    """Base class for tracking information about files, sections, etc."""

    def __init__(self, source: Union[str, Dict, List], level: int = 0,
                 prepend_sep: bool = True):
        """Generic setup for all DataInfo classes.

        Args:
            source: the information from the index that tells us about this
                data, such as a string containing the filename, a dictionary
                containing title and filename, or a list of such items.
            level: refers to the nesting level in the index for this data; for
                example, level 0 might be a chapter, level 1 a section, and
                level 3 a subsection.
            prepend_sep: whether to prepend a section separator to the text
                of this object when reproducing it.  One might choose not to if
                this is the beginning.
        """
        self.level = level
        if isinstance(source, dict):
            self.title = list(source.keys())[0]
        else:
            self.title = ''
        self.prepend_sep = prepend_sep or self.title
        self.sep = self.get_sep().format(self.title)
        self.filename = None
        self._text = None
        self._tags = set()

    def get_sep(self) -> str:
        """String to prepend to this item when concatenating with others."""
        try:
            return options.fmt['seps'][self.level]
        except (IndexError, KeyError):
            return options.fmt['default_sep']

    def __str__(self):
        return self.filename or self.title or "Empty {}".format(
            self.__class__.__name__)

    @property
    def text(self) -> str:
        """Textual contents of this object, including separator if appropriate."""
        raise NotImplementedError()

    @property
    def tags(self) -> Set[str]:
        """Data tags for this object."""
        return self._tags

    def flat_contents(self) -> List:
        """Helper for making a flat list of files."""
        raise NotImplementedError()


class FileInfo(DataInfo):
    """Represents an individual text file."""

    def __init__(self, source: Union[Dict, str], level: int = 0,
                 prepend_sep: bool = True):
        super(FileInfo, self).__init__(source=source, level=level,
                                       prepend_sep=prepend_sep)
        try:
            self.filename = os.path.abspath(os.sep.join([options.base_dir, source]))
        except TypeError:
            self.filename = os.path.abspath(os.sep.join(
                [options.base_dir, source[self.title]]))

    def __read_text(self) -> None:
        """Fetch and store the actual text/tags of this file."""
        if self._text is None:
            self._tags, self._text = read_files(self.filename)
            self._text = "".join(self._text)

    @property
    def text(self) -> str:
        """File contents, minus tags."""
        self.__read_text()
        if self.prepend_sep:
            return self.sep + self._text
        else:
            return self._text

    @property
    def tags(self) -> Set[str]:
        """Tags specific to this file."""
        self.__read_text()
        return self._tags

    def flat_contents(self) -> List[DataInfo]:
        """Helper for making a flat list of files."""
        return [self]


class SectionInfo(DataInfo):
    """Represents a grouping of multiple files' contents."""

    def __init__(self, source: Union[str, Dict, List], level: int = 0,
                 prepend_sep: bool = True):
        super(SectionInfo, self).__init__(source=source, level=level,
                                          prepend_sep=prepend_sep)
        self.contents = []
        if isinstance(source, dict):
            contents = list(source.values())
        elif isinstance(source, list):
            contents = source
        else:
            contents = [source]
        prepend_sep = False
        for value in contents:
            if isinstance(value, list) or isinstance(value, dict):
                value_type = SectionInfo
            else:
                value_type = FileInfo
            self.contents.append(value_type(level=level+1, source=value,
                                            prepend_sep=prepend_sep))
            prepend_sep = True

    @property
    def text(self) -> str:
        """Combined text of all files in this section."""
        mine = self.sep if self.prepend_sep else ''
        return mine + ''.join(thing.text for thing in self.contents)

    @property
    def tags(self) -> Set[str]:
        """Combined tags of all files in this section."""
        return set().union(*[thing.tags for thing in self.contents])

    def flat_contents(self) -> List[DataInfo]:
        """All files and separators in this section."""
        contents = []
        for item in self.contents:
            contents += item.flat_contents()
        return contents


def smart_info(source: Union[str, Dict, List], **kwargs) -> DataInfo:
    """Factory to create the appropriate DataInfo object from index data."""
    if isinstance(source, str) or (isinstance(source, dict) and any(
            isinstance(value, str) for value in source.values())):
        return FileInfo(source=source, **kwargs)
    else:
        return SectionInfo(source=source, **kwargs)


class IndexFile(object):
    """Wrapper for the data from index file."""
    def __init__(self, filename: Optional[str]):
        """Setup for the class.

        Args:
            filename: index file (overrides global options if given.)
        """
        self.filename = filename or options.index_file
        if not os.path.exists(self.filename):
            self.filename = get_index_file_path(self.filename)
        self._contents = None
        self._leveled = None
        self._ordered = None
        self._files = None

    @property
    def contents(self) -> List[DataInfo]:
        """Contents of the index file, as nested list."""
        if not self._contents:
            self._contents = []
            parsed_contents = read_org_file(self.filename)
            prepend_sep = False
            for item in parsed_contents:
                self._contents.append(smart_info(source=item, level=0,
                                                 prepend_sep=prepend_sep))
                prepend_sep = True
        return self._contents

    @property
    def ordered(self) -> List[DataInfo]:
        """Flat, ordered list of file contents."""
        if not self._ordered:
            self._ordered = []
            for item in self.contents:
                self._ordered += item.flat_contents()
        return self._ordered

    @property
    def files(self) -> List[str]:
        """Ordered list of the names of text files in the index."""
        if not self._files:
            self._files = [f.filename for f in self.ordered if f.filename]
        return self._files

    def tagged(self, tags: Optional[Iterable[str]] = None,
               blacklist_tags: Optional[Iterable[str]] = None,
               match_all: bool = False) -> List[DataInfo]:
        """Ordered list of file objects matching the given tags.

        If no tags are specified, identical to `IndexFile.ordered`.
        """
        if not tags and not blacklist_tags:
            return self.contents
        else:
            fnames = get_files_tagged(filenames=self.files, tags=tags,
                                      blacklist_tags=blacklist_tags,
                                      match_all=match_all)
            return [f for f in self.ordered if f.filename in fnames]

    def get_contents(self, tags: Optional[Iterable[str]] = None,
                     blacklist_tags: Optional[Iterable[str]] = None,
                     match_all: bool = False):
        """Combined tags and text of files matching given tag restrictions."""
        files = self.tagged(tags=tags, blacklist_tags=blacklist_tags,
                            match_all=match_all)
        tags = set().union(*[f.tags for f in files])
        text = ''.join([f.text for f in files])
        return tags, text.lstrip()

    def text(self, **kwargs) -> str:
        """Combined text of files matching given tag restrictions.

        See `IndexFile.get_contents` for information about kwargs.
        """
        return self.get_contents(**kwargs)[1]


def combine_from_index(index_filename: str, include_tags: bool = False,
                       **kwargs) -> str:
    """Combine text of files found in index matching tags."""
    index = IndexFile(filename=index_filename)
    tags, text = index.get_contents(**kwargs)
    if include_tags:
        return prepend_tags(tags=tags, text=text)
    else:
        return text


def new_project() -> None:
    """Create files for a new project."""
    os.makedirs(options.base_dir, exist_ok=True)
    fmt_file = full_path(FORMAT_FILENAME)
    index_file = full_path(INDEX_FILENAME)
    if not os.path.exists(fmt_file):
        with open(fmt_file, 'w') as fmt:
            yaml.safe_dump(DEFAULT_FMT, fmt)
    if not os.path.exists(index_file):
        with open(index_file, 'w') as idx:
            idx.write('')
    create_ini()


def parse_ini() -> configparser.ConfigParser:
    """Parse configuration file."""
    ini_path = full_path(INI_FILENAME)
    config = configparser.ConfigParser()
    opts = vars(options)
    config['config'] = deepcopy(opts)
    config['config'].pop('fmt')
    if os.path.exists(ini_path):
        config.read(ini_path)
        for var in config['config']:
            opts[var] = yaml.safe_load(config['config'][var])
    return config


def create_ini() -> configparser.ConfigParser:
    """Create a new default configuration file if none exists.

    Returns the configuration stored in that file.
    """
    ini_path = full_path(INI_FILENAME)
    config = parse_ini()
    if not os.path.exists(ini_path):
        with open(ini_path, 'w') as outfile:
            config.write(outfile)
    return config


def read_and_replace_old_config() -> configparser.ConfigParser:
    """Replace config.yaml with writerblocks.ini."""
    config_filename = full_path(CONFIG_FILENAME)
    if os.path.exists(config_filename):
        logging.warning("Converting config.yaml to writerblocks.ini section")
        config_contents = read_org_file(config_filename)
        opts = vars(options)
        for opt in config_contents:
            opts[opt] = config_contents[opt]
        os.remove(config_filename)
    ini_contents = create_ini()
    return ini_contents


def parse_options(user_args: argparse.Namespace,
                  pandoc_args: Optional[List[str]]) -> argparse.Namespace:
    """Collect and organize the various options set by the user.

    Priority: user-specified options override config-file options, which
    in turn override the default options.
    """
    if pandoc_args:
        user_args.pandoc_args = pandoc_args
    # Need to identify base directory to find config files.
    if user_args.base_dir:
        options.base_dir = user_args.base_dir

    # Load config file options.
    read_and_replace_old_config()

    # Load format file.
    fmt_filename = full_path(FORMAT_FILENAME)
    options.fmt = read_org_file(fmt_filename) if os.path.exists(fmt_filename) else DEFAULT_FMT

    # Only try to find index file if we expect it to exist.
    if user_args.index_file and not user_args.new_project:
        options.index_file = get_index_file_path(filename=user_args.index_file)

    # Convert to dicts for ease of combining.
    user_opts = vars(user_args)
    base_opts = vars(options)
    # Replace with command-line options next.
    for opt in user_opts:
        if user_opts[opt] is not None:
            base_opts[opt] = user_opts[opt]
    # Make nice sets of tags.
    if options.tags:
        options.tags = split_tags(tags=options.tags)
    if options.blacklist_tags:
        options.blacklist_tags = split_tags(options.blacklist_tags)

    # Finally, if there's a specified "preamble" file be sure we include it.
    if options.fmt.get('preamble'):
        preamble = preamble_to_tex()
        if os.path.exists(preamble):
            options.pandoc_args.append('--include-before-body={}'.format(preamble))
    return options


def run(action_on_error: Optional[Callable] = lambda: None) -> str:
    """Core program functionality, called after options are set.

    Args:
        action_on_error: optional function to run if we fail to find the index
            file correctly.
    """
    if options.new_project:
        new_project()
        return "Created project files in {}".format(options.base_dir)
    try:
        text = combine_from_index(index_filename=options.index_file,
                                  match_all=options.all_tags,
                                  include_tags=False)
        write_contents_to_file(text=text)
        return "Successfully created {}".format(options.out_file)
    except FileNotFoundError:
        # Probably there's no index file, execute specified function.
        action_on_error()
        raise
