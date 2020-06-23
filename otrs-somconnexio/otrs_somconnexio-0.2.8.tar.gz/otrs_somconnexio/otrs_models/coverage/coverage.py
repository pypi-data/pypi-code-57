class Coverage:
    @classmethod
    def get_selector_values(cls):
        """
        Return a list of tupples with the values as key and value of the tupple.
        """
        return [(val, val) for val in cls.VALUES]
