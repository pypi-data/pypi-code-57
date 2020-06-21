import urllib3


class Bitcoin(object):
    def latest_block_hash():
        http = urllib3.PoolManager()
        url = "https://blockstream.info/api/blocks/tip/hash"
        response = http.request('GET', url)
        response.status
        return response.data.decode('utf-8')
