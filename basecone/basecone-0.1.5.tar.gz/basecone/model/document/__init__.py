import os
import json
from .company import Company
from .tag import Tag

class Document():
    def __init__(self, id, status, name, company, created_on, modified_on, transaction_proposal_id, transaction_id, source, source_metadata, tag):
        self.id = id
        self.status = status
        self.name = name
        self.company = company
        self.created_on = created_on
        self.modified_on = modified_on
        self.transaction_proposal_id = transaction_proposal_id
        self.transaction_id = transaction_id
        self.source = source
        self.tag = tag
        self.artifacts = None
        self.transaction = None

    @classmethod
    def from_dict(cls, data):
        return cls(
            id = data['documentId'],
            status = data['status'],
            name = data['name'],
            company = Company.from_dict(data['company']),
            created_on = data['createdOn'],
            modified_on = data.get('modifiedOn'),
            transaction_proposal_id = data.get('transactionProposalId'),
            transaction_id = data.get('transactionId'),
            source = data['source'],
            source_metadata = data.get('sourceMetadata'),
            tag = Tag.from_dict(data['tag'])
        )


    def to_json(self):
        return dict()
        
# {
#   "modifiedOn": "2020-03-05T12:38:05.29",
#   "name": "21818384",
#   "lookupIdentifier": null,
#   "lock": null,
#   "createdOn": "2020-03-05T12:37:57.807",
#   "sourceMetadata": null,
#   "source": "MailImporter",
#   "tag": {
#     "customTags": null,
#     "code": "PNV",
#     "codeValue": "INK"
#   },
#   "transactionProposalId": "1076b130-3cf1-48dc-ba67-d173cd650199",
#   "user": {
#     "userName": null,
#     "_links": [
#       {
#         "href": "https://api.basecone.com/v1/users/66811c79-15f8-4a31-8c37-33f0c273f866",
#         "rel": "self"
#       }
#     ],
#     "userId": "66811c79-15f8-4a31-8c37-33f0c273f866",
#     "name": null
#   },
#   "_links": [
#     {
#       "href": "https://api.basecone.com/v1/documents/cedde416-1151-465e-828d-27d1de834e81",
#       "rel": "self"
#     }
#   ],
#   "transactionId": null,
#   "type": "Unstructured",
#   "company": {
#     "companyCode": "130977",
#     "_links": [
#       {
#         "href": "https://api.basecone.com/v1/companies/6a2c4a9b-46c9-420d-b936-e6434bb30f08",
#         "rel": "self"
#       }
#     ],
#     "companyId": "6a2c4a9b-46c9-420d-b936-e6434bb30f08"
#   },
#   "documentId": "cedde416-1151-465e-828d-27d1de834e81"
# }