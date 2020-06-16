import ujson as json
import argparse
import types

def remove_nulls(content):
    if type(content) == list:
        return [remove_nulls(x) for x in content]

    val = {}
    if type(content) == dict:
        for k,v in list(content.items()):
            if type(v) in (dict, list):
                val[k] = remove_nulls(v)
            elif v is not None:
                val[k] = v
    return val

def check_filter(content, param, value):
    if type(content) == list:
        return any([check_filter(x, param, value) for x in content])

    for key in param[:-1]:
        if key in content:
            content = content[key]
        else:
            return False

    return param[-1] in content and content[param[-1]] == value

def print_json_file(input_file, row_filter):
    if row_filter != None:
        param, value = row_filter.split(':')
        param = param.split('.')
        run_filter = lambda content: check_filter(content, param, value)
    else:
        run_filter = lambda content: True

    with open(input_file, "r") as f:
        for line in f:
            content = json.loads(line)
            if run_filter(content):
                content = remove_nulls(content)
                print(json.dumps(content, indent = 4))
                print(" ------------\n")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Copies and Joins S3 data files to Bytegain S3 storage')
    parser.add_argument('--input', type=str, help='Input file', required = True)
    parser.add_argument('--filter', type=str, help = "PARAM:VALUE filter for printing JSON rows", default = None)
    args = parser.parse_args()

    print_json_file(args.input, args.filter)
