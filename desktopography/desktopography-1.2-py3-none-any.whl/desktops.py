import subprocess

from . import db
from . import selector

DESKTOPS = {
    'cinnamon': 'org.cinnamon.desktop.background',
    'gnome': 'org.gnome.desktop.background',
}


def set_wallpaper(desktop, size):
    wallpaper_url = selector.select_random_wallpaper(size)
    wallpaper_path = db.store(wallpaper_url)
    subprocess.call([
        'gsettings',
        'set',
        DESKTOPS[desktop],
        'picture-uri',
        'file://{}'.format(wallpaper_path),
    ])
    return wallpaper_path
