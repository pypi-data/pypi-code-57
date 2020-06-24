from docutils.parsers.rst import Parser  # type: ignore
from docutils.frontend import OptionParser
from docutils.utils import new_document
from docutils.nodes import Node, NodeVisitor, field, title  # type: ignore


class RstAnalyzer:

    def analyze(self, content: str):
        parser = Parser()
        components = (Parser,)
        settings = OptionParser(components=components).get_default_values()
        document = new_document('<rst-doc>', settings=settings)
        parser.parse(content, document)

        result = {}

        def assign_result(value):
            entries = value.split('\n')
            for entry in entries:
                key, value = entry.split('=')
                value = value.strip()
                if ',' in value:
                    value = [item.strip() for item in value.split(',')]
                result[key.strip()] = value

        visitor = _RstVisitor(document, callback=assign_result)
        document.walk(visitor)
        return result


class _RstVisitor(NodeVisitor):

    def __init__(self, *attrs, tag: str = 'estimark', callback=None) -> None:
        super().__init__(*attrs)
        self.tag = tag
        self.callback = callback
        self.title: str = ''

    def visit_title(self, node) -> None:
        if not self.title and self.callback:
            self.title = "name={0}".format(node[0])
            self.callback(self.title)

    def visit_field(self, node) -> None:
        """Called for "reference" nodes."""
        key = node[0][0]
        if key == self.tag and self.callback:
            value = node[1][0][0]
            self.callback(value)

    def unknown_visit(self, node: Node) -> None:
        """Called for all other node types."""
