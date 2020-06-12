class Artifact():

    def __init__(self, id, document_id, page_count, content_type, type):
        self.id = id
        self.document_id = document_id
        self.page_count = page_count
        self.content_type = content_type
        self.type = type

    @classmethod
    def from_dict(cls, document_id, data):
        return cls(
            id = data['artifactId'],
            document_id = document_id,
            page_count = data['pageCount'],
            content_type = data['contentType'],
            type = data['type']
        )

# {
#   "type": "Original",
#   "contentType": [
#     "application/pdf",
#     "image/jpeg"
#   ],
#   "artifactId": "9fcce1ac-e611-44a6-80a0-474926c889fb",
#   "pageCount": 2
# }