from lib_template.hello_world import hello_world, time_now


def test_hello_world():
    name = "John"
    assert f"Hello World {name}" == hello_world(name)


def test_time_now():
    assert time_now()
