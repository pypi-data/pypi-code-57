import jinja2
import logging
import os
from bookbook.latex import combine_and_convert
from pathlib import Path

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


class BookContext:
    """
    A context manager to work in a directory with a temporary file
    """

    def __init__(self, filename, filecontent: str, work_path: Path):
        self.filepath = Path(filename)
        self.filecontent = filecontent
        self.work_path = work_path
        self.curdir = None

    def __enter__(self):
        self.initial_path = Path.cwd()
        os.chdir(self.work_path)
        with open(self.filepath, 'w') as f:
            f.write(self.filecontent)
        return self

    def __exit__(self, *args):
        self.filepath.unlink()
        os.chdir(self.initial_path)


class Book:
    """A book to be built with bookbook"""

    bookbook_filename = 'bookbook_filename.tex'

    def __init__(self, conf):

        self.output_path = conf['output_path']
        self.project_path = conf['project_path']
        self.titlepage_path = conf['pages']['path'] / conf['book']['titlepage']
        self.book_title = conf['book']['file']
        self.template_path = conf['template_path'].as_posix()

    def build(self):
        """Build book"""

        # Render basic bookbook template including /pages/titlepage.tex content
        env = jinja2.Environment(loader=jinja2.FileSystemLoader(
                                 self.template_path))
        template = env.get_template('book.tplx')

        with open(self.titlepage_path) as f:
            titlepage_content = f.read()
        bookbook_template = template.render(titlepage=titlepage_content)

        # Work temporarly in self.output_path directory
        with BookContext(Path(self.bookbook_filename), bookbook_template,
                         self.output_path):

            # Call bookbook
            combine_and_convert(Path('.'),
                                Path(self.book_title),
                                pdf=True,
                                template_file=self.bookbook_filename)
