# from __future__ import annotations
#
# import pytest
#
# from viewdom.h2 import VDOM2, html, render
#
#
# @pytest.fixture
# def vdom_one() -> VDOM2:
#     vo = html('<div id="1">A <span>2</span> B</div>')
#     return vo
#
#
# def test_render(vdom_one):
#     assert 'div' == vdom_one.tag
#     assert dict(id="1") == vdom_one.props
#     assert 'A ' == vdom_one.children[0]
#     assert 'span' == vdom_one.children[1].tag
#     assert dict() == vdom_one.children[1].props
#     assert '2' == vdom_one.children[1].children[0]
#     assert ' B' == vdom_one.children[2]
#
#     result = render(vdom_one)
#     assert 9 == result
