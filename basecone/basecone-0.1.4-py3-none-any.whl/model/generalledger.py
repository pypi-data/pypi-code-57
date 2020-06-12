class GeneralLedger {
    def __init__(self, code):
        self.code

    @classmethod
    def from_dict(cls, data):
        return cls(
            code = data['code']
        )
}