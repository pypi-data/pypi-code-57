class Object(object):
    def __str__(self):
        return self.__class__.__name__ + self.__dict__.__str__()
