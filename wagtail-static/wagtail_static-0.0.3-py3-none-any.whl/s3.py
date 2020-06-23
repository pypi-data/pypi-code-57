from pathlib import Path

import boto3
from django.conf import settings

from .local_files import get_local_filepath

static_base = getattr(settings, 'STATIC_PAGE_FILEPATH', './static-pages/')


def upload_site_tree(site):
    client = boto3.client('s3')
    static_dir = Path(static_base, site.site_name)
    for file in static_dir.glob('**/index.html'):
        bucket_path = file.relative_to(static_dir)
        client.upload_file(
            str(file.absolute()),
            'nj-static-test',
            str(bucket_path),
            ExtraArgs={'ContentType': 'text/html'}
        )


def upload_page(page):
    client = boto3.client('s3')
    site = page.get_site()
    static_dir = Path(static_base, site.site_name)
    page_path = get_local_filepath(page)
    bucket_path = page_path.relative_to(static_dir)
    client.upload_file(
        str(page_path.absolute()),
        'nj-static-test',
        str(bucket_path),
        ExtraArgs={'ContentType': 'text/html'}
    )
