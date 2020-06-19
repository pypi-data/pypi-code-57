from django.db import models
from wagtail.contrib.settings.models import BaseSetting
from wagtail.admin.edit_handlers import TabbedInterface, ObjectList
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.admin.edit_handlers import StreamFieldPanel
from wagtail.core.fields import StreamField, RichTextField
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.documents.blocks import DocumentChooserBlock
from wagtail.images.blocks import ImageChooserBlock
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel
from wagtail.core.models import Orderable
from wagtail.admin.edit_handlers import InlinePanel

LANGUAGE_FR = 'fr'
LANGUAGE_EN = 'en'
LANGUAGE_DE = 'de'
LANGUAGE_NL = 'nl'
LANGUAGE_ES = 'es'
LANGUAGE_IT = 'it'
LANGUAGES = [
    (LANGUAGE_FR, 'French'),
    (LANGUAGE_EN, 'English'),
    (LANGUAGE_DE, 'German'),
    (LANGUAGE_NL, 'Dutch'),
    (LANGUAGE_ES, 'Spanish'),
    (LANGUAGE_IT, 'Italian'),
]
LOCALES = {
    LANGUAGE_FR: 'fr-FR',
    LANGUAGE_EN: 'en-EN',
    LANGUAGE_DE: 'de-DE',
    LANGUAGE_NL: 'nl-NL',
    LANGUAGE_ES: 'es-ES',
    LANGUAGE_IT: 'it-IT',
}


class AFounders(Orderable):
    settings = ParentalKey("WebspaceSettings", related_name="founders")
    name = models.CharField(default='', blank=True, max_length=100)
    gender = models.CharField(choices=[
        ('Male', 'Male'),
        ('Female', 'Female'),
    ], default='', blank=True, max_length=100)
    same_as = models.URLField(blank=True)
    nationality = models.CharField(default='', blank=True, max_length=100)

    general_panels = [
        FieldPanel('name'),
        FieldPanel('gender'),
        FieldPanel('same_as'),
        FieldPanel('nationality'),
    ]

    class Meta:
        verbose_name = 'Founder'
        abstract = True
        app_label = 'cms'


class AWebspaceSettings(BaseSetting, ClusterableModel):
    facebook = models.URLField(blank=True, help_text='Facebook page URL')
    instagram = models.URLField(blank=True, help_text='Instagram page URL')
    linkedin = models.URLField(blank=True, help_text='Linkedin page URL')
    twitter = models.URLField(blank=True, help_text='Twitter page URL')

    brand_name = models.CharField(default='', blank=True, max_length=100)
    logo_header = StreamField([
        ('image', ImageChooserBlock(label="Image - ratio 200x55")),
        ('svg', DocumentChooserBlock(label="Svg - ratio 200x55")),
    ], blank=True)
    logo_schema = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name="Logo Entreprise",
        help_text="Logo pour les Schemas Google"
    )
    favicon = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name="Favicon",
    )
    ga_code = models.CharField(
        default='',
        blank=True,
        max_length=100,
        help_text="Google Analytics - Code de suivis"
    )
    language = models.CharField(
        choices=LANGUAGES,
        default='',
        blank=True,
        max_length=100,
        help_text="Language du site"
    )
    collect_text = RichTextField(
        blank=True,
        default='',
        help_text="Text qui apparait lorsqu'une personne doit accepter les CGU ou autre"
    )
    social_share_text = RichTextField(
        blank=True,
        default='',
        help_text="Text qui apparait sur un block Social Share"
    )
    vat_id = models.CharField(default='', blank=True, max_length=100)
    legal_name = models.CharField(default='', blank=True, max_length=100)
    founding_date = models.DateField(blank=True, default=None, null=True)
    contact_phone = models.CharField(default='', blank=True, max_length=100)
    contact_email = models.CharField(default='', blank=True, max_length=100)
    area_served = models.CharField(default='', blank=True, max_length=100)
    location_street_address = models.CharField(default='', blank=True, max_length=100)
    location_address_locality = models.CharField(default='', blank=True, max_length=100)
    location_postal_code = models.CharField(default='', blank=True, max_length=100)
    location_address_country = models.CharField(default='', blank=True, max_length=100)
    founding_location = models.CharField(default='', blank=True, max_length=100)

    general_panels = [
        FieldPanel('language'),
        FieldPanel('ga_code'),
        FieldPanel('collect_text'),
        FieldPanel('social_share_text')
    ]

    socials_panels = [
        FieldPanel('facebook'),
        FieldPanel('instagram'),
        FieldPanel('linkedin'),
        FieldPanel('twitter'),
    ]

    brand_tab_panels = [
        FieldPanel('brand_name'),
        StreamFieldPanel('logo_header'),
        ImageChooserPanel('favicon'),
        ImageChooserPanel('logo_schema'),
    ]

    organization_panels = [
        FieldPanel('vat_id'),
        FieldPanel('legal_name'),
        FieldPanel('founding_date'),
        FieldPanel('contact_phone'),
        FieldPanel('contact_email'),
        FieldPanel('area_served'),
        FieldPanel('location_street_address'),
        FieldPanel('location_address_locality'),
        FieldPanel('location_postal_code'),
        FieldPanel('location_address_country'),
        FieldPanel('founding_location'),
        InlinePanel("founders", label="Founders")
    ]

    edit_handler = TabbedInterface([
        ObjectList(general_panels, heading='General'),
        ObjectList(brand_tab_panels, heading='Brand'),
        ObjectList(organization_panels, heading='Organization'),
        ObjectList(socials_panels, heading='Socials'),
    ])

    class Meta:
        verbose_name = 'Base'
        abstract = True
        app_label = 'cms'

    @property
    def locale(self):
        return LOCALES[self.language] if self.language in LOCALES else ''
