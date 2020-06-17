from django.core.management.base import BaseCommand
from wafer.talks.models import Talk
import json
import os
import re
import requests


class Command(BaseCommand):
    help = 'Load video URLs from sreview.debian.net'

    def handle(self, *args, **options):
        jsonurl = 'https://sreview.debian.net/released.json'
        jsondata = requests.get(jsonurl)
        data = json.loads(jsondata.content.decode('utf-8'))

        for entry in data['videos']:
            basename = os.path.basename(re.sub(r'/$', '', entry['eventid']))
            talk_id = int(basename.split('-')[0])
            talk = Talk.objects.get(pk=talk_id)
            talk.urls.get_or_create(
                description='Video',
                url=entry['details_url']
            )
            print('Loaded video for <%s>' % talk)
