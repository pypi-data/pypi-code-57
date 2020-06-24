from typing import List, Dict, Any
from pathlib import Path
from .rst_analyzer import RstAnalyzer


class RstLoader:

    def __init__(self, root: str, analyzer: RstAnalyzer) -> None:
        self._nodes: List[Dict[str, Any]] = []
        self.root = root
        self.analyzer = analyzer

    @property
    def nodes(self):
        if not self._nodes:
            self.load()
        return self._nodes

    def load(self):
        path = Path(self.root)

        nodes_dict = {}
        for node in sorted(path.rglob('*.rst')):
            data = self._analyze_node(node)

            if 'index.rst' in node.name:
                node = node.parent
                data['summary'] = True

            metadata = {
                'file_name': node.name,
                'parent_dir': node.parent.name,
                'parent_absolute': str(node.parent.absolute())
            }

            nodes_dict[str(node.absolute())] = {**metadata, **data}

        for value in nodes_dict.values():
            value['id'] = self._extract_id(value)
            value['parent_id'] = self._extract_parent_id(nodes_dict, value)
            self._nodes.append(value)

    def _analyze_node(self, node: Path) -> Dict[str, Any]:
        data_dict = self._extract_content(node)
        return data_dict

    def _extract_content(self, node: Path) -> Dict[str, Any]:
        content = node.read_text()
        return self.analyzer.analyze(content)

    def _extract_id(self, value: Dict[str, Any]) -> str:
        _id = value.get('id', '')
        if _id:
            return _id

        file_name = value.get('file_name', '')
        parent_dir = value.get('parent_dir', '')

        if '_' in file_name:
            _id, *rest = file_name.split('_')
        elif '_' in parent_dir:
            _id, *rest = parent_dir.split('_')

        return _id

    def _extract_parent_id(self, nodes_dict: Dict[str, Any],
                           value: Dict[str, Any]) -> str:
        parent_value = nodes_dict.get(value.get('parent_absolute', ''))
        if not parent_value:
            return ''

        return self._extract_id(parent_value)
