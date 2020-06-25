import argparse
import collections
import fiddler
import json

# py.test :

# Details of a request sent by Fiddler client
RequestInfo = collections.namedtuple(
    'RequestInfo', ['url', 'token', 'data', 'json_encoder']
)


class InMemorySender:
    def __init__(self):
        self.incoming = []

    def send(self, api_endpoint, token, data, json_encoder=None):
        self.incoming.append(RequestInfo(api_endpoint, token, data, json_encoder))


def test_publish_event():
    test_req = RequestInfo(
        url='https://api.fiddler.ai/external_event/' 'test_org/test_project/test_model',
        token='test_token',
        data={'test_key_1': 'test_value_1'},
        json_encoder=None,
    )

    fdl = fiddler.Fiddler('test_token', 'test_org', 'test_project', 'test_model')

    sender = InMemorySender()
    fdl._sender = sender

    fdl.publish_event(test_req.data)

    assert sender.incoming[-1] == test_req


class CustomEncoder(json.JSONEncoder):
    pass


# Manual testing with real service


def manual_test(args):
    """Manual test of publish_event() with actual server"""
    fdl = fiddler.Fiddler(args.token, args.org, args.project, args.model)
    fdl.publish_event(json.loads(args.data))


if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser(description='Utility for manual tests')

    arg_parser.add_argument('--org')
    arg_parser.add_argument('--project')
    arg_parser.add_argument('--model')
    arg_parser.add_argument('--token')
    arg_parser.add_argument('--data')

    manual_test(arg_parser.parse_args())
