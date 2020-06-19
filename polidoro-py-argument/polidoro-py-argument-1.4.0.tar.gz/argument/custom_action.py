from argparse import Action


class CustomAction(Action):
    def __init__(self, *args, method=None, **kwargs):
        self.method = method
        super(CustomAction, self).__init__(*args, **kwargs)

    def __call__(self, argument_parser, namespace, argument_values, option_string):
        resp = self.method(*argument_values)
        if resp is not None:
            print(resp)
        exit(0)
