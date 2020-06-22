from tokenizer_tools.utils.deprecated_api import deprecated_api

def test_deprecated_api():

    @deprecated_api(deprecated_api)
    def print_hello():
        print("hello")

    print_hello()
