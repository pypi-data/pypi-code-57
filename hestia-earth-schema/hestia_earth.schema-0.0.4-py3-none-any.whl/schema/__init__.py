# auto-generated content
from collections import OrderedDict
from enum import Enum


class NodeType(Enum):
    ACTOR = 'Actor'
    BIBLIOGRAPHY = 'Bibliography'
    CYCLE = 'Cycle'
    INVENTORY = 'Inventory'
    ORGANISATION = 'Organisation'
    SITE = 'Site'
    SOURCE = 'Source'
    TERM = 'Term'


class SchemaType(Enum):
    ACTOR = 'Actor'
    BIBLIOGRAPHY = 'Bibliography'
    COMPLETENESS = 'Completeness'
    CYCLE = 'Cycle'
    EMISSION = 'Emission'
    INFRASTRUCTURE = 'Infrastructure'
    INPUT = 'Input'
    INVENTORY = 'Inventory'
    MEASUREMENT = 'Measurement'
    ORGANISATION = 'Organisation'
    PRODUCT = 'Product'
    PROPERTY = 'Property'
    SITE = 'Site'
    SOURCE = 'Source'
    TERM = 'Term'


class Actor:
    def __init__(self):
        self.fields = OrderedDict()
        self.fields['type'] = 'Actor'
        self.fields['name'] = ''
        self.fields['firstName'] = ''
        self.fields['lastName'] = ''
        self.fields['orcid'] = ''
        self.fields['scopusID'] = ''
        self.fields['primaryInstitution'] = ''
        self.fields['city'] = ''
        self.fields['country'] = ''
        self.fields['email'] = ''
        self.fields['website'] = ''


class BibliographyDocumentType(Enum):
    BILL = 'bill'
    BOOK = 'book'
    BOOK_SECTION = 'book_section'
    CASE = 'case'
    COMPUTER_PROGRAM = 'computer_program'
    CONFERENCE_PROCEEDINGS = 'conference_proceedings'
    ENCYCLOPEDIA_ARTICLE = 'encyclopedia_article'
    FILM = 'film'
    GENERIC = 'generic'
    HEARING = 'hearing'
    JOURNAL = 'journal'
    MAGAZINE_ARTICLE = 'magazine_article'
    NEWSPAPER_ARTICLE = 'newspaper_article'
    PATENT = 'patent'
    REPORT = 'report'
    STATUTE = 'statute'
    TELEVISION_BROADCAST = 'television_broadcast'
    THESIS = 'thesis'
    WEB_PAGE = 'web_page'
    WORKING_PAPER = 'working_paper'


class Bibliography:
    def __init__(self):
        self.fields = OrderedDict()
        self.fields['type'] = 'Bibliography'
        self.fields['name'] = ''
        self.fields['documentDOI'] = ''
        self.fields['arxivID'] = ''
        self.fields['isbn'] = ''
        self.fields['issn'] = ''
        self.fields['scopus'] = ''
        self.fields['ssrn'] = ''
        self.fields['mendeleyID'] = ''
        self.fields['title'] = ''
        self.fields['documentType'] = ''
        self.fields['authors'] = []
        self.fields['outlet'] = ''
        self.fields['year'] = None
        self.fields['volume'] = None
        self.fields['issue'] = None
        self.fields['chapter'] = ''
        self.fields['pages'] = ''
        self.fields['publisher'] = ''
        self.fields['city'] = ''
        self.fields['editors'] = []
        self.fields['institutionPub'] = []
        self.fields['websites'] = []
        self.fields['dateAccessed'] = None
        self.fields['abstract'] = ''


class Completeness:
    def __init__(self):
        self.fields = OrderedDict()
        self.fields['type'] = 'Completeness'
        self.fields['fertilizer'] = None
        self.fields['soilAmend'] = None
        self.fields['pesticides'] = None
        self.fields['water'] = None
        self.fields['elecFuel'] = None
        self.fields['coProducts'] = None
        self.fields['residue'] = None
        self.fields['manureMgmt'] = None


class CycleFunctionalUnitMeasure(Enum):
    _1_HA = '1 ha'
    RELATIVE = 'relative'


