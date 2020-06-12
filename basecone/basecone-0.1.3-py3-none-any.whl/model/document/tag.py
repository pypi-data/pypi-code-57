class Tag():
    def __init__(self, code, code_value, custom_tags):
        self.code = code
        self.code_value = code_value
        self.custom_tags = custom_tags

    @classmethod
    def from_dict(cls, data):
        return cls(
            code = data['code'],
            code_value = data['codeValue'],
            custom_tags = data.get('customTags', []),
        )