from dogebuild.dogefile_internals.context import lifecycle


def proto_mode():
    lifecycle({"proto-sources": [], "build": ["proto-sources"]})