class Cycle:
    def __init__(self):
        self.fields = OrderedDict()
        self.fields['type'] = 'Cycle'
        self.fields['name'] = ''
        self.fields['site'] = None
        self.fields['defaultSource'] = None
        self.fields['startDate'] = None
        self.fields['endDate'] = None
        self.fields['cycleDuration'] = None
        self.fields['croppingDuration'] = None
        self.fields['treatment'] = ''
        self.fields['treatmentDescription'] = ''
        self.fields['functionalUnitMeasure'] = ''
        self.fields['functionalUnitDetails'] = ''
        self.fields['dataCompleteness'] = []
        self.fields['inputs'] = []
        self.fields['emissions'] = []
        self.fields['products'] = []
        self.fields['practices'] = []
        self.fields['dataPrivate'] = None


class EmissionSdDefinition(Enum):
    CYCLES = 'cycles'
    FARMS = 'farms'
    REPLICATIONS = 'replications'
    SITES = 'sites'


class Emission:
    def __init__(self):
        self.fields = OrderedDict()
        self.fields['type'] = 'Emission'
        self.fields['term'] = None
        self.fields['description'] = ''
        self.fields['value'] = []
        self.fields['relDays'] = []
        self.fields['sd'] = None
        self.fields['sdDefinition'] = ''
        self.fields['properties'] = []
        self.fields['method'] = None
        self.fields['methodDescription'] = ''
        self.fields['methodTier'] = None
        self.fields['characterisation'] = None
        self.fields['source'] = None


class Infrastructure:
    def __init__(self):
        self.fields = OrderedDict()
        self.fields['type'] = 'Infrastructure'
        self.fields['name'] = ''
        self.fields['term'] = None
        self.fields['startDate'] = None
        self.fields['endDate'] = None
        self.fields['lifespan'] = None
        self.fields['source'] = None
        self.fields['inputs'] = []


class InputSdDefinition(Enum):
    CYCLES = 'cycles'
    FARMS = 'farms'
    REPLICATIONS = 'replications'
    SITES = 'sites'


class Input:
    def __init__(self):
        self.fields = OrderedDict()
        self.fields['type'] = 'Input'
        self.fields['term'] = None
        self.fields['description'] = ''
        self.fields['value'] = []
        self.fields['relDays'] = []
        self.fields['sd'] = None
        self.fields['sdDefinition'] = ''
        self.fields['currency'] = ''
        self.fields['price'] = None
        self.fields['cost'] = None
        self.fields['properties'] = []
        self.fields['method'] = None
        self.fields['methodDescription'] = ''
        self.fields['source'] = None
        self.fields['inventory'] = None


class Inventory:
    def __init__(self):
        self.fields = OrderedDict()
        self.fields['type'] = 'Inventory'
        self.fields['name'] = ''
        self.fields['version'] = None
        self.fields['cycle'] = None
        self.fields['product'] = None
        self.fields['functionalUnitMeasure'] = ''
        self.fields['functionalUnitQuantity'] = None
        self.fields['inventory'] = []
        self.fields['dataPrivate'] = None


class Measurement:
    def __init__(self):
        self.fields = OrderedDict()
        self.fields['type'] = 'Measurement'
        self.fields['term'] = None
        self.fields['method'] = None
        self.fields['methodDescription'] = ''
        self.fields['date'] = ''
        self.fields['time'] = ''
        self.fields['units'] = ''
        self.fields['value'] = None
        self.fields['sd'] = None
        self.fields['depthUpper'] = None
        self.fields['depthLower'] = None
        self.fields['source'] = None


class Organisation:
    def __init__(self):
        self.fields = OrderedDict()
        self.fields['type'] = 'Organisation'
        self.fields['name'] = ''
        self.fields['latitude'] = None
        self.fields['longitude'] = None
        self.fields['streetAddress'] = ''
        self.fields['city'] = ''
        self.fields['addressRegion'] = ''
        self.fields['country'] = ''
        self.fields['postOfficeBoxNumber'] = ''
        self.fields['postalCode'] = ''
        self.fields['startDate'] = None
        self.fields['endDate'] = None
        self.fields['dataPrivate'] = None


class ProductSdDefinition(Enum):
    CYCLES = 'cycles'
    FARMS = 'farms'
    REPLICATIONS = 'replications'
    SITES = 'sites'


