from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from address.models import AddressField, Address
from phonenumber_field.modelfields import PhoneNumberField
import uuid
from commons.models import MasterDataMixin
from commons.models import IntervalMixin
from commons.models import gender_choices, gender_female, gender_male

# Create your models here.

class Invoice(models.Model):
    class Meta:
        db_table = 'invoices'
        verbose_name = _("számla")
        verbose_name_plural = _("számlák")

class Case(models.Model):
    class Meta:
        db_table = 'cases'
        verbose_name = _("ügy")
        verbose_name_plural = _("ügyek")

class Comment(models.Model):
    class Meta:
        db_table = 'comments'
        verbose_name = _("hozzászólás")
        verbose_name_plural = _("hozzászólások")

class Document(models.Model):
    class Meta:
        db_table = 'documents'
        verbose_name = _("dokumentum")
        verbose_name_plural = _("dokumentumok")

class Attachment(models.Model):
    class Meta:
        db_table = 'attachments'
        verbose_name = _("csatolmány")
        verbose_name_plural = _("csatolmányok")

class ApiConfiguration(models.Model):
    class Meta:
        db_table = 'api_configurations'
        verbose_name = _("interfész beállítás")
        verbose_name_plural = _("interfész beállítások")

class Contact(models.Model):
    class Meta:
        db_table = 'contacts'
        verbose_name = _("kapcsolat")
        verbose_name_plural = _("kapcsolatok")

# ==================================
class Event(models.Model):
    class Meta:
        db_table = 'events'
        verbose_name = _("esemény")
        verbose_name_plural = _("események")

class Appointment(models.Model):
    class Meta:
        db_table = 'appointments'
        verbose_name = _("találkozó")
        verbose_name_plural = _("találkozók")

class Remainder(models.Model):
    class Meta:
        db_table = 'remainders'
        verbose_name = _("emlékeztető")
        verbose_name_plural = _("emlékeztetők")

class Activity(models.Model):
    class Meta:
        db_table = 'activities'
        verbose_name = _("aktivitás")
        verbose_name_plural = _("aktivitások")
# =================================

class Department(models.Model):
    class Meta:
        db_table = 'departments'
        verbose_name = _("részleg")
        verbose_name_plural = _("részlegek")

class Lead(models.Model):
    class Meta:
        db_table = 'leads'
        verbose_name = _("vezető")
        verbose_name_plural = _("vezetők")

class Team(models.Model):
    class Meta:
        db_table = 'teams'
        verbose_name = _("csapat")
        verbose_name_plural = _("csapatok")

# ===========================================

class Tag(models.Model):
    class Meta:
        db_table = 'tags'
        verbose_name = _("címke")
        verbose_name_plural = _("címkék")

class Template(models.Model):
    class Meta:
        db_table = 'templates'
        verbose_name = _("sablon")
        verbose_name_plural = _("sablonok")

class Letter(models.Model):
    class Meta:
        db_table = 'letters'
        verbose_name = _("levél")
        verbose_name_plural = _("levelek")

class Contract(models.Model):
    class Meta:
        db_table = 'contracts'
        verbose_name = _("szerződés")
        verbose_name_plural = _("szerződések")

class Category(models.Model):
    class Meta:
        db_table = 'categories'
        verbose_name = _("kategória")
        verbose_name_plural = _("kategóriák")


class Ledger(models.Model):
    class Meta:
        db_table = 'ledgers'
        verbose_name = _("főkönyv")
        verbose_name_plural = _("főkönyvek")

