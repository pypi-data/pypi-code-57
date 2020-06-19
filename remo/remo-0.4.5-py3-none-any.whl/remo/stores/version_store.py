import os
import re
from django.conf import settings


class Version:
    rgx_digits = re.compile(r'\d+')

    @staticmethod
    def latest_electron_app(platform: str):
        files = os.listdir(settings.DOWNLOAD_URL)
        platforms = {
            'Linux': '',
            'Darwin': '-mac',
            'Windows': '-win'
        }
        plt = platforms.get(platform, '')
        rgx = re.compile(rf'remo-(\d.\d.\d){plt}.zip')
        files = filter(rgx.fullmatch, files)
        if not files:
            return None, None

        versions = list(map(lambda name: rgx.findall(name)[0], files))
        versions.sort(reverse=True, key=Version.to_num)
        latest = versions[0]
        file_name = 'remo-{}{}.zip'.format(latest, plt)
        return latest, file_name

    @staticmethod
    def to_num(ver):
        if not ver:
            return 0

        num = list(map(int, Version.rgx_digits.findall(ver)))
        num.extend([0, 0, 0, 0, 0])
        num = num[:5]
        return sum(map(lambda v: v[0] * v[1], zip(num, [1000, 100, 10, 1, 0.1])))
