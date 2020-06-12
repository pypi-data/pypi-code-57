import os
from threading import Thread
from pathlib import Path
import click
from click import ClickException
import math
import requests
import json
import yaml
from mimetypes import guess_extension
from .model import Artifact, Document, Transaction, Company

from .utils import timeit

BASE_URL = 'https://api.basecone.com/v1'

class MaxReachedException(Exception):
    pass

class Client:
    def __init__(self, debug=False, limit=50):
        self.debug = debug
        self.limit = limit

        self._init()

    def _init(self):
        """
        Load config from ~/.basecone/config.yml
        (fail is not available)
        """
        config = os.path.join(Path.home(), ".basecone/config.yml")

        if not os.path.isfile(config):
            raise ClickException(f'Unable to load {config}.\nMake sure you properly configure the Basecone cli.')

        with open(config, 'r') as f:
            try:
                self.config = yaml.safe_load(f)

            except yaml.parser.ParserError:
                raise ClickException(f'[ERROR] {config} could not be parsed.')

    def __getattr__(self, key):
        try:
            return self.config[key]
        except KeyError:
            return None

    def me(self):
        me = self.do_get('users/currentUser').json()

        companies = list()
        offset  = 0
        q = f"users/{me['id']}/companies"

        while True:
            result = self.do_get(f'{q}?offset={offset}&limit={self.limit}').json()
            count = len(result.get('companies',[]))

            for c in result.get('companies',[]):
                companies.append(Company.from_dict(c))

            # offset += self.limit + 1
            offset += self.limit

            if (count < self.limit):
                break

        me.update({'companies': companies})

        return me

    def __check(self, method, url, response):
        r = response.json()

        if r.get('Code', '') == 'unauthorized':
            raise click.UsageError(f"Not authorized to access {method.upper()} {url}")

    def do_get(self, uri, is_json=True):
        try:
            url = '{0}/{1}'.format(BASE_URL, uri)
            auth = requests.auth.HTTPBasicAuth(self.config['client_id'], self.config['api_access_key'])

            response = requests.get(url, auth=auth)
            response.raise_for_status()

            if is_json:
                self.__check('get', url, response)
            
            return response

        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 403:
                raise click.UsageError(f"Not authorized to access {url}")
            else:
                raise click.ClickException(str(e))

    def do_post(self, uri, data):
        try:
            url = '{0}/{1}'.format(BASE_URL, uri)

            response = requests.post(url, json=data)
            response.raise_for_status

            if self.debug:
                click.echo(json.dumps(response.text))

            self.__check('post', url, response)

            return response

        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 403:
                if self.debug: click.echo(f'>>> do_post({uri}): {json.dumps(data, indent=2)}')

                raise click.UsageError(f"Not authorized to access {url}")
            else:
                raise click.ClickException(str(e))

    def token(self, username, password):
        """
        Create api access key for specific user
        https://developers.basecone.com/ApiReference/ApiUserAccessKeys

        @params:
        {
            "username": "Quasimodo",
            "password": "VerySecretPassword",
            "officeCode": "YourBaseconeOfficeCode",
            "clientIdentifier": "81638f6b-2e84-4abb-ab61-634afb455d15",
            "clientSecret": "iaq2DGp243kYA2PcmuQYTqcQ26cBOFQ+t8U92S8JX1zZASnzwOmu680pFwVs/NPE2zoQDWzM0QSNdYRc"
        }

        @returns
        {
            "apiAccessKey":"76e8a07e-db7c-47c1-bc65-f39ef600b9ad",
            "userId":"34e8a07e-db7c-78c1-bc65-f39ef611b9aE"
        }
        """
        if 'client_secret' not in self.config:
            self.config['client_secret'] = click.prompt('Basecone client secret not found. Please enter (you got that from Basecone)')

        params = dict(
            username = username,
            password = password,
            officeCode = self.config['office_code'],
            clientIdentifier = self.config['client_id'],
            clientSecret = self.config['client_secret']
        )
        return self.do_post('Authentication/ApiAccessKeys', params).json()

    def artifacts(self, document_id, filter=None):
        """
        https://developers.basecone.com/ApiReference/ArtifactsCollection
        """
        result = self.do_get('documents/{0}/artifacts'.format(document_id))
        ret = list()
        for artifact in result.json()['artifacts']:
            ret.append(Artifact.from_dict(document_id=document_id, data=artifact))

        return ret

    def download_transactions(self, c, f=None, m=None):
        """
        Download transactions for company (multithreaded).

        @param: c Company
        @param: f Filter
        @param: m Max number of results.
        """
        basedir = os.path.join(os.path.dirname(os.path.realpath(__file__)), '../', self.download_to, c.name)

        if not os.path.isdir(basedir):
            os.makedirs(basedir)

        # extra call to get number of 'transactions' (includes filter)
        num_transactions = self.count(company_id=c.id, entity='transactions', filter=f)

        if self.debug:
            click.echo(f'>>> found {num_transactions} transaction(s).')

        # reset counters per company
        offset  = 0
        count   = 0
        total   = min(num_transactions, m) if m else num_transactions
        limit   = min(self.limit, m) if m else self.limit

        # TODO: prevent overwrite 'transactions.csv' by adding suffix (~ use filter ??)
        database_file = f'{basedir}/transactions.csv'

        # reset file per company
        with open(database_file, 'w', encoding="utf-8") as fh:
            fh.write('transaction_number;document_id;date;type;currency;total_amount;description' + os.linesep)        

        with click.progressbar(length=total, label=f"Downloading {total} transactions for company '{c.name}'") as _progress:
            threads = []
            while True:
                transactions = self.transactions(c.id, offset, self.limit, f)

                thread = Thread(target=self.handle_transactions, args=(basedir, transactions))
                thread.start()
                threads.append(thread)

                with open(database_file, 'a', encoding="utf-8") as fh:
                    for t in transactions:
                        date = t.transaction_date.split('T')[0]
                        line = f"{t.transaction_number};{t.document_id};{date};{t.type};{t.currency};{t.total_amount};{t.description}"

                        fh.write(line + os.linesep)

                _progress.update(len(transactions))

                count += len(transactions)

                if (count >= total or len(transactions) < self.limit):
                    # fetched all available transactions ... break + continue with next company
                    # FIXME: (or bug) number of transactions do _not_ match actual num transactions.
                    break

                offset += self.limit + 1

            # make sure all threads are finished before continue with next Company
            for thread in threads:
                thread.join()

            # cosmetic: show 100% progress ... aka done
            _progress.update(num_transactions)

    def handle_transactions(self, basedir, transactions):
        """
        Handle batch transactions in separate thread.
        """
        for transaction in transactions:

            artifacts = self.artifacts(transaction.document_id)

            # assuming that all documents only have one (~ 1) artifact !!
            if self.debug and len(artifacts) > 1:
                click.echo(f'>> transaction {transaction.id} has {len(artifacts)} artifacts (expected only 1)')

            # create directory based on transaction_date date (if needed)
            directory = f"{basedir}/{transaction.transaction_date.split('T')[0]}"

            if not os.path.isdir(directory):
                try:
                    os.mkdir(directory)
                except FileExistsError:
                    pass

            # write transaction metadata
            jsonfile = f'{directory}/{transaction.id}.json'

            with open(jsonfile, 'wt', encoding="utf-8") as fh:
                fh.write(json.dumps(transaction.to_json(), indent=2) + os.linesep)

            for artifact in artifacts:

                # guessing extension using first item in 'Content-Type'
                target = f'{transaction.id}{guess_extension(artifact.content_type[0])}'

                if os.path.exists(f"{directory}/{target}"):
                    continue

                # TODO: do multithreaded
                body = self.download_artifact(artifact)

                with open(f"{directory}/{target}", 'wb') as fh:
                    fh.write(body)

    def download_documents(self, c, f=None, m=None):
        """
        Download documents for company (multithreaded).

        @param: c Company
        @param: f Filter
        @param: m Max number of results.
        """
        # extra call to get number of 'documents'
        num_docs = self.count(company_id=c.id, entity='documents', filter=f)

        if self.debug:
            click.echo(f'>>> found {num_docs} document(s).')

        # reset counters per company
        offset  = 0
        count   = 0
        total   = min(num_docs, m) if m else num_docs
        limit   = min(self.limit, m) if m else self.limit

        basedir = os.path.join(os.path.dirname(os.path.realpath(__file__)), '../', self.download_to, c.name)

        if not os.path.isdir(basedir):
            os.makedirs(basedir)

        with click.progressbar(length=total, label=f"Downloading {total} documents for company '{c.name}'") as _progress:

            try:
                while True:
                    # FIXME: show click.progressbar() immediately instead of after first batch.

                    docs = self.documents(company_id=c.id, offset=offset, limit=self.limit, filter=f) or []

                    # document == boekstuk
                    for doc in docs:
                        # each 'artifact' is 1 downloadable document
                        for artifact in doc.artifacts:
                            # create directory based on created_on date (if needed)
                            directory = f"{basedir}/{doc.created_on.split('T')[0]}"

                            if not os.path.isdir(directory):
                                try:
                                    os.mkdir(directory)
                                except FileExistsError:
                                    pass

                            # document metadata
                            tag = doc.tag.code_value if doc.tag else None
                            data = {
                                'name': doc.name,
                                'tag': tag,
                                'created_on': doc.created_on,
                                'modified_on': doc.modified_on
                            }

                            jsonfile = f'{directory}/{doc.id}.json'

                            with open(jsonfile, 'wt', encoding="utf-8") as fh:
                                fh.write(json.dumps(data, indent=2) + os.linesep)

                            body = self.download_artifact(artifact)

                            # guessing extension using first item in 'Content-Type'
                            target = f'{doc.id}{guess_extension(artifact.content_type[0])}'
                            with open(f"{directory}/{target}", 'wb') as fh:
                                fh.write(body)

                            count += len(doc.artifacts)

                            if (count >= total or len(docs) < limit):
                                raise MaxReachedException()

                    _progress.update(len(docs))

                    offset += self.limit + 1

            except MaxReachedException:
                pass

    def download_artifact(self, artifact):
        page_id = 1
        content_type = 'application/pdf'
        result = self.do_get(f'documents/{artifact.document_id}/artifacts/{artifact.id}?pageId={page_id}&contentType={content_type}', is_json=False)
        return result.content

    def count(self, company_id, entity="documents", filter=None):
        """
        Get total number of entities for company.
        """
        q = f'{entity}?companyId={company_id}'

        if filter:
            q += f'&{filter}'

        return int(self.do_get(f'{q}&offset=0&limit=1').json()['_metadata']['total'])

    def documents(self, company_id, offset=0, limit=50, filter=None):
        """
        https://developers.basecone.com/ApiReference/DocumentCollection
        """
        ret = list()

        q = f'documents?companyId={company_id}'

        if filter:
            q += f'&{filter}'

        result = self.do_get(f'{q}&offset={offset}&limit={limit}').json()

        documents = result.get('documents',[])

        if self.debug:
            if documents:
                d = documents[0]
                click.echo(json.dumps(d, indent=2))
                doc = Document.from_dict(d)
                click.echo(doc.tag.custom_tags)
            else:
                click.echo('>>> no documents found')

        for d in documents:
            try:
                document = Document.from_dict(d)

                document.artifacts = self.artifacts(document.id)

                ret.append(document)

            except Exception as e:
                print(f'Error: {str(e)}')
                print(json.dumps(d, indent=2))

        return ret

    def transactions(self, company_id, offset=0, limit=50, filter=None):
        """
        https://developers.basecone.com/ApiReference/TransactionCollection
        """
        ret = list()

        q = f'transactions?companyId={company_id}'

        if filter:
            q += f'&{filter}'

        result = self.do_get(f'{q}&offset={offset}&limit={limit}').json()
        transactions = result.get('transactions',[])

        if self.debug:
            if transactions:
                t = transactions[0]
                click.echo(json.dumps(t, indent=2))
            else:
                click.echo('>>> no transactions found')

        for t in transactions:
            try:
                transaction = Transaction.from_dict(t)
                
                # NOTE: This takes too long ... moved to cli (for now)
                # transaction.artifacts = self.artifacts(transaction.document_id)

                ret.append(transaction)
            except Exception as e:
                print(f"Error: {str(e)}")
                print(json.dumps(t, indent=2))

        return ret

    def create_webhook(self, company_id, endpoint, username=None, password=None):
        """
        https://developers.basecone.com/ApiReference/CreateWebhookSubscription
        """
        params = dict(
            companyId = company_id,
            endpoint = endpoint
        )

        if username and password:
            params['username'] = username
            params['password'] = password

        if self.debug:
            click.echo(f'>> Params: {json.dumps(params, indent=2)}')
            
        result = self.do_post(f'subscriptions', params).json()

        if self.debug:
            click.echo(json.dumps(result, indent=2))

        return result

    def webhooks(self):
        """
        https://developers.basecone.com/ApiReference/WebhookSubscriptionCollection
        """
        result = self.do_get('subscriptions')

        return result


    def get_transaction_proposal(self, transaction_id):
        result = self.do_get(f'transactionproposals/{transaction_id}').json()

        if self.debug:
            click.echo(json.dumps(result, indent=2))

        return result

    def get_api(self, entity):
        result = self.do_get(f'{entity}').json()

        if self.debug:
            click.echo(json.dumps(result, indent=2))

        return result
