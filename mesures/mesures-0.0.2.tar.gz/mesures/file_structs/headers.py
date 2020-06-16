import yaml

HEADERS = []
with open('headers.yaml') as f:
    data = yaml.load_all(f, Loader=yaml.Loader)
    for x in data:
        HEADERS.append(x)
