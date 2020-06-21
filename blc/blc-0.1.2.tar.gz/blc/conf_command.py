from cleo import Command
import configparser


class ConfCommand(Command):
    """
    Config the CLI to ready to use
    blc:config
    """

    def handle(self):
        self.line('<info>Welcome to bcl setup</info>')
        base_url = self.ask('What is the remote of backups', None)
        api_key = self.ask('What is the api key for tha remote', None)
        config = configparser.ConfigParser()
        config['default'] = {'base_url': base_url, 'api_key': api_key}
        with open('config.ini', 'w') as configfile:
            config.write(configfile)
        self.line('<info>Configuration finished use --help to get started</info>')
