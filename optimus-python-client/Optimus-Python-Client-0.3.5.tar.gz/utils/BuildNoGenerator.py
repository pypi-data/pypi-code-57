import uuid


class BuildNoGenerator(object):

    @classmethod
    def getBuildNo(cls):
        return uuid.uuid4()
