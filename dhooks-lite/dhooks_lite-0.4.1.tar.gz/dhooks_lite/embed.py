import logging
import datetime
import json


logger = logging.getLogger(__name__)


class _EmbedObject:        
    """base class for all Embed objects"""

    def to_dict(self) -> dict:        
        """returns the properties of an object as dict
        
        will not include properties that are None
        will call to_dict() on all Embed objects        
        """
        arr = dict()
        for key, value in self.__dict__.items():
            if value is not None:
                if isinstance(value, list):
                    v_list = list()
                    for elem in value:
                        if isinstance(elem, (_EmbedObject)):
                            v_list.append(elem.to_dict())
                        else:    
                            raise NotImplementedError()
                    arr[key[1:]] = v_list
                else:
                    if isinstance(value, (_EmbedObject)):
                        arr[key[1:]] = value.to_dict()            
                    else:    
                        arr[key[1:]] = value
        return arr

    def __eq__(self, other):
        """enables comparing all objects by value, including nested objects"""
        if not isinstance(other, type(self)):            
            return False    
        return all(
            self.__dict__[key1] == other.__dict__[key2] 
            for key1, key2 in zip(self.__dict__.keys(), other.__dict__.keys())
        )

    def __ne__(self, other):
        """enables comparing all objects by value, including nested objects"""
        return not self.__eq__(other)


class Author(_EmbedObject):
    """Author in an Embed"""
    def __init__(
        self, 
        name: str, 
        url: str = None, 
        icon_url: str = None,
        proxy_icon_url: str = None
    ):
        if not name:
            raise ValueError('name can not be None')
        
        self._name = str(name)
        self._url = str(url) if url else None
        self._icon_url = str(icon_url) if icon_url else None
        self._proxy_icon_url = str(proxy_icon_url) if proxy_icon_url else None

    @property
    def name(self) -> str:
        return self._name

    @property
    def url(self) -> str:
        return self._url

    @property
    def icon_url(self) -> str:
        return self._icon_url

    @property
    def proxy_icon_url(self) -> str:
        return self._proxy_icon_url


class Field(_EmbedObject):
    """Field in an Embed"""

    MAX_CHARACTERS_NAME = 256
    MAX_CHARACTERS_VALUE = 1024

    def __init__(self, name: str, value: str, inline: bool = True):
        if not name:
            raise ValueError('name can not be None')
        if not value:
            raise ValueError('value can not be None')
        if not isinstance(inline, bool):
            raise TypeError('inline must be of type bool')

        name = str(name)
        if len(name) > self.MAX_CHARACTERS_NAME:
            raise ValueError('name can not exceed {} characters'.format(
                self.MAX_CHARACTERS_NAME
            ))
        value = str(value)        
        if len(value) > self.MAX_CHARACTERS_VALUE:
            raise ValueError('value can not exceed {} characters'.format(
                self.MAX_CHARACTERS_VALUE
            ))
        
        self._name = name
        self._value = value
        self._inline = inline

    @property
    def name(self) -> str:
        return self._name

    @property
    def value(self) -> str:
        return self._value

    @property
    def inline(self) -> str:
        return self._inline


class Footer(_EmbedObject):
    """Footer in an Embed"""
    def __init__(
        self, 
        text: str, 
        icon_url: str = None, 
        proxy_icon_url: str = None
    ):
        if not text:
            raise ValueError('text can not be None')        
                
        self._text = str(text)
        self._icon_url = str(icon_url) if icon_url else None
        self._proxy_icon_url = str(proxy_icon_url) if proxy_icon_url else None

    @property
    def text(self) -> str:
        return self._text

    @property
    def icon_url(self) -> str:
        return self._icon_url

    @property
    def proxy_icon_url(self) -> str:
        return self._proxy_icon_url


