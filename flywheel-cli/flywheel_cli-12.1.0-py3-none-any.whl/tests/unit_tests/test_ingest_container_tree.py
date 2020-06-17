import io
import re
from uuid import UUID, uuid4

import pytest

from flywheel_cli.ingest import container_tree


def test_container_node_default_values():
    node = container_tree.ContainerNode(1)

    assert node.id is not None
    assert isinstance(node.id, UUID)
    assert node.level == 1
    assert node.parent is None
    assert node.src_context is None
    assert node.dst_context is None
    assert node.dst_files == []
    assert node.exists is None
    assert node.children == []
    assert node.bytes_sum == 0
    assert node.files_cnt == 0

def test_container_node():
    params = {
        'level': 1,
        'id_': uuid4(),
        'parent': container_tree.ContainerNode(2),
        'src_context': {'src': 'ctx'},
        'dst_context': {'dst': 'ctx'},
        'dst_files': ['file1', 'file2'],
        'exists': True,
        'bytes_sum': 1234,
        'files_cnt': 5
    }
    node = container_tree.ContainerNode(**params)

    assert node.id == params['id_']
    assert node.level == params['level']
    assert node.parent == params['parent']
    assert node.src_context == params['src_context']
    assert node.dst_context == params['dst_context']
    assert node.dst_files == params['dst_files']
    assert node.exists == params['exists']
    assert node.children == []
    assert node.bytes_sum == params['bytes_sum']
    assert node.files_cnt == params['files_cnt']

def test_container_node_str_label():
    params = {
        'level': 1,
        'id_': uuid4(),
        'src_context': {'label': 'src_label', '_id': 'src_id'},
        'dst_context': {'label': 'dst_label', '_id': 'dst_id'},
        'exists': False,
        'bytes_sum': 1234,
        'files_cnt': 1
    }

    # existing
    node = container_tree.ContainerNode(**params)
    node_str = remove_color_formatting(str(node))
    assert node_str == "dst_label (1.2 KB / 1 file) (using)"

    # not existing
    node.exists = False
    node_str = remove_color_formatting(str(node))
    assert node_str == "dst_label (1.2 KB / 1 file) (creating)"

    # use dst_context id
    node.dst_context = {'_id': 'dst_id'}
    node_str = remove_color_formatting(str(node))
    assert node_str == "dst_id (1.2 KB / 1 file) (creating)"

    # use dst_context but no label
    node.dst_context = {'random': 'random'}
    node_str = remove_color_formatting(str(node))
    assert node_str == "NO_LABEL (1.2 KB / 1 file) (creating)"

    # use src_context
    node.dst_context = {}
    node_str = remove_color_formatting(str(node))
    assert node_str == "src_label (1.2 KB / 1 file) (creating)"

    # no context
    node.dst_context = None
    node.src_context = None
    node_str = remove_color_formatting(str(node))
    assert node_str == "NO_LABEL (1.2 KB / 1 file) (creating)"

def test_container_node_str_files():
    params = {
        'level': 1,
        'id_': uuid4(),
        'dst_context': {'label': 'dst_label', '_id': 'dst_id'},
    }

    node = container_tree.ContainerNode(**params)
    node_str = remove_color_formatting(str(node))
    assert node_str == "dst_label (using)"

    # file cnt only
    params['files_cnt'] = 1
    node = container_tree.ContainerNode(**params)
    node_str = remove_color_formatting(str(node))
    assert node_str == "dst_label (using)"

    # file cnt AND byte count
    params['bytes_sum'] = 1234
    node = container_tree.ContainerNode(**params)
    node_str = remove_color_formatting(str(node))
    assert node_str == "dst_label (1.2 KB / 1 file) (using)"

    # multiple file AND byte count
    params['files_cnt'] = 2
    node = container_tree.ContainerNode(**params)
    node_str = remove_color_formatting(str(node))
    assert node_str == "dst_label (1.2 KB / 2 files) (using)"

    # multiple file AND byte count AND creating
    params['dst_context'] = None
    node = container_tree.ContainerNode(**params)
    node_str = remove_color_formatting(str(node))
    assert node_str == "NO_LABEL (1.2 KB / 2 files) (creating)"

     # multiple file AND byte count AND force exists
    params['exists'] = True
    node = container_tree.ContainerNode(**params)
    node_str = remove_color_formatting(str(node))
    assert node_str == "NO_LABEL (1.2 KB / 2 files) (using)"

def test_container_tree():
    tree = container_tree.ContainerTree()
    assert isinstance(tree.root, container_tree.ContainerNode)
    assert len(tree.nodes) == 1

