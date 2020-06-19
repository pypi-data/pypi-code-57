import uuid
from enum import Enum

from django.db import models

from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField


class Contact(models.Model):
    class GENDER(Enum):
        female = (0, 'female')
        male = (1, 'male')
        diverse = (2, 'diverse')

        @classmethod
        def get_value(cls, member):
            return cls[member].value[0]

    first_name = models.CharField(max_length=128)  # without middle names
    last_name = models.CharField(max_length=128)  # without middle names
    display_name = models.CharField(max_length=255)  # full name with prefixes (titles) and suffixes

    gender = models.PositiveSmallIntegerField(choices=[x.value for x in GENDER])

    date_of_birth = models.DateField()

    email = models.EmailField(blank=True, default='')

    def __str__(self):
        return f'{self.display_name}'


class Subject(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    contact = models.ForeignKey(Contact, on_delete=models.CASCADE, related_name='subject_contact')
    guardians = models.ManyToManyField(Contact, blank=True, related_name='guardian_contacts')

    @property
    def is_active(self):
        return not self.inactivity_set.exists()

    @property
    def is_child(self):
        return self.child_set.exists()

    @property
    def is_patient(self):
        return self.patient_set.exists()


class Child(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)


class Patient(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)


class Address(models.Model):
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE, related_name='addresses')
    city = models.CharField(max_length=128)
    country = CountryField(default='DE')
    zip_code = models.CharField(max_length=16)  # c.f. http://en.wikipedia.org/wiki/Postal_codes
    street = models.CharField(max_length=255)  # street name & number + additional info

    def __str__(self):
        return f'{self.street}, {self.zip_code}, {self.city}, {self.country}'


class Phone(models.Model):
    class LABEL(Enum):
        mobile = (0, 'mobile')
        home = (1, 'home')
        work = (2, 'work')
        emergency = (3, 'emergency')
        other = (255, 'other')

        @classmethod
        def get_value(cls, member):
            return cls[member].value[0]

    label = models.PositiveSmallIntegerField(choices=[x.value for x in LABEL])
    number = PhoneNumberField()
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE, related_name='phones')

    def __str__(self):
        return f'{self.number}'


class Inactivity(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    until = models.DateField(null=True)  # until = null means inactive with open end
