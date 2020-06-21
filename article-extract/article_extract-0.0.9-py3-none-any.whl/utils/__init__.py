# -*- encoding=utf-8 -*-
import re

DIRTY_CHARS = re.compile(r'[Ҫ瀹╄ㄥɾڸŲӰеԪΪЩй˾ǹӦȾڷҽա⣿Ŀѣ╀ц¤ㄣ�]', flags=(re.I|re.S))


def guess_encoding(content, encoding):
    try:
        html = content.decode(encoding, errors='ignore')
        no_ascii_content_str = re.sub(re.compile(r'[\sa-zA-Z0-9`i\~\!@#\$\%\^\&\*\(\)_\+\-=\[\]\{\}\|\?/<>,\.;\':"]', flags=(re.I|re.S)), '', html)
        chi_chars = re.findall(re.compile(r'[的一是了我不人在他有这个上们来到时大地为子中你说生国年着就那和要她出也得里后自以会家可下而过天去能对小多然于心学么之都好看起发当没成只如事把还用第样道想作种开网]', flags=(re.I|re.S)), no_ascii_content_str)
        str_chars = re.findall(DIRTY_CHARS, no_ascii_content_str)
        if (len(chi_chars) / len(no_ascii_content_str) >= 0.1 or
                len(chi_chars) >= 3) and (len(set(str_chars))<=2):
            return html
    except Exception:
        pass
    return None


def bytes_to_html(content):
    if not isinstance(content, bytes):
        raise Exception("content type should be bytes.")
    match = re.search(rb'charset="?([A-Za-z0-9-]*)"?', content)
    encoding = 'utf-8'
    html = ''
    if match:
        encoding = match.group(1).decode('ascii')
        html = guess_encoding(content, encoding)
    if not html:
        encoding = 'utf-8'
        html = guess_encoding(content, encoding)
    if not html:
        encoding = 'gbk'
        html = guess_encoding(content, encoding)
    if not html:
        encoding = 'gb2312'
        html = guess_encoding(content, encoding)
    if not html:
        encoding = 'utf16'
        html = guess_encoding(content, encoding)
    if not html:
        encoding = 'unicode'
        html = guess_encoding(content, encoding)
    if html is not None:
        return (encoding, html)
    else:
        raise Exception()