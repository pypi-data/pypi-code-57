""" This file is based on DataFile.cpp from endless-sky 0.9.12.

    Instead of going through each char one by one, we uses regex to avoid loops.
"""

import os, re, logging

from .datanode import DataNode

WARN_MIXED_WHITESPACE = True

# Every char <= " " is whitespace, except \n
WHITESPACE = "".join(
    chr(c) for c in range(ord(" ") + 1) if c not in (ord(n) for n in "\n")
)
WHITESPACE_RE = re.compile("[" + WHITESPACE + "]")
NOT_WHITESPACE_RE = re.compile("[^" + WHITESPACE + "]")


class DataFile:
    """ A simple wrapper around a file containing DataNodes.

        It is not really needed in python, but let's us stay closer to the C++
        side of things.
        Instances have
        `root` attribute, which is a DataNode representing the file,
        `source` attribute, which is a string with the origin file path or None
        `warning_mixed_ws` attribute, a boolean enabling logging messages about mixed
            usage (which slows things down)
    """

    def __init__(self, path_or_file=None, warn_mixed_ws=WARN_MIXED_WHITESPACE):
        self.warn_mixed_ws = warn_mixed_ws
        self.source = None
        self.root = DataNode()
        if path_or_file is not None:
            self.load(path_or_file)

    def load(self, path_or_file_or_list):
        """ Load nodes from a filelike, os.PathLike or simply a list of strings. """

        try:
            self.source = path_or_file_or_list.filename
        except AttributeError:
            pass

        # We may be given a simple string, so try this first
        try:
            path = os.fspath(path_or_file_or_list)
        except TypeError:
            # OK, so it was neither a string nor a pathlib.Path or something like it.
            # We can treat files as a list of strings, too, so we do just that.
            stack = [self.root]
            whiteStack = [-1]
            fileIsSpaces = warned = False
            for linenumber, line in enumerate(path_or_file_or_list):
                linenumber += 1  # linenumbers start at 1
                logging.debug("Line {}: {!r}".format(linenumber, line))
                # C++ As a sentinel, make sure the file always ends in a newline.
                if line == "" or line[-1] != "\n":
                    line += "\n"
                white = 0
                # C++ Find the first non-white character in this line
                # (as \n isn't a "white" char, the re will always find something)
                white = NOT_WHITESPACE_RE.search(line).start()

                # C++ Warn about mixed indentations when parsing files.
                if self.warn_mixed_ws:
                    wschars = line[:white]
                    spacescount = wschars.count(" ")
                    fileIsSpaces = spacescount > 0 or fileIsSpaces
                    if spacescount not in (0, len(wschars)):
                        logging.warning(
                            "{}:{} Mixed whitespace usage in line".format(
                                self.source, linenumber
                            )
                        )
                    if (
                        linenumber > 0
                        and spacescount
                        and not fileIsSpaces
                        and not warned
                    ):
                        logging.warning(
                            "{}:{} Mixed whitespace usage in file".format(
                                self.source, linenumber
                            )
                        )
                        warned = True

                # C++ Skip empty lines (including comment lines).
                if line[white] in ("#", "\n"):
                    continue

                # C++ Determine where in the node tree we are inserting this node, based on
                # C++ whether it has more indentation than the previous node, less, or the same.
                while whiteStack[-1] >= white:
                    whiteStack.pop(-1)
                    stack.pop(-1)

                # C++ Add this node as a child of the proper node.
                children = stack[-1].children
                node = DataNode()
                children.append(node)
                node.line_number = linenumber

                # C++ Remember where in the tree we are.
                stack.append(node)
                whiteStack.append(white)

                # C++ Tokenize the line. Skip comments and empty lines.
                line = line[white:]
                while line != "\n":
                    # C++ Check if this token begins with a quotation mark. If so, it will
                    # C++ include everything up to the next instance of that mark.
                    # (or \n, and otherwise we will look for WHITESPACE again)
                    if line[0] in ('"', "`"):
                        split = line[1:].split(line[0], 1)
                        if len(split) > 1:
                            token, line = split
                        else:
                            logging.warning(
                                "{}:{} Closing quotation mark is missing".format(
                                    self.source, linenumber
                                )
                            )
                            token, line = line[:-1], "\n"
                    else:
                        s = WHITESPACE_RE.search(line)
                        end = s.start() if s else -1
                        token, line = line[:end], line[end:]
                    logging.debug("Token {!r}, Rest {!r}".format(token, line))
                    node.tokens.append(token)
                    logging.debug(repr(node.tokens))

                    nextpos = NOT_WHITESPACE_RE.search(line).start()
                    line = line[nextpos:]
        else:
            with open(path) as f:
                self.load(f)
            self.source = path
