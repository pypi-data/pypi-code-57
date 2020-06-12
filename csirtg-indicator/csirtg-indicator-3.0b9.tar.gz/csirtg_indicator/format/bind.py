import time
import os
from csirtg_indicator import Indicator

from io import StringIO

OUTPUT_PATH = os.getenv('CSIRTG_INDICATOR_BIND_PATH', '/etc/namedb')


def get_lines(data, filename=OUTPUT_PATH):
    output = StringIO()
    output.write("// generated by: {} at {}\n".
                 format('csirtg-indicator',
                        time.strftime('%Y-%m-%dT%H:%M:%S %Z')))

    for i in data:
        if isinstance(i, Indicator):
            i = i.__dict__()

        if i['itype'] != 'fqdn':
            continue

        output.write('zone "{}" {{type master; file "{}";}};'.
                     format(i['indicator'], filename))

        yield output.getvalue()

        if isinstance(output, StringIO):
            output.truncate(0)
            output.seek(0)
