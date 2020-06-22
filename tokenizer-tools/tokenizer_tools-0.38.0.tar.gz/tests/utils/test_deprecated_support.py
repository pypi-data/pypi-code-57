from tokenizer_tools.utils.deprecated_support import deprecated_support

def test_deprecated_support():
    @deprecated_support()
    def print_hello():
        print("hello")

    print_hello()