class Image(_EmbedObject):
    """Image in an Embed"""
    def __init__(
        self, 
        url: str, 
        proxy_url: str = None, 
        height: int = None, 
        width: int = None
    ):
        if not url:
            raise ValueError('url can not be None')        
        if width and width <= 0:
            raise ValueError('width must be > 0')
        if height and height <= 0:
            raise ValueError('height must be > 0')
                        
        self._url = str(url)
        self._proxy_url = str(proxy_url) if proxy_url else None
        self._height = int(height) if height else None
        self._width = int(width) if width else None

    @property
    def url(self) -> str:
        return self._url

    @property
    def proxy_url(self) -> str:
        return self._proxy_url

    @property
    def height(self) -> str:
        return self._height

    @property
    def width(self) -> str:
        return self._width


class Thumbnail(Image):
    """Thumbnail in an Embed"""    


class Embed(_EmbedObject):    
    """Embedded content for a message"""
    
    MAX_CHARACTERS = 6000
    MAX_TITLE = 256
    MAX_DESCRIPTION = 2048
    MAX_FIELDS = 25
    
    def __init__(
        self, 
        description: str = None,
        title: str = None,
        url: str = None, 
        timestamp: datetime.datetime = None, 
        color: int = None, 
        footer: Footer = None,                        
        image: Image = None, 
        thumbnail: Thumbnail = None,        
        author: Author = None,
        fields: list = None
    ):        
        """Initialize an Embed object

        Parameters

        - description: message text for this embed
        - title: title of embed
        - url: url of embed
        - timestamp: timestamp of embed content
        - color: color code of the embed
        - footer: footer information
        - image: image within embed
        - thumbnail: thumbnail for this embed        
        - author: author information
        - fields: fields information

        Exceptions

        - TypeException: when passing variables of wrong type
        - ValueException: when embed size exceeds hard limit
        
        """
        if timestamp and not isinstance(timestamp, datetime.datetime):
            raise TypeError('timestamp must be a datetime object')
        if footer and not isinstance(footer, Footer):
            raise TypeError('footer must be a Footer object')
        if image and not isinstance(image, Image):
            raise TypeError('image must be an Image object')
        if thumbnail and not isinstance(thumbnail, Thumbnail):
            raise TypeError('thumbnail must be a Thumbnail object')        
        if author and not isinstance(author, Author):
            raise TypeError('author must be a Author object')
        if fields and not isinstance(fields, list):
            raise TypeError('fields must be a list')
        if fields:
            if len(fields) > self.MAX_FIELDS:
                raise ValueError('Fields can not exceed {} objects'.format(
                    self.MAX_FIELDS
                ))
            for f in fields:
                if not isinstance(f, Field):
                    raise TypeError('all elements in fields must be a Field')

        if description and len(description) > self.MAX_DESCRIPTION:
            raise ValueError(
                'description exceeds max length of {} characters'.format(
                    self.MAX_DESCRIPTION
                )
            )

        if title and len(title) > self.MAX_TITLE:
            raise ValueError(
                'title exceeds max length of {} characters'.format(
                    self.MAX_TITLE
                )
            )
        
        self._title = str(title) if title else None
        self._type = 'rich'
        self._description = str(description) if description else None
        self._url = str(url) if url else None
        self._timestamp = timestamp.isoformat() if timestamp else None
        self._color = int(color) if color else None
        self._footer = footer
        self._image = image
        self._thumbnail = thumbnail        
        self._author = author        
        self._fields = fields

        d_json = json.dumps(self.to_dict())
        if len(d_json) > self.MAX_CHARACTERS:
            raise ValueError(
                'Embed exceeds maximum allowed char size of {} by {}'.format(
                    self.MAX_CHARACTERS,
                    len(d_json) - self.MAX_CHARACTERS
                )
            )

    @property
    def description(self) -> str:
        return self._description

    @property
    def title(self) -> str:
        return self._title

    @property
    def type(self) -> str:
        return self._type

    @property
    def url(self) -> str:
        return self._url

    @property
    def timestamp(self) -> str:
        return self._timestamp

    @property
    def color(self) -> str:
        return self._color
    
    @property
    def footer(self) -> str:
        return self._footer

    @property
    def image(self) -> str:
        return self._image

    @property
    def thumbnail(self) -> str:
        return self._thumbnail

    @property
    def author(self) -> str:
        return self._author

    @property
    def fields(self) -> str:
        return self._fields
