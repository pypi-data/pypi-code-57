from thmcli.util.api import get_api
from argh.decorators import arg


@arg('room', help='Room code')
def roominfo(room):
    api = get_api()

    r = api.room_details(room)

    print(f'Description for room "{r["title"]}"')
    print()
    print(r['description'])
