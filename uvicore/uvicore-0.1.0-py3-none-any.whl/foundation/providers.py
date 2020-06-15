from uvicore.support.provider import ServiceProvider


class Foundation(ServiceProvider):

    def register(self):

        # Register configs
        self.configs([
            ('foundation', 'uvicore.foundation.config.foundation.config')
        ])

        # # Register root level commands
        # self.commands(
        #     name='root',
        #     #help='xx',
        #     commands=[
        #         ('version', 'uvicore.foundation.commands.version.cli'),
        #     ]
        # )

        # Register HTTP Serve commands
        # force = False
        # if "'http', 'serve'" in str(sys.argv):
        #     force = True
        self.commands(
            name='http',
            help='Uvicore HTTP Commands',
            commands=[
                ('serve', 'uvicore.foundation.commands.serve.cli'),
            ],
            force=True  # Runs even if is_console = False
        )


    def boot(self):
        pass
