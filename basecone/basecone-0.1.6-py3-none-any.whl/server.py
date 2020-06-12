import json
import click
from flask import Flask, request, make_response, jsonify
from flask.views import MethodView

class Server:

    def __init__(self, port, debug):
        self.port = port
        self.debug = debug
        self.app = Flask('basecone')

        self.app.add_url_rule('/webhook', view_func=BaseconeWebhookAPI.as_view("basecone_webhook_api"))

    def run(self):
        self.app.run(debug=self.debug, use_reloader=False, port=self.port)

class BaseconeWebhookAPI(MethodView):
    """
    Basecone webhook handler
    """
    def __init__(self):
        self.switcher = {
            "DocumentCreated": self.document_created,
            "TransactionCreated": self.transaction_created,
        }

    def get(self):
        """
        Handle GET request
        """
        return make_response(jsonify(dict()), 200)

    def post(self):
        """
        Handle POST request
        """
        data = request.get_json(silent=True)

        # 
        f = self.switcher.get(data.get('webhookEventType',''), self.default)

        return f(request)

    def document_created(self, request):
        """
        Document created event

        A document created event is raised when a document is created, this can happen due to an import, or when existing documents or split or merged.

        https://developers.basecone.com/ApiReference/DocumentCreated

        {
            "documentId": "095eaf00-7788-4503-b644-4e613ee963a4",
            "id": "c8a07d44-bcaa-4fc3-bcce-7be9c91530cb",
            "companyId": "fb8f9584-3fc6-4cc7-abda-530ff397ea82",
            "created": "2014-09-30T13:51:35.4928649Z",
            "webhookEventType": "DocumentCreated",
            "customFields": {}
        }
        """
        click.echo('>> DocumentCreated')
        return make_response(jsonify(request.get_json(silent=True)), 200)

    def transaction_created(self, request):
        """
        Transaction created event

        A transaction created event will be raised when a user either processes or books a transaction proposal.

        https://developers.basecone.com/ApiReference/TransactionCreated

        {
            "transactionId": "521f2038-fe89-45fe-86f4-84553071a425",
            "documentId": "521f2038-fe89-45fe-86f4-84553071a425",
            "id": "1c2eb8b5-7dc9-430d-8b03-85e0036f80b0",
            "companyId": "fb8f9584-3fc6-4cc7-abda-530ff397ea82",
            "created": "2014-10-09T12:25:50.3140682Z",
            "webhookEventType": "TransactionCreated",
            "customFields": {}
        }
        """
        click.echo('>> TransactionCreated')
        return make_response(jsonify(request.get_json(silent=True)), 200)

    def default(self, request):
        """
        Default method called for webhook event.
        """
        return make_response(jsonify(request.get_json(silent=True)), 200)