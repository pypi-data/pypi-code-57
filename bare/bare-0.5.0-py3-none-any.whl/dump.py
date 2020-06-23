import argparse
import tempfile
import importlib.machinery
import base64

from bare.__main__ import codegen


def main():
    parser = argparse.ArgumentParser(description="BARE message debugger")
    parser.add_argument('schema', type=open)
    parser.add_argument('type')
    parser.add_argument('--base64', '-b', action='store_true')
    parser.add_argument('message')
    args = parser.parse_args()

    if args.base64:
        message = base64.b64decode(args.message)
    else:
        with open(args.message, 'rb') as handle:
            message = handle.read()

    with tempfile.NamedTemporaryFile(suffix='.py', mode='w') as output:
        codegen(args.schema.read(), output, '    ')
        output.flush()
        schema = importlib.machinery.SourceFileLoader('schema', output.name).load_module()

        type = getattr(schema, args.type)
        result = type.unpack(message)

    print(result.__class__.__name__)
    print(vars(result))


if __name__ == '__main__':
    main()
