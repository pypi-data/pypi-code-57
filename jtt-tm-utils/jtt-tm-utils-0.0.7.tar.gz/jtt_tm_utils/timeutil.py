from datetime import datetime
def linux_timestamp():
    return int(datetime.now().timestamp())

def timestamp_ms():
    return datetime.now().timestamp()*1000