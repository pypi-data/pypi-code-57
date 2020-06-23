from pathlib import Path

from django.conf import settings
from django.core.handlers.wsgi import WSGIRequest

static_base = getattr(settings, 'STATIC_PAGE_FILEPATH', './static-pages/')


def get_local_filepath(page):
    site = page.get_site()
    base_path = Path(static_base).joinpath(site.site_name)
    url_path = page.get_url_parts()[2]
    file_path = base_path.joinpath(url_path[1:])
    if not file_path.exists():
        file_path.mkdir(parents=True)
    return file_path.joinpath('index.html')


def create_static_file(page):
    dummy_meta = page._get_dummy_headers()
    dummy_request = WSGIRequest(dummy_meta)
    dummy_request.static_generation = True  # So we don't get served the last static build
    site = page.get_site()
    dummy_request.site = site

    # Pass through serve so we get middleware applied
    response = page.serve(dummy_request)
    response.render()
    page_content = response.content

    path = get_local_filepath(page)
    path.write_bytes(page_content)
    return path


def destroy_all_static_files():
    static_dir = Path(static_base)
    if static_dir.exists():
        for file in static_dir.glob('**/index.html'):
            file.unlink()


def clean_unused_dirs(path=static_base):
    directory = Path(path)
    for child in directory.iterdir():
        if child.is_dir():
            try:
                child.rmdir()
            except OSError:
                clean_unused_dirs(child.absolute())
