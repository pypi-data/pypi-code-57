import json
from os import listdir
from os.path import isfile, join
from django.core.files.images import ImageFile
from django.core.management.base import BaseCommand
from django.contrib.contenttypes.models import ContentType
from wagtail.core.models import Page, Site
from wagtail.documents.models import Document
from wagtail.images.models import Image

from ....cms.pages import *
from ....cms.management.mock_entries import MockEntries
from ....cms.snippets import \
    MenuItem, \
    Menu, \
    IconSnippet

from ....cms import constants
from ....cms.settings import SocialMediaSettings


class Command(BaseCommand):
    help = 'Cms commands : init'

    def add_arguments(self, parser):
        parser.add_argument('action', type=str)
        parser.add_argument('extra', type=str, nargs='?', default='')

    def handle(self, *args, **options):
        eval('self.' + options['action'] + '(' + options['extra'] + ')')

    def init(self):
        #  Delete all data
        Site.objects.all().delete()
        Page.objects.all().delete()
        Image.objects.all().delete()
        Document.objects.all().delete()
        Menu.objects.all().delete()
        MenuItem.objects.all().delete()
        me = MockEntries()

        # Create page content type

        page_content_type, created = ContentType.objects.get_or_create(
            model='page',
            app_label='wagtailcore'
        )

        # Root page

        root = Page.objects.create(
            title="Root",
            slug='root',
            content_type=page_content_type,
            path='0001',
            depth=1,
            numchild=1,
            url_path='/',
        )
        root.save()

        # -------------------------------- HomePage --------------------------------

        home_page = HomePage.objects.create(
            title="Home Page",
            slug='home',
            path='00010001',
            depth=2,
            numchild=0,
            body=json.dumps([
                me.first_content(),
                me.cards(stop=3, card='custom', carousel=False, container='regular', theme=constants.THEME_LIGHT),
                me.media_text(size_media='xl', reverse=True, section=True),
                me.cards(card='feature'),
                me.media_text(size_media='xl', theme=constants.THEME_LIGHT, section=True),
                me.cards(card='freelance', theme=constants.THEME_LIGHT),
                me.media_text(size_media='xl', reverse=True),
                me.media_text(theme=constants.THEME_LIGHT),
            ])
        )
        home_page.save()
        home_page_menu_id = me.menu(home_page)
        me.add_header_buttons(home_page)

        # Create default site

        site = Site.objects.create(
            hostname='localhost:8080',
            root_page_id=home_page.id,
            is_default_site=True
        )
        site.save()

        # -------------------------------- Content Pages --------------------------------

        freelance_page = ContentPage(
            title="Freelance Page",
            slug='freelance',
            body=json.dumps([
                me.first_content(),
                me.media_text(theme=constants.THEME_LIGHT),
            ])
        )
        home_page.add_child(instance=freelance_page)
        freelance_menu_id = me.menu(freelance_page)
        me.add_menu(freelance_page, home_page_menu_id)
        me.add_menu(home_page, freelance_menu_id)

        company_page = ContentPage(
            title="Company Page",
            slug='entreprise',
            body=json.dumps([
                me.first_content(),
                me.media_text(theme=constants.THEME_LIGHT),
            ])
        )
        home_page.add_child(instance=company_page)
        company_menu_id = me.menu(company_page)
        me.add_menu(company_page, home_page_menu_id)
        me.add_menu(home_page, company_menu_id)

        qsn_page = ContentPage(
            title="QSN Page",
            slug='qui-sommes-nous',
            body=json.dumps([
                me.first_content(),
                me.media_text(size_media='xl'),
            ])
        )
        home_page.add_child(instance=qsn_page)
        qsn_menu_id = me.menu(qsn_page)
        me.add_menu(qsn_page, home_page_menu_id)
        me.add_menu(home_page, qsn_menu_id)

        # -------------------------------- Example --------------------------------

        # -------------------------------- Cards --------------------------------

        block_page = ContentPage(
            title="Example",
            slug='example',
        )
        home_page.add_child(instance=block_page)
        block_menu_id = me.menu(block_page)
        me.add_menu(block_page, home_page_menu_id)
        me.add_menu(home_page, block_menu_id)

        carousel_page = ContentPage(
            title="Cards",
            slug='cards',
            body=json.dumps([
                me.text(txt='<h2>Cards Custom</h2>', align='center'),
                me.cards(stop=1, card='custom', carousel=False, container='content'),
                me.cards(stop=2, card='custom', carousel=False, container='regular'),
                me.cards(stop=3, card='custom', carousel=False, container='regular'),

                me.cards(stop=1, card='custom', carousel=False, theme=constants.THEME_LIGHT, container='content'),
                me.cards(stop=2, card='custom', carousel=False, theme=constants.THEME_LIGHT, container='regular'),
                me.cards(stop=3, card='custom', carousel=False, theme=constants.THEME_LIGHT, container='regular'),

                me.text(txt='<h2>Cards Services</h2>', align='center'),
                me.cards(stop=3, card='service', carousel=False, container='regular'),
                me.cards(stop=3, card='service', carousel=False, theme=constants.THEME_LIGHT, container='regular'),
                me.cards(stop=3, card='feature', carousel=False, container='regular'),
                me.cards(stop=3, card='feature', carousel=False, theme=constants.THEME_LIGHT, container='regular'),
                me.text(txt='<h2>Cards Freelance</h2>', align='center'),
                me.cards(stop=3, card='freelance', carousel=False, container='regular'),
                me.cards(stop=3, card='freelance', carousel=False, theme=constants.THEME_LIGHT, container='regular'),

                me.text(txt='<h2>Carousel Custom</h2>', align='center'),
                me.cards(card='custom'),
                me.cards(card='custom', theme=constants.THEME_LIGHT),
                me.text(txt='<h2>Carousel Services</h2>', align='center'),
                me.cards(card='service'),
                me.cards(card='service', theme=constants.THEME_LIGHT),
                me.cards(card='feature'),
                me.cards(card='feature', theme=constants.THEME_LIGHT),
                me.text(txt='<h2>Carousel Freelance</h2>', align='center'),
                me.cards(card='freelance'),
                me.cards(card='freelance', theme=constants.THEME_LIGHT),
            ])
        )
        block_page.add_child(instance=carousel_page)
        me.menu(carousel_page, block_menu_id)
        me.add_menu(carousel_page, home_page_menu_id)

        # -------------------------------- Media Text --------------------------------

        media_text_page = ContentPage(
            title="Media Text",
            slug='media-text',
            body=json.dumps([
                me.text(txt='<h2>Media Text Regular</h2>', align='center'),
                me.media_text(reverse=True),
                me.media_text(theme=constants.THEME_LIGHT),

                me.text(txt='<h2>Media Text Size XL</h2>', align='center'),
                me.media_text(size_media='xl', reverse=True),
                me.media_text(size_media='xl', theme=constants.THEME_LIGHT),

                me.text(txt='<h2>Media Text Buttons</h2>', align='center'),
                me.media_text(
                    reverse=True,
                    button_1=constants.BUTTON_WHITE_FULL,
                    button_2=constants.BUTTON_WHITE_LIGHT
                ),
                me.media_text(
                    theme=constants.THEME_LIGHT,
                    button_1=constants.BUTTON_GREEN_FULL,
                    button_2=constants.BUTTON_GREEN_LIGHT
                ),

                me.text(txt='<h2>Media Text Background</h2>', align='center'),
                me.media_text(
                    reverse=True,
                    button_1=constants.BUTTON_BLUE_FULL,
                    button_2=constants.BUTTON_BLUE_LIGHT,
                    bg=True
                ),
                me.media_text(
                    theme=constants.THEME_LIGHT,
                    button_1=constants.BUTTON_WHITE_FULL,
                    button_2=constants.BUTTON_WHITE_LIGHT,
                    bg=True
                ),

                me.text(txt='<h2>Media Text Align</h2>', align='center'),
                me.media_text(
                    align='justify',
                    reverse=True,
                    button_1=constants.BUTTON_BLUE_FULL,
                    button_2=constants.BUTTON_BLUE_LIGHT,
                ),
                me.media_text(
                    theme=constants.THEME_LIGHT,
                    button_1=constants.BUTTON_WHITE_FULL,
                    button_2=constants.BUTTON_WHITE_LIGHT,
                    align='center'
                ),
            ])
        )
        block_page.add_child(instance=media_text_page)
        me.menu(media_text_page, block_menu_id)
        me.add_menu(media_text_page, home_page_menu_id)

        # -------------------------------- Text --------------------------------

        text_page = ContentPage(
            title="Text",
            slug='text',
            body=json.dumps([
                me.text(size='example', align='left'),
                me.text(size='example', align='left', theme=constants.THEME_LIGHT),

                me.text(size='normal', align='left'),
                me.text(size='normal', align='left', theme=constants.THEME_LIGHT),

                me.text(size='big', align='left'),
                me.text(size='big', align='left', theme=constants.THEME_LIGHT),
            ])
        )
        block_page.add_child(instance=text_page)
        me.menu(text_page, block_menu_id)
        me.add_menu(text_page, home_page_menu_id)

        # -------------------------------- Image --------------------------------

        image_page = ContentPage(
            title="Images",
            slug='images',
            body=json.dumps([
                me.text(txt='<h2>JPG</h2>', align='center', theme=constants.THEME_LIGHT),
                me.text(txt='<p>Size XS</p>', align='center', theme=constants.THEME_LIGHT),
                me.image(size='xs'),
                me.text(txt='<p>Size S</p>', align='center', theme=constants.THEME_LIGHT),
                me.image(size='s'),
                me.text(txt='<p>Size M</p>', align='center', theme=constants.THEME_LIGHT),
                me.image(size='m'),
                me.text(txt='<p>Size L</p>', align='center', theme=constants.THEME_LIGHT),
                me.image(size='l'),
                me.text(txt='<p>Size X</p>', align='center', theme=constants.THEME_LIGHT),
                me.image(size='x'),
                me.text(txt='<p>Size XL</p>', align='center', theme=constants.THEME_LIGHT),
                me.image(size='xl'),

                me.text(txt='<h2>SVG</h2>', align='center'),
                me.text(txt='<p>Size XS</p>', align='center'),
                me.svg(size='xs', theme=constants.THEME_LIGHT),
                me.text(txt='<p>Size S</p>', align='center'),
                me.svg(size='s', theme=constants.THEME_LIGHT),
                me.text(txt='<p>Size M</p>', align='center'),
                me.svg(size='m', theme=constants.THEME_LIGHT),
                me.text(txt='<p>Size L</p>', align='center'),
                me.svg(size='l', theme=constants.THEME_LIGHT),
                me.text(txt='<p>Size X</p>', align='center'),
                me.svg(size='x', theme=constants.THEME_LIGHT),
                me.text(txt='<p>Size XL</p>', align='center'),
                me.svg(size='xl', theme=constants.THEME_LIGHT),
            ])
        )
        block_page.add_child(instance=image_page)
        me.menu(image_page, block_menu_id)
        me.add_menu(image_page, home_page_menu_id)

        # -------------------------------- First Content --------------------------------

        first_content_page = ContentPage(
            title="First Content",
            slug='first-content',
            body=json.dumps([
                me.first_content(),
                me.first_content(
                    theme=constants.THEME_LIGHT,
                    button_1=constants.BUTTON_WHITE_LIGHT,
                    button_2=constants.BUTTON_WHITE_FULL
                ),
                me.first_content(align='center'),
                me.first_content(
                    align='center',
                    theme=constants.THEME_LIGHT,
                    button_1=constants.BUTTON_WHITE_LIGHT,
                    button_2=constants.BUTTON_WHITE_FULL
                ),
                me.first_content(align='right'),
                me.first_content(
                    align='right',
                    theme=constants.THEME_LIGHT,
                    button_1=constants.BUTTON_WHITE_LIGHT,
                    button_2=constants.BUTTON_WHITE_FULL
                )
            ])
        )
        block_page.add_child(instance=first_content_page)
        me.menu(first_content_page, block_menu_id)
        me.add_menu(first_content_page, home_page_menu_id)

        # -------------------------------- CTA --------------------------------

        cta_page = ContentPage(
            title="CTA",
            slug='cta',
            body=json.dumps([
                me.text(txt='<h1>CTA</h1>', align='center'),
                me.cta()
            ])
        )
        block_page.add_child(instance=cta_page)
        me.menu(cta_page, block_menu_id)
        me.add_menu(cta_page, home_page_menu_id)

        # -------------------------------- Contact Freelance --------------------------------

        contact_freelance_page = ContentPage(
            title="Contact Freelance",
            slug='contact-freelance',
            body=json.dumps([
                me.text(txt='<h1>Contact Freelance</h1>', align='center'),
                me.contact_freelance()
            ])
        )
        block_page.add_child(instance=contact_freelance_page)
        me.menu(contact_freelance_page, block_menu_id)
        me.add_menu(contact_freelance_page, home_page_menu_id)

        # -------------------------------- Jobs Popular --------------------------------

        jobs_popular_page = ContentPage(
            title="Jobs Popular",
            slug='jobs-popular',
            body=json.dumps([
                me.text(txt='<h1>Jobs Popular</h1>', align='center'),
                me.jobs_popular()
            ])
        )
        block_page.add_child(instance=jobs_popular_page)
        me.menu(jobs_popular_page, block_menu_id)
        me.add_menu(jobs_popular_page, home_page_menu_id)

        # -------------------------------- Timeline --------------------------------

        timeline_page = ContentPage(
            title="Timeline",
            slug='timeline',
            body=json.dumps([
                me.text(txt='<h1>Timeline</h1>', align='center'),
                me.timeline()
            ])
        )
        block_page.add_child(instance=timeline_page)
        me.menu(timeline_page, block_menu_id)
        me.add_menu(timeline_page, home_page_menu_id)

        # -------------------------------- Line Medias --------------------------------

        medias_line_page = ContentPage(
            title="Medias Line",
            slug='medias-line',
            body=json.dumps([
                me.text(txt='<h1>Medias Line</h1>', align='center'),
                me.medias_line(2),
                me.medias_line(),
                me.medias_line(4),
            ])
        )
        block_page.add_child(instance=medias_line_page)
        me.menu(medias_line_page, block_menu_id)
        me.add_menu(medias_line_page, home_page_menu_id)

        # -------------------------------- Grid Info --------------------------------

        grid_info_page = ContentPage(
            title="Grid Info",
            slug='grid-info',
            body=json.dumps([
                me.text(txt='<h1>Grid Info</h1>', align='center'),
                me.grid_info(),
            ])
        )
        block_page.add_child(instance=grid_info_page)
        me.menu(grid_info_page, block_menu_id)
        me.add_menu(grid_info_page, home_page_menu_id)

        # -------------------------------- Buttons --------------------------------

        buttons_page = ContentPage(
            title="Buttons",
            slug='buttons',
            body=json.dumps([
                me.text(txt='<h1>Buttons</h1>', align='center'),
                me.buttons(),
                me.buttons('center'),
                me.buttons('right'),
            ])
        )
        block_page.add_child(instance=buttons_page)
        me.menu(buttons_page, block_menu_id)
        me.add_menu(buttons_page, home_page_menu_id)

        # -------------------------------- Forms --------------------------------

        form_page = ContentPage(
            title="Forms",
            slug='forms',
            body=json.dumps([
                me.text(txt=me.form, align='left'),
            ])
        )
        block_page.add_child(instance=form_page)
        me.menu(form_page, block_menu_id)
        me.add_menu(form_page, home_page_menu_id)

        # -------------------------------- Social Settings --------------------------------

        social_settings = SocialMediaSettings.for_site(site)
        social_settings.facebook = 'https://www.facebook.com/stationspatialefreelance/'
        social_settings.linkedin = 'https://www.linkedin.com/company/stationspatiale'
        social_settings.instagram = 'https://www.instagram.com/station_spatiale/'
        social_settings.save()

    def icons(self):
        keys = [
            "astro_level_0",
            "astro_level_1",
            "astro_level_2",
            "astro_level_3",
            "angle",
            "back",
            "building",
            "camera",
            "circle_red",
            "circle_green",
            "cross",
            "cross_red",
            "email",
            "facebook",
            "feature",
            "folder",
            "h1",
            "home",
            "info",
            "instagram",
            "left",
            "link",
            "linkedin",
            "lock",
            "map_marker",
            "success",
            "pen",
            "phone",
            "plus",
            "price_service",
            "price_feature",
            "help",
            "right",
            "rocket",
            "search",
            "service",
            "tick",
            "time",
            "trash",
            "user",
            "warning",
            "minus",
            "error",
            "number_1",
            "number_2",
            "number_3",
            "accordion",
            "matching",
        ]
        for key in keys:
            ico, created = IconSnippet.objects.get_or_create(
                key=key
            )
            if created:
                ico.save()

    def docs(self):
        Document.objects.all().delete()
        doc_path = 'CHANGE_ME/cms/management/commands/files/documents'
        doc_files = [f for f in listdir(doc_path) if isfile(join(doc_path, f))]
        for doc_name in doc_files:
            file_title = doc_name.replace('.svg', '').replace('-', ' ').replace('_', ' ').title()
            file = ImageFile(
                open(doc_path + '/' + doc_name, "rb"),
                name=file_title + '.svg'
            )
            try:
                document = Document.objects.get(title=file_title)
            except Document.DoesNotExist:
                document = Document(
                    title=file_title,
                    file=file
                )
                document.save()

            if 'icon_' in doc_name:
                doc_name_sp = doc_name.split('_')
                key_icon = doc_name_sp[1]
                theme = doc_name_sp[2]
                key_icon = key_icon.replace('-', '_')
                try:
                    icon = IconSnippet.objects.get(key=key_icon)
                    if theme == 'light.svg':
                        icon.light = document
                        icon.save()
                    if theme == 'space.svg':
                        icon.space = document
                        icon.save()
                except IconSnippet.DoesNotExist:
                    print("Error key icon does not exist")
                    import pdb
                    pdb.set_trace()

    def imgs(self):
        Image.objects.all().delete()
        doc_path = 'CHANGE_ME/cms/management/commands/files/images'
        doc_files = [f for f in listdir(doc_path) if isfile(join(doc_path, f))]
        for doc_name in doc_files:
            file_title = doc_name.replace('.png', '').replace('-', ' ').replace('_', ' ').title()
            file = ImageFile(
                open(doc_path + '/' + doc_name, "rb"),
                name=file_title + '.png'
            )
            try:
                document = Image.objects.get(title=file_title)
            except Image.DoesNotExist:
                document = Image(
                    title=file_title,
                    file=file
                )
                document.save()
