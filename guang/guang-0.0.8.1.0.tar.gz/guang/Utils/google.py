import gdown
import fire
import numpy as np
import string


def rand_str(length=7):
    """Generate random string
    """
    totol_len = 62
    assert length < totol_len
    idx = np.random.permutation(totol_len)
    S = np.array([i for i in string.printable[:totol_len]])
    out = ''.join(S[idx[:length]].tolist())
    return out


def download(url, output=None, quiet=False, proxy=None, speed=None):
    if "https://drive.google.com/" in url:
        url_prefix = 'https://drive.google.com/uc?id='
        url_id = url[url.find('id=') + 3:]
        url = url_prefix + url_id
    gdown.download(url=url,
                   output=output,
                   quiet=quiet,
                   proxy=proxy,
                   speed=speed)


download.__doc__ = gdown.download.__doc__

if __name__ == "__main__":
    # url = "https://drive.google.com/open?id=1ZnDYF9rHKbef27tiHkWrLznqe18le7ol"
    # download(url, "xxx.zip", speed=100000) # speed: kb/s
    fire.Fire(download)
