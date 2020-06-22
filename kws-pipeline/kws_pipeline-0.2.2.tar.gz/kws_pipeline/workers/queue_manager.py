from urllib.parse import urljoin

import requests


class QueueManager:
    def __init__(self, queue_manager_url):
        self.queue_manager_url = queue_manager_url

    def set_status(self, uuid, **kwargs):
        url = urljoin(self.queue_manager_url, str(uuid))
        r = requests.put(url, data=kwargs)
        return r
