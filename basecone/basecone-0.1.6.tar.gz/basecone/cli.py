import os
import click
from click import BadOptionUsage
import json
import time
from datetime import datetime

from basecone import Client, Server, __version__

def filter(companies, f=[]):
    """
    Apply filter on company list
    """
    if not f:
        return companies

    filtered_company_ids = list(dict.fromkeys(f))

    # apply filter
    companies = [c for c in companies if c.id in filtered_company_ids]

    not_in = [c for c in filtered_company_ids if c not in [c.id for c in companies]]

    if not_in:
        click.echo(f"[WARNING] filter(s) not found: {', '.join(not_in)}")

    return companies

@click.group()
@click.version_option(version=__version__)
def main():
    """
    Basecone admin
    """
    pass

@main.command()
@click.option('-u', '--username', help="Your Basecone username", required=True)
@click.option('-p', '--password', help="Your Basecone password", prompt="Enter your Basecone password", hide_input=True)
@click.option('-debug', help='Show more verbose output', is_flag=True)
def token(username, password, debug):
    """
    Create new API access keys.
    """
    client = Client(debug)

    token = client.token(username, password)

    click.echo(json.dumps(token, indent=2))

@main.command()
@click.option('-max', help='Max number of documents', type=int)
@click.option('-from', 'from_date', help= "From transaction date", type=click.DateTime(formats=['%d-%m-%Y']))
@click.option('-to', 'to_date', help= "To transaction date", type=click.DateTime(formats=['%d-%m-%Y']), default=datetime.now().strftime('%d-%m-%Y'))
@click.option('-debug', help='Show more verbose output', is_flag=True)
@click.option('-timing', help='Show timing', is_flag=True)
def documents(max, from_date, to_date, debug, timing):
    """
    Download Basecone documents.
    """
    if timing:
        ts = time.time()

    client = Client(debug)

    me = client.me()

    companies = filter(me['companies'], client.filter)

    # set filters
    _filter = None
    # if from_date and to_date:
    #     _filter = 'createdOn=["{}","{}"]'.format(from_date.strftime('%Y-%m-%dT00:00:00.000'), to_date.strftime('%Y-%m-%dT00:00:00.000'))
    # elif from_date:
    #     # wont match anything because of timestamp
    #     _filter = 'createdOn={}'.format(from_date.strftime('%Y-%m-%dT00:00:00.000'))

    if _filter:
        click.echo(f'Filtering documents does not work ... yet :(')

    for company in companies:
        # TODO: downloading documents is still single-threaded
        client.download_documents(c=company, f=_filter, m=max)

    if timing:
        te = time.time()
        click.echo(f">>> Download took {round((te - ts) * 1000, 2)} ms to execute")

    click.echo(f'Done 🤖')

@main.command()
@click.option('-max', help='Max number of transactions (mainly used for dev purposes)', type=int)
@click.option('-from', 'from_date', help= "From transaction date", type=click.DateTime(formats=['%d-%m-%Y']))
@click.option('-to', 'to_date', help= "To transaction date", type=click.DateTime(formats=['%d-%m-%Y']))
@click.option('-year', help="Book year", type=click.DateTime(formats=['%Y']))
@click.option('-debug', help='Show more verbose output', is_flag=True)
@click.option('-timing', help='Show timing', is_flag=True)
def download(max, from_date, to_date, year, debug, timing):
    """
    Download Basecone transactions.
    """
    if timing:
        ts = time.time()

    if (from_date or to_date) and year:
        raise BadOptionUsage(option_name='year', message="Can't use year together with from/to")

    client = Client(debug)

    me = client.me()

    companies = filter(me.get('companies',[]), client.filter)

    # set filter
    _filter = None

    if from_date and to_date:
        _filter = 'transactionDate=["{}","{}"]'.format(from_date.strftime('%Y-%m-%d'), to_date.strftime('%Y-%m-%d'))
    elif from_date:
        _filter = 'transactionDate={}'.format(from_date.strftime('%Y-%m-%d'))
    elif year:
        _filter = 'bookYear={}'.format(year.strftime('%Y'))

    for company in companies:
        # do multithreaded download transactions per company
        client.download_transactions(c=company, f=_filter, m=max)

    if timing:
        te = time.time()
        click.echo(f">>> Download took {round((te - ts) * 1000, 2)} ms to execute")

    click.echo(f'Done 🤖')

@main.command()
@click.argument('action', type=click.Choice(['create', 'update', 'delete', 'list']))
@click.option('-company', help="Company Id for which you need a webhook", required=True)
@click.option('-endpoint', help="A valid url representing the endpoint Basecone needs to deliver events to.", required=True)
@click.option('-u', '--username', help="A username that Basecone will use for basic authentication when delivering the event.")
@click.option('-p', '--password', help="A password that Basecone will use for basic authentication when delivering the event.")
@click.option('-debug', help='Show more verbose output', is_flag=True)
def webhook(action, company, endpoint, username, password, debug):
    """
    Manage Basecone webhooks.
    """
    #
    # Error: Not authorized to access POST https://api.basecone.com/v1/subscriptions
    #

    #
    # https://developers.basecone.com/ApiReference/CreateWebhookSubscription
    # https://developers.basecone.com/ApiReference/Webhooks
    #
    # IDEA:
    # - create webhook to public endpoint (~ ngrok)
    # - create 'Basecone server' that handles webhook event
    #
    client = Client(debug)

    if action == 'create':

        response = client.create_webhook(company, endpoint, username, password)

        if debug:
            click.echo(json.dumps(response, indent=2))

    elif action == 'list':

        response = client.webhooks()

        if debug:
            click.echo(json.dumps(response, indent=2))

    else:
        click.echo(f'{action} not supported ... yet')


@main.command()
@click.argument('attr', type=click.Choice(['self', 'company']), required=True)
@click.option('-debug', help='Show more verbose output', is_flag=True)
def my(attr, debug):
    """
    Show info about your Basecone account.
    """
    client = Client(debug)

    me = client.me()

    if attr == 'company':
        companies = me.get('companies')
        if debug:
            click.echo(f'>>> found {len(companies)} companies')
        for c in companies:
            click.echo(json.dumps(c.to_json(), indent=2))
    elif attr == 'self':
        _me = dict(
            id = me.get('id'),
            name = me.get('name'),
            username = me.get('username'),
            email = me.get('email'),
            phoneNumber = me.get('phoneNumber'),
            roles = me.get('roles', []),
            office_code = me.get('officeCode'),
            language = me.get('language')
        )

        click.echo(json.dumps(_me, indent=2))

@main.command()
@click.option('-port', help="Server port", default=5000)
@click.option('-debug', help='Show more verbose output', is_flag=True)
def server(port, debug):
    """
    Start server to process Basecone webhooks.
    """
    server = Server(port, debug)
    server.run()


# @main.command()
# @click.argument('what', required=True)
# # @click.argument('transaction')
# @click.option('-debug', help='Show more verbose output', is_flag=True)
# def get(what, debug):
#     # GET transactionproposals/:id
#     client = Client(debug)

#     me = client.me()

#     # https://developers.basecone.com/ApiReference/GetTransactionProposals

#     # Error: Not authorized to access https://api.basecone.com/v1/transactionproposals/14277c53-4193-44d2-b0ad-0277bbf74874

#     if what == 'transaction':
#         client.get_transaction_proposal(transaction)
#     elif what == 'webhook':
#         client.get_api(what)
#     else:
#         # click.echo(f'Action {what} is not supported.')
#         client.get_api(what)