def test_container_tree_add_node():
    params = {
        'level': 1,
        'id_': uuid4(),
        'bytes_sum': 1234,
        'files_cnt': 5
    }

    tree = container_tree.ContainerTree()

    tree.add_node(
        params['id_'],
        None,
        params['level'],
        bytes_sum=params['bytes_sum'],
        files_cnt=params['files_cnt']
    )

    # add node
    assert len(tree.nodes) == 2
    assert tree.nodes[params['id_']].parent == tree.root
    assert tree.nodes[params['id_']] in tree.root.children

    # count files
    assert tree.root.files_cnt == 5
    assert tree.root.bytes_sum == 1234

    # add new node to the last node
    params2 = {
        'level': 2,
        'id_': uuid4(),
        'bytes_sum': 2345,
        'files_cnt': 10
    }
    tree.add_node(
        params2['id_'],
        params['id_'],
        params2['level'],
        bytes_sum=params2['bytes_sum'],
        files_cnt=params2['files_cnt']
    )

    assert len(tree.nodes) == 3
    assert tree.nodes[params2['id_']].parent == tree.nodes[params['id_']]
    assert tree.nodes[params2['id_']] not in tree.root.children
    assert tree.nodes[params2['id_']] in tree.nodes[params['id_']].children

    # count files
    assert tree.root.files_cnt == 5 + 10
    assert tree.root.bytes_sum == 1234 + 2345
    # 1st child
    node = tree.nodes[params['id_']]
    assert node.files_cnt == 5
    assert node.bytes_sum == 1234 + 2345
    # 2nd child
    node = tree.nodes[params2['id_']]
    assert node.files_cnt == 10
    assert node.bytes_sum == 2345

def test_container_tree_add_node_twice():
    id_ = uuid4()
    tree = container_tree.ContainerTree()

    tree.add_node(
        id_,
        None,
        1
    )

    # add node
    assert len(tree.nodes) == 2
    assert tree.nodes[id_].level == 1

    tree.add_node(
        id_,
        None,
        2
    )

    # add node
    assert len(tree.nodes) == 2
    assert tree.nodes[id_].level == 1

def test_container_tree_print_not_utf8(tree_data):
    out = io.StringIO()
    tree_data.print_tree(out)
    out.seek(0)

    lines = [
        "`- label_1 (13.0 KB / 5 files) (using)",
        "   |- label_1_1 (8.0 KB / 7 files) (using)",
        "   |  `- label_2_1 (4.0 KB / 9 files) (using)",
        "   `- label_1_2 (4.0 KB / 8 files) (using)",
        "`- label_2 (2.0 KB / 6 files) (using)",
    ]

    print_lines = out.readlines()
    assert len(print_lines) == len(lines)
    for i in range(len(print_lines)):
        l = remove_color_formatting(print_lines[i]).rstrip()
        assert l == lines[i]

def test_container_tree_print_utf8(tree_data):
    out = UTF8StringIO()
    tree_data.print_tree(out)
    out.seek(0)

    lines = [
        "└─ label_1 (13.0 KB / 5 files) (using)",
        "   ├─ label_1_1 (8.0 KB / 7 files) (using)",
        "   │  └─ label_2_1 (4.0 KB / 9 files) (using)",
        "   └─ label_1_2 (4.0 KB / 8 files) (using)",
        "└─ label_2 (2.0 KB / 6 files) (using)",
    ]

    print_lines = out.readlines()
    assert len(print_lines) == len(lines)
    for i in range(len(print_lines)):
        l = remove_color_formatting(print_lines[i]).rstrip()
        assert l == lines[i]

@pytest.fixture(scope="function")
def tree_data():
    ids = [
        uuid4(),
        uuid4(),
        uuid4(),
        uuid4(),
        uuid4(),
    ]

    tree = container_tree.ContainerTree()
    tree.add_node(
        level=1,
        id_=ids[0],
        parent=None,
        bytes_sum=1024,
        files_cnt=5,
        dst_context={'label': 'label_1'},
    )
    tree.add_node(
        level=1,
        id_=ids[1],
        parent=None,
        bytes_sum=2048,
        files_cnt=6,
        dst_context={'label': 'label_2'},
    )
    tree.add_node(
        level=2,
        id_=ids[2],
        parent=ids[0],
        bytes_sum=4096,
        files_cnt=7,
        dst_context={'label': 'label_1_1'},
    )
    tree.add_node(
        level=2,
        id_=ids[3],
        parent=ids[0],
        bytes_sum=4096,
        files_cnt=8,
        dst_context={'label': 'label_1_2'},
    )
    tree.add_node(
        level=3,
        id_=ids[4],
        parent=ids[2],
        bytes_sum=4096,
        files_cnt=9,
        dst_context={'label': 'label_2_1'},
    )

    return tree

def remove_color_formatting(txt):
    """
    code from
    https://stackoverflow.com/questions/14693701/how-can-i-remove-the-ansi-escape-sequences-from-a-string-in-python
    """
    ansi_escape = re.compile(r'''
        \x1B  # ESC
        (?:   # 7-bit C1 Fe (except CSI)
            [@-Z\\-_]
        |     # or [ for CSI, followed by a control sequence
            \[
            [0-?]*  # Parameter bytes
            [ -/]*  # Intermediate bytes
            [@-~]   # Final byte
        )
    ''', re.VERBOSE)
    return ansi_escape.sub('', txt)

class UTF8StringIO(io.StringIO):
    encoding = "UTF-8"
