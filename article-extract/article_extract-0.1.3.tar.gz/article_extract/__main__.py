# -*- coding: utf-8 -*-
import sys
import json
import argparse
from .article_extract import extractor


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '-url', required=True, type=str, help='文章的url')
    parser.add_argument('-html', required=False, help='文章内容的html')
    args = parser.parse_args()
    article_data = extractor(url=args.u, is_content_html=args.html)
    print(json.dumps(article_data, ensure_ascii=False, indent=4))
    sys.exit()


if __name__ == '__main__':
    sys.exit(main())
