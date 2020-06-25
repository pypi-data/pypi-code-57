class NumberRandomCharsException(Exception):
    min_num_chars = 0
    max_num_chars = 32
    def __init__(self):
        super().__init__('The random characters are generated as a uuid4. Therefore, the selected number "num_random_chars" should be between {} to {} '.format(
                          NumberRandomCharsException.min_num_chars, NumberRandomCharsException.max_num_chars))
        
class NumberCharsBucketNameException(Exception):
    min_num_chars = 3
    max_num_chars = 63
    def __init__(self, bucket_name, num_chars):
        super().__init__('The number of characters in a bucket name should be between {} and {}. Your bucket name {} has {} chars only'.format(
            NumberCharsBucketNameException.min_num_chars, NumberCharsBucketNameException.max_num_chars,
            bucket_name, num_chars))