class Product:
    def __init__(self):
        self.fields = OrderedDict()
        self.fields['type'] = 'Product'
        self.fields['term'] = None
        self.fields['description'] = ''
        self.fields['value'] = []
        self.fields['relDays'] = []
        self.fields['sd'] = None
        self.fields['sdDefinition'] = ''
        self.fields['currency'] = ''
        self.fields['price'] = None
        self.fields['revenue'] = None
        self.fields['economicValueShare'] = None
        self.fields['properties'] = []
        self.fields['method'] = None
        self.fields['methodDescription'] = ''
        self.fields['destination'] = None
        self.fields['source'] = None


class Property:
    def __init__(self):
        self.fields = OrderedDict()
        self.fields['type'] = 'Property'
        self.fields['term'] = None
        self.fields['key'] = None
        self.fields['value'] = None
        self.fields['iri'] = None
        self.fields['sd'] = None
        self.fields['source'] = None


class SiteSiteType(Enum):
    BUILDING = 'building'
    FIELD = 'field'
    NATURAL_VEGETATION = 'natural vegetation'
    POND = 'pond'


class Site:
    def __init__(self):
        self.fields = OrderedDict()
        self.fields['type'] = 'Site'
        self.fields['siteType'] = ''
        self.fields['name'] = ''
        self.fields['organisation'] = None
        self.fields['defaultSource'] = None
        self.fields['boundary'] = None
        self.fields['area'] = None
        self.fields['latitude'] = None
        self.fields['longitude'] = None
        self.fields['country'] = ''
        self.fields['region'] = ''
        self.fields['subRegion'] = ''
        self.fields['subSubRegion'] = ''
        self.fields['subSubSubRegion'] = ''
        self.fields['startDate'] = None
        self.fields['endDate'] = None
        self.fields['measurements'] = []
        self.fields['infrastructure'] = []
        self.fields['practices'] = []
        self.fields['dataPrivate'] = None


class Source:
    def __init__(self):
        self.fields = OrderedDict()
        self.fields['type'] = 'Source'
        self.fields['name'] = ''
        self.fields['bibliography'] = None
        self.fields['metaAnalysisBibliography'] = None
        self.fields['doiHESTIA'] = ''
        self.fields['uploadDate'] = None
        self.fields['uploadBy'] = None
        self.fields['validationDate'] = None
        self.fields['validationBy'] = []
        self.fields['intendedApplication'] = ''
        self.fields['studyReasons'] = ''
        self.fields['intendedAudience'] = ''
        self.fields['comparativeAssertions'] = None
        self.fields['design'] = ''


class TermTermType(Enum):
    ANIMALPRODUCT = 'animalProduct'
    AQUACULTUREMANAGEMENT = 'aquacultureManagement'
    BIODIVERSITY = 'biodiversity'
    BUILDING = 'building'
    CHARACTERISATION = 'characterisation'
    CROP = 'crop'
    CROPPROTECTION = 'cropProtection'
    CROPRESIDUEMANAGEMENT = 'cropResidueManagement'
    CROPSUPPORT = 'cropSupport'
    DAIRYMANAGEMENT = 'dairyManagement'
    DESTINATION = 'destination'
    ELECTRICITY = 'electricity'
    EMISSION = 'emission'
    FLOODINGREGIME = 'floodingRegime'
    FUEL = 'fuel'
    INORGANICFERTILIZER = 'inorganicFertilizer'
    IRRIGATION = 'irrigation'
    LANDUSEMANAGEMENT = 'landUseManagement'
    LIVEANIMAL = 'liveAnimal'
    MACHINERY = 'machinery'
    MATERIAL = 'material'
    MEASUREMENT = 'measurement'
    MODEL = 'model'
    ORGANICFERTILIZER = 'organicFertilizer'
    PESTICIDEAI = 'pesticideAI'
    PESTICIDEBRANDNAME = 'pesticideBrandName'
    PROCESSEDFOOD = 'processedFood'
    PROPERTY = 'property'
    SEED = 'seed'
    SOILAMENDMENT = 'soilAmendment'
    SOILTYPE = 'soilType'
    WATER = 'water'


class Term:
    def __init__(self):
        self.fields = OrderedDict()
        self.fields['type'] = 'Term'
        self.fields['termType'] = ''
        self.fields['name'] = ''
        self.fields['shortName'] = ''
        self.fields['synonyms'] = []
        self.fields['definition'] = ''
        self.fields['description'] = ''
        self.fields['units'] = ''
        self.fields['subClassOf'] = None
        self.fields['defaultProperties'] = []
        self.fields['dependentVariables'] = []
        self.fields['independentVariables'] = []
