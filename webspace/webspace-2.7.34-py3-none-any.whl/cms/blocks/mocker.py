import json
import random
from io import BytesIO
import requests
from django.core.files.images import ImageFile
from django.utils import lorem_ipsum

from wagtail.images.models import Image

from webspace.cms.models import MyDocument
from webspace.loader import get_model
from webspace.cms import constants

Menu = get_model('cms', 'Menu')
MenuItem = get_model('cms', 'MenuItem')


def title():
    return lorem_ipsum.words(random.randint(5, 15))


def text(rand_min=100, rand_max=200):
    return lorem_ipsum.words(random.randint(rand_min, rand_max))


class Mocker(object):
    h = f"""
        {title()}
        """

    xs = f"""
            <h3>{title()}</h3>
            <p>{text(10, 10)}</p>
            """

    small = f"""
            <h2>{title()}</h2>
            <h3>{title()}</h3>
            <hr/>
            <p>{text(20, 20)}</p>
            """

    normal = f"""
        <h3>{title()}</h3>
        <hr/>
        <p>{text(50, 50)}</p>
        """

    big = f"""
        <h2>{title()}</h2>
        <h3>{title()}</h3>
        <h4>{title()}</h4>
        <hr/>
        <p>{title()}</p>
        <ol>
            <li>{title()}</li>
            <li>{title()}</li>
            <li>{title()}</li>
            <li>{title()}</li>
        </ol>
        <p>{title()}</p>
        <p><b>{title()}</b><i>{title()}</i></p>
        <p><i>{title()}</i></p>
        <ul>
            <li>{title()}</li>
            <li>{title()}</li>
            <li>{title()}</li>
            <li>{title()}</li>
        </ul>
        <p></p>
        <p></p>
        <p>{text()}</p>
        <p><a href="#">{title()}</a>. {text()}</p><p><br/></p>
        """

    example = f"""
        <h1>H1 -> Lorem ipsum dolor sit amet, consectetur adipiscing elit</h1>
        <h2>H2 -> Lorem ipsum dolor sit amet, consectetur adipiscing elit</h2>
        <h3>H3 -> Lorem ipsum dolor sit amet, consectetur adipiscing elit</h3>
        <h4>H4 -> Lorem ipsum dolor sit amet, consectetur adipiscing elit</h4>
        <h5>H5 -> Lorem ipsum dolor sit amet, consectetur adipiscing elit</h5>
        <h6>H6 -> Lorem ipsum dolor sit amet, consectetur adipiscing elit</h6>
        <hr/>
        <p>Paragraph -> {title()}</p>
        <p><b>Bold -> {title()}</b></p>
        <p><i>Italic -> {title()}</i></p>
        <p><strong>Strong -> {title()}</strong></p>
        """

    text_first_content = f"""
        <h2>Lorem ipsum dolor sit amet, consectetur adipiscing elit</h2>
        <hr/>
        <p>{title()}</p>
        """

    URL_TEST = "https://stationspatiale.com"
    URL_EMBED = "https://www.youtube.com/watch?time_continue=1&v=UoXQIR8ykEY&feature=emb_logo"

    #  Bg desktop
    IMG_FAVICON = {
        'url': "https://station-spatiale.s3.eu-west-3.amazonaws.com/cms/icon_space.png",
        'title': "IMG_FAVICON",
        'name': "IMG_FAVICON.svg",
        'model': Image
    }

    #  Bg desktop
    SVG_BG_DESKTOP_LIGHT = {
        'url': "https://station-spatiale.s3.eu-west-3.amazonaws.com/cms/bg-desktop_light.svg",
        'title': "SVG_BG_DESKTOP_LIGHT",
        'name': "SVG_BG_DESKTOP_LIGHT.svg",
        'model': MyDocument
    }
    IMG_BG_DESKTOP_LIGHT = {
        'url': "https://station-spatiale.s3.eu-west-3.amazonaws.com/cms/bg-desktop_light.png",
        'title': "IMG_BG_DESKTOP_LIGHT",
        'name': "IMG_BG_DESKTOP_LIGHT.png",
        'model': Image
    }
    SVG_BG_DESKTOP_SPACE = {
        'url': "https://station-spatiale.s3.eu-west-3.amazonaws.com/cms/bg-desktop_space.svg",
        'title': "SVG_BG_DESKTOP_SPACE",
        'name': "SVG_BG_DESKTOP_SPACE.svg",
        'model': MyDocument
    }
    IMG_BG_DESKTOP_SPACE = {
        'url': "https://station-spatiale.s3.eu-west-3.amazonaws.com/cms/bg-desktop_space.png",
        'title': "IMG_BG_DESKTOP_SPACE",
        'name': "IMG_BG_DESKTOP_SPACE.png",
        'model': Image
    }

    #  Bg mobile
    SVG_BG_MOBILE_LIGHT = {
        'url': "https://station-spatiale.s3.eu-west-3.amazonaws.com/cms/bg-mobile_light.svg",
        'title': "SVG_BG_MOBILE_LIGHT",
        'name': "SVG_BG_MOBILE_LIGHT.svg",
        'model': MyDocument
    }
    IMG_BG_MOBILE_LIGHT = {
        'url': "https://station-spatiale.s3.eu-west-3.amazonaws.com/cms/bg-mobile_light.png",
        'title': "IMG_BG_MOBILE_LIGHT",
        'name': "IMG_BG_MOBILE_LIGHT.png",
        'model': Image
    }
    SVG_BG_MOBILE_SPACE = {
        'url': "https://station-spatiale.s3.eu-west-3.amazonaws.com/cms/bg-mobile_space.svg",
        'title': "SVG_BG_MOBILE_SPACE",
        'name': "SVG_BG_MOBILE_SPACE.svg",
        'model': MyDocument
    }
    IMG_BG_MOBILE_SPACE = {
        'url': "https://station-spatiale.s3.eu-west-3.amazonaws.com/cms/bg-mobile_space.png",
        'title': "IMG_BG_MOBILE_SPACE",
        'name': "IMG_BG_MOBILE_SPACE.png",
        'model': Image
    }

    # Logo
    SVG_LOGO_LIGHT = {
        'url': "https://station-spatiale.s3.eu-west-3.amazonaws.com/cms/logo_light.svg",
        'title': "SVG_LOGO_LIGHT",
        'name': "SVG_LOGO_LIGHT.svg",
        'model': MyDocument
    }
    IMG_LOGO_LIGHT = {
        'url': "https://station-spatiale.s3.eu-west-3.amazonaws.com/cms/logo_light.png",
        'title': "IMG_LOGO_LIGHT",
        'name': "IMG_LOGO_LIGHT.png",
        'model': Image
    }
    SVG_LOGO_SPACE = {
        'url': "https://station-spatiale.s3.eu-west-3.amazonaws.com/cms/logo_space.svg",
        'title': "SVG_LOGO_SPACE",
        'name': "SVG_LOGO_SPACE.svg",
        'model': MyDocument

    }
    IMG_LOGO_SPACE = {
        'url': "https://station-spatiale.s3.eu-west-3.amazonaws.com/cms/logo_space.png",
        'title': "IMG_LOGO_SPACE",
        'name': "IMG_LOGO_SPACE.png",
        'model': Image
    }

    # Blog cover  

    SVG_BLOG_COVER_LIGHT = {
        'url': "https://station-spatiale.s3.eu-west-3.amazonaws.com/cms/blog-cover_light.svg",
        'title': "SVG_BLOG_COVER_LIGHT",
        'name': "SVG_BLOG_COVER_LIGHT.svg",
        'model': MyDocument
    }
    IMG_BLOG_COVER_LIGHT = {
        'url': "https://station-spatiale.s3.eu-west-3.amazonaws.com/cms/blog-cover_light.png",
        'title': "IMG_BLOG_COVER_LIGHT",
        'name': "IMG_BLOG_COVER_LIGHT.png",
        'model': Image
    }
    SVG_BLOG_COVER_SPACE = {
        'url': "https://station-spatiale.s3.eu-west-3.amazonaws.com/cms/blog-cover_space.svg",
        'title': "SVG_BLOG_COVER_SPACE",
        'name': "SVG_BLOG_COVER_SPACE.svg",
        'model': MyDocument
    }
    IMG_BLOG_COVER_SPACE = {
        'url': "https://station-spatiale.s3.eu-west-3.amazonaws.com/cms/blog-cover_space.png",
        'title': "IMG_BLOG_COVER_SPACE",
        'name': "IMG_BLOG_COVER_SPACE.png",
        'model': Image
    }

    # Square  

    SVG_SQUARE_LIGHT = {
        'url': "https://station-spatiale.s3.eu-west-3.amazonaws.com/cms/media-text_light.svg",
        'title': "SVG_SQUARE_LIGHT",
        'name': "SVG_SQUARE_LIGHT.svg",
        'model': MyDocument

    }
    IMG_SQUARE_LIGHT = {
        'url': "https://station-spatiale.s3.eu-west-3.amazonaws.com/cms/media-text_light.png",
        'title': "IMG_SQUARE_LIGHT",
        'name': "IMG_SQUARE_LIGHT.png",
        'model': Image
    }
    SVG_SQUARE_SPACE = {
        'url': "https://station-spatiale.s3.eu-west-3.amazonaws.com/cms/media-text_space.svg",
        'title': "SVG_SQUARE_SPACE",
        'name': "SVG_SQUARE_SPACE.svg",
        'model': MyDocument

    }
    IMG_SQUARE_SPACE = {
        'url': "https://station-spatiale.s3.eu-west-3.amazonaws.com/cms/media-text_space.png",
        'title': "IMG_SQUARE_SPACE",
        'name': "IMG_SQUARE_SPACE.svg",
        'model': Image
    }

    # Icon  

    SVG_ICON_LIGHT = {
        'url': "https://station-spatiale.s3.eu-west-3.amazonaws.com/cms/icon_light.svg",
        'title': "SVG_ICON_LIGHT",
        'name': "SVG_ICON_LIGHT.svg",
        'model': MyDocument

    }
    IMG_ICON_LIGHT = {
        'url': "https://station-spatiale.s3.eu-west-3.amazonaws.com/cms/icon_light.png",
        'title': "IMG_ICON_LIGHT",
        'name': "IMG_ICON_LIGHT.png",
        'model': Image
    }
    SVG_ICON_SPACE = {
        'url': "https://station-spatiale.s3.eu-west-3.amazonaws.com/cms/icon_space.svg",
        'title': "SVG_ICON_SPACE",
        'name': "SVG_ICON_SPACE.svg",
        'model': MyDocument

    }
    IMG_ICON_SPACE = {
        'url': "https://station-spatiale.s3.eu-west-3.amazonaws.com/cms/icon_space.png",
        'title': "IMG_ICON_SPACE",
        'name': "IMG_ICON_SPACE.png",
        'model': Image
    }

    # Content height

    SVG_CONTENT_HEIGHT_LIGHT = {
        'url': "https://station-spatiale.s3.eu-west-3.amazonaws.com/cms/content-height_light.svg",
        'title': "SVG_CONTENT_HEIGHT_LIGHT",
        'name': "SVG_CONTENT_HEIGHT_LIGHT.svg",
        'model': MyDocument

    }
    IMG_CONTENT_HEIGHT_LIGHT = {
        'url': "https://station-spatiale.s3.eu-west-3.amazonaws.com/cms/content-height_light.png",
        'title': "IMG_CONTENT_HEIGHT_LIGHT",
        'name': "IMG_CONTENT_HEIGHT_LIGHT.png",
        'model': Image
    }
    SVG_CONTENT_HEIGHT_SPACE = {
        'url': "https://station-spatiale.s3.eu-west-3.amazonaws.com/cms/content-height_space.svg",
        'title': "SVG_CONTENT_HEIGHT_SPACE",
        'name': "SVG_CONTENT_HEIGHT_SPACE.svg",
        'model': MyDocument

    }
    IMG_CONTENT_HEIGHT_SPACE = {
        'url': "https://station-spatiale.s3.eu-west-3.amazonaws.com/cms/content-height_space.png",
        'title': "IMG_CONTENT_HEIGHT_SPACE",
        'name': "IMG_CONTENT_HEIGHT_SPACE.png",
        'model': Image
    }

    # Content width

    SVG_CONTENT_WIDTH_LIGHT = {
        'url': "https://station-spatiale.s3.eu-west-3.amazonaws.com/cms/content-width_light.svg",
        'title': "SVG_CONTENT_WIDTH_LIGHT",
        'name': "SVG_CONTENT_WIDTH_LIGHT.svg",
        'model': MyDocument
    }
    IMG_CONTENT_WIDTH_LIGHT = {
        'url': "https://station-spatiale.s3.eu-west-3.amazonaws.com/cms/content-width_light.png",
        'title': "IMG_CONTENT_WIDTH_LIGHT",
        'name': "IMG_CONTENT_WIDTH_LIGHT.png",
        'model': Image
    }
    SVG_CONTENT_WIDTH_SPACE = {
        'url': "https://station-spatiale.s3.eu-west-3.amazonaws.com/cms/content-width_space.svg",
        'title': "SVG_CONTENT_WIDTH_SPACE",
        'name': "SVG_CONTENT_WIDTH_SPACE.svg",
        'model': MyDocument
    }
    IMG_CONTENT_WIDTH_SPACE = {
        'url': "https://station-spatiale.s3.eu-west-3.amazonaws.com/cms/content-width_space.png",
        'title': "IMG_CONTENT_WIDTH_SPACE",
        'name': "IMG_CONTENT_WIDTH_SPACE.png",
        'model': Image
    }

    five = lorem_ipsum.words(5)
    hun = lorem_ipsum.words(100)
    animation = {
        'effect': 'fade-right',
        'duration': '1500'
    }
    default_url = "http://localhost:8080"

    @staticmethod
    def button(m_type=constants.BUTTON_PRIMARY_FULL):
        return {
            'text': 'Click here',
            'type': m_type
        }

    @staticmethod
    def file(img):
        try:
            ret = img['model'].objects.get(title=img['title'])
            return ret
        except img['model'].DoesNotExist:
            response = requests.get(img['url'])
            file = ImageFile(BytesIO(response.content), name=img['name'])
            ret = img['model'](
                title=img['title'],
                file=file
            )
            ret.save()
            return ret

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
            'value': Mocker.button(m_type=constants.BUTTON_PRIMARY)
        }, {
            'type': 'button',
            'value': Mocker.button(m_type=constants.BUTTON_SECONDARY)
        }]
        page.header_buttons = json.dumps(header_buttons)
        page.save()
