import click
import requests
import webbrowser


@click.command()
@click.pass_context
def test(ctx):
    # r = requests.get('https://idpdecathlon.oxylane.com/as/authorization.oauth2?response_type=code&client_id=apimanagement&redirect_uri=https://api-portal.decathlon.net&scope=openid%20profile', auth=('user', 'pass'))
        # response = requests.get('https://idpdecathlon.oxylane.com/as/authorization.oauth2?response_type=code&client_id=apimanagement&redirect_uri=https://api-portal.decathlon.net&scope=openid%20profile', allow_redirects=True)
        # print(response)

    webbrowser.open('www.google.com')