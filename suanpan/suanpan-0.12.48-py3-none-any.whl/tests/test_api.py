from suanpan import api, g

g.debug = True

print(api.call(12345, "test", {"test": "data"}))
