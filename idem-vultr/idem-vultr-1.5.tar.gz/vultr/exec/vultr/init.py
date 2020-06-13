import httpx


def __init__(hub):
    hub.exec.vultr.ACCT = ["vultr"]
    hub.exec.vultr.HTTPX = httpx.AsyncClient()
