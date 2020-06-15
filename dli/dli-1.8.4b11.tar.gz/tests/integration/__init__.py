from secrets import token_urlsafe


def random_name():
    return 'qa-test-cases-{}'.format(token_urlsafe(5))
