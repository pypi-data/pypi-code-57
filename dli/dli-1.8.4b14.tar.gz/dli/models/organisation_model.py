from dli.models import AttributesDict

class OrganisationModel(AttributesDict):
    @classmethod
    def _from_v2_response(cls, data):
        data = data.pop('data')
        attributes = data["attributes"]
        return cls(id=data["id"], **attributes)
