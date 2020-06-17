from .mapping import BaseDictKey
from dataclasses import dataclass
from typing import *
from urllib.parse import urlparse
import os
import re
from enum import Enum

__all__ = ['PropertyValueInput', 'PlaceInput', 'LocationInput', 'PersonIdentifierInput', 'OrganizationInput',
           'PersonInput', 'ThingInput', 'PersonOrThingInput', 'CreateCIDInput', 'UpdateCIDInput',
           'AssignIdentifierInput', 'IdentifierTypeInput']


@dataclass
class PropertyValueInput:
    name: str
    value: str

    def validate(self):
        errors = []
        if self.name is None:
            errors.append('Property name is required')
        if self.value is None:
            errors.append('Property value is required')
        return errors


@dataclass
class PlaceInput(BaseDictKey):
    streetAddress: str
    city: str
    state: str
    postalCode: str
    country: str
    countryCode: str
    latitude: float
    longitude: float
    url: str

    def validate(self):
        errors = []
        if self.latitude and (self.latitude < -90 or self.latitude > 90):
            errors.append('Latitude value is invalid')
        if self.longitude and (self.longitude < -180 or self.longitude > 180):
            errors.append('Longitude value is invalid')
        if self.url and not re.match(r'^http', str(self.url)):
            errors.append('URL must begin with https or http')
        return errors


@dataclass
class LocationInput(BaseDictKey):
    artifact: str
    representation: List[str]

    def validate(self):
        if self.representation is None and self.artifact is None:
            return ['Representation or Artifact link is required']

        errors = []
        if self.representation:
            for image_link in self.representation:
                parse_res = urlparse(image_link)
                if parse_res.scheme not in ['http', 'https']:
                    errors.append(f'Representation must be http link. {image_link}')
                    continue
                filename, file_ext = os.path.splitext(parse_res.path)
                if file_ext.lower() not in ['.jpg', '.jpeg', '.png', '.gif', 'tiff']:
                    errors.append(f'Representation links must be images. {image_link}')
                    continue
        if self.artifact:
            parse_res = urlparse(self.artifact)
            if parse_res.scheme not in ['http', 'https']:
                errors.append(f'Representation must be http link. {self.artifact}')
        return errors


@dataclass
class PersonIdentifierInput(BaseDictKey):
    ORCID: str
    ISNI: str
    Twitter: str
    Other: str

    def validate(self):
        if self.ORCID is None and self.ISNI is None and self.Twitter is None and self.Other is None:
            return ['At least one of the Person Identifier fields must be supplied']


@dataclass
class OrganizationInput(BaseDictKey):
    identifier: PropertyValueInput
    name: str
    where: PlaceInput
    image: str

    def validate(self):
        errors = []
        if self.name is None and self.identifier is None:
            errors.append('Organization name or identifier is required')
        return errors


@dataclass
class PersonInput(BaseDictKey):
    identifier: PersonIdentifierInput
    name: str
    givenName: str
    additionalName: str
    familyName: str
    honorificPrefix: str
    honorificSuffix: str
    alternateName: str
    email: str
    image: str
    jobTitle: str
    department: OrganizationInput
    worksFor: OrganizationInput

    def validate(self):
        errors = []
        if self.name is None:
            errors.append('Person name is required')
        if self.email and not re.match(r'^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$', str(self.email)):
            errors.append('Email is invalid')
        return errors


@dataclass
class ThingInput(BaseDictKey):
    identifier: PropertyValueInput
    name: str
    image: str

    def validate(self):
        errors = []
        if self.name is None and self.identifier is None:
            errors.append('Thing identifier or name is required')
        return errors


@dataclass
class PersonOrThingInput(BaseDictKey):
    person: PersonInput
    thing: ThingInput

    def validate(self):
        errors = []
        if self.person is not None:
            errors.extend(self.person.validate())
        if self.thing is not None:
            errors.extend(self.thing.validate())
        return errors


@dataclass
class CreateCIDInput(BaseDictKey):
    who: PersonOrThingInput
    what: ThingInput
    where: PlaceInput
    location: LocationInput
    props: List[PropertyValueInput]

    def validate(self):
        errors = []
        if self.location:
            errors.extend(self.location.validate())
        if self.who is not None:
            errors.extend(self.who.validate())
        if self.what is not None:
            errors.extend(self.what.validate())
        if self.where is not None:
            errors.extend(self.where.validate())
        return errors


@dataclass
class UpdateCIDInput(BaseDictKey):
    cid: str
    who: PersonOrThingInput
    what: ThingInput
    where: PlaceInput
    location: LocationInput
    props: List[PropertyValueInput]

    def validate(self):
        CID_PREFIX = '20.500.12592'

        errors = []
        if not self.cid:
            errors.append('cid is required')
        elif not self.cid.startswith(CID_PREFIX + '/') or not self.cid.replace(CID_PREFIX, '')[1:].isalnum():
            errors.append('Invalid cid format. Must be 20.500.12592/abcdef')
        if self.location:
            errors.extend(self.location.validate())
        if self.who is not None:
            errors.extend(self.who.validate())
        if self.what is not None:
            errors.extend(self.what.validate())
        if self.where is not None:
            errors.extend(self.where.validate())
        return errors

class IdentifierTypeInput(Enum):
    DOI = 1
    ARK = 2
    OCLC = 3
    PARENT = 4

@dataclass
class AssignIdentifierInput(BaseDictKey):
    cid: str
    identifier: str
    type: IdentifierTypeInput

    def validate(self):
        errors = []
        if not self.cid:
            errors.append('cid is required')
        if not self.type:
            errors.append('type is required')
        if self.type == IdentifierTypeInput.DOI and not re.match(r'^10.\d{4,9}/[-._;()/:a-zA-Z0-9]+$',
                                                                 str(self.identifier)):
            errors.append('DOI format is invalid. Expecting 10.(digits)/(handle)')
        if self.type == IdentifierTypeInput.ARK and not re.match(r'^ark\:/\d{4,9}/[/:a-zA-Z0-9]+',
                                                                 str(self.identifier)):
            errors.append('ARK format is invalid. Expecting ark:/(NAAN)/(handle)')
        if self.type == IdentifierTypeInput.PARENT and not re.match(r'^20\.500\.12592/[a-z0-9]+$',
                                                                 str(self.identifier)):
            errors.append('PARENT CID format is invalid. Expecting 20.500.12592/(handle)')
        return errors

@dataclass
class RemoveIdentifierInput(BaseDictKey):
    cid: str
    identifier: str
    type: IdentifierTypeInput

    def validate(self):
        errors = []
        if not self.cid:
            errors.append('cid is required')
        if not self.type:
            errors.append('type is required')
        if self.type == IdentifierTypeInput.DOI and not re.match(r'^10.\d{4,9}/[-._;()/:a-zA-Z0-9]+$',
                                                                 str(self.identifier)):
            errors.append('DOI format is invalid. Expecting 10.(digits)/(handle)')
        if self.type == IdentifierTypeInput.ARK and not re.match(r'^ark\:/\d{4,9}/[/:a-zA-Z0-9]+',
                                                                 str(self.identifier)):
            errors.append('ARK format is invalid. Expecting ark:/(NAAN)/(handle)')
        if self.type == IdentifierTypeInput.PARENT and not re.match(r'^20\.500\.12592/[a-z0-9]+$',
                                                                 str(self.identifier)):
            errors.append('PARENT CID format is invalid. Expecting 20.500.12592/(handle)')
        return errors
