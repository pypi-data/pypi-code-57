import pytest
from easy_publish import generate_posts, generate_parsed_post_list, PostParser, PostCollection


@pytest.fixture(scope="module")
def fakenotes_files():
    return ['./tests/fakenotes/note.md',
             './tests/fakenotes/other.md',
             './tests/fakenotes/other-note-two.md']

@pytest.fixture(scope="module")
def fakenotes_file():
    return './tests/fakenotes/note.md'

@pytest.fixture(scope="module")
def parsed_posts(fakenotes_files):
    parsed_posts = generate_parsed_post_list(fakenotes_files)
    return parsed_posts

def test_generate_posts():
    # incomplete
    posts = generate_posts("./tests/fakenotes")
    assert posts.__class__.__name__ == 'PostCollection'

def test_PostCollection(parsed_posts):
    # incomplete
    post_collection = PostCollection(parsed_posts)
    assert post_collection.posts.__class__.__name__ == "dict"
    assert post_collection.metadata.__class__.__name__ == "list"

def test_Metadata():
    pass

def test_PostParser(fakenotes_file):
    # incomplete
    p = PostParser(fakenotes_file)
    assert p.file == "./tests/fakenotes/note.md"
    assert p.title == "This is the fakenote"
    assert p.date == "5-23-94"
    assert p.author == "Sam Dixon"
    assert p.tags == ["first post", "item", "blogpost"]
    assert p.content
