import json
import random
from io import BytesIO
import requests
from django.core.files.images import ImageFile
from django.utils import lorem_ipsum
from wagtail.documents.models import Document
from wagtail.core.models import PageViewRestriction

from ...cms import constants
from ...cms.snippets import Menu, MenuItem
from .mock_text import MockText


def title():
    return lorem_ipsum.words(random.randint(5, 15))


def text():
    return lorem_ipsum.words(random.randint(100, 200))


class Mock(MockText):
    SVG_CUBE = {
        'url': "https://stationspatiale.com/static/assets/img/svg/icons/phone/space.svg",
        'title': "cube",
        'name': "cube.svg"
    }
    IMG_BLOG = {
        'url': "https://blog.stationspatiale.com/wp-content/uploads/2020/01/Fichier-2-100-900x600.jpg",
        'title': "blog",
        'name': "blog.jpg"
    }
    five = lorem_ipsum.words(5)
    hun = lorem_ipsum.words(100)
    animation = {
        'effect': 'fade-right',
        'duration': '1500'
    }
    default_url = "http://localhost:8080"

    @staticmethod
    def file(img, model=Document):
        try:
            ret = model.objects.get(title=img['title'])
            return ret
        except model.DoesNotExist:
            response = requests.get(img['url'])
            file = ImageFile(BytesIO(response.content), name=img['name'])
            ret = model(
                title=img['title'],
                file=file
            )
            ret.save()
            return ret

    @staticmethod
    def button(m_type=constants.BUTTON_GREEN_FULL):
        return {
            'text': 'Click here',
            'type': m_type
        }

    @staticmethod
    def base(bg=False, theme=constants.THEME_SPACE, container='regular', padding=True):
        return {
            'svg_bg': {
                'desktop': {
                    'file': Mock.file(Mock.SVG_CUBE).id if bg else None,
                },
                'mobile': {
                    'file': Mock.file(Mock.SVG_CUBE).id if bg else None,
                },
            },
            'theme': theme,
            'container': container,
            'padding': padding
        }

    @staticmethod
    def menu(page, menu_id=None):
        if not menu_id:
            menu = Menu.objects.create(
                help_text=page.title,
                title=page.title
            )
            menu.save()
            menu_id = menu.id
        menu_item = MenuItem.objects.create(
            menu_id=menu_id,
            link_title=page.title,
            link_page_id=page.id
        )
        menu_item.save()
        return menu_id

    @staticmethod
    def add_menu(page, menu_id, footer=True):

        # Header

        header_menus = []
        for header_menu in page.header_menus:
            header_menus.append({
                'type': 'menu',
                'value': header_menu.value.id
            })
        header_menus.append({
            'type': 'menu',
            'value': menu_id
        })
        page.header_menus = json.dumps(header_menus)

        # Footer

        if footer:
            footer_menus = []
            for footer_menu in page.footer:
                footer_menus.append({
                    'type': 'menu',
                    'value': footer_menu.value.id
                })
            footer_menus.append({
                'type': 'menu',
                'value': menu_id
            })
            page.footer = json.dumps(footer_menus)
        page.save()

    @staticmethod
    def add_header_buttons(page):
        header_buttons = [{
            'type': 'button',
            'value': Mock.button(m_type=constants.BUTTON_GREEN_LIGHT)
        }, {
            'type': 'button',
            'value': Mock.button(m_type=constants.BUTTON_WHITE_LIGHT)
        }]
        page.header_buttons = json.dumps(header_buttons)
        page.save()

    @staticmethod
    def set_login_required(page):
        pvr = PageViewRestriction.objects.create(
            page_id=page.id,
            restriction_type='login'
        )
        pvr.save()
