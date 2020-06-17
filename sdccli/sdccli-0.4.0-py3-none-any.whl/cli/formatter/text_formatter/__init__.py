from sdccli.cli.formatter.text_formatter import alert, dashboard, panel
from sdccli.cli.formatter.text_formatter.scanning import alert as scanning_alert
from sdccli.cli.formatter.text_formatter.scanning import image


class NormalFormatter:
    def __init__(self):
        self.formats = {}
        self.formats.update(alert.formats())
        self.formats.update(dashboard.formats())
        self.formats.update(scanning_alert.formats())
        self.formats.update(image.formats())
        self.formats.update(panel.formats())

    def format(self, response, format_type):
        if format_type in self.formats:
            self.formats[format_type](response)
        else:
            print(response)
