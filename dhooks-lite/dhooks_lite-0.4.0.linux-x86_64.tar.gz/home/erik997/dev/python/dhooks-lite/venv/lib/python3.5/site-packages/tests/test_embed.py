import datetime
import unittest

from dhooks_lite.embed import Embed, Author, Footer, Field, Image, Thumbnail

from . import set_test_logger

MODULE_PATH = 'dhooks_lite.embed'
logger = set_test_logger(MODULE_PATH, __file__)


class TestEmbedObjectComparing(unittest.TestCase):
    
    def setUp(self):
        self.x1 = Author('Bruce', 'url-1')
        self.x2 = Author('Bruce', 'url-1')
        self.y1 = Author('Bruce', 'url-2')
        self.y2 = Author('Clark', 'url-1')
        self.z = Author('Clark', 'url-2')
            
    def test_objects_are_equal(self):
        self.assertEqual(self.x1, self.x1)
        self.assertEqual(self.x1, self.x2)

    def test_objects_are_not_equal(self):
        self.assertNotEqual(self.x1, self.y1)
        self.assertNotEqual(self.x1, self.y2)
        self.assertNotEqual(self.x1, self.z)
        self.assertNotEqual(self.x1, Footer('Bruce', 'url-1'))


class TestAuthor(unittest.TestCase):

    def test_detect_missing_params_on_create(self):
        with self.assertRaises(ValueError):
            Author(None)

    def test_create_with_name_only(self):
        x = Author('Bruce Wayne')
        self.assertEqual(x.name, 'Bruce Wayne')
        self.assertDictEqual(
            x.to_dict(),
            {
                'name': 'Bruce Wayne'
            }
        )

    def test_create_with_all_params(self):
        x = Author(
            'Bruce Wayne', 
            url='url-1', 
            icon_url='url-2', 
            proxy_icon_url='url-3'
        )
        self.assertEqual(x.name, 'Bruce Wayne')
        self.assertEqual(x.url, 'url-1')
        self.assertEqual(x.icon_url, 'url-2')
        self.assertEqual(x.proxy_icon_url, 'url-3')
        self.assertDictEqual(
            x.to_dict(),
            {
                'name': 'Bruce Wayne',
                'url': 'url-1',
                'icon_url': 'url-2',
                'proxy_icon_url': 'url-3'
            }
        )

  
class TestField(unittest.TestCase):

    def test_detect_missing_params_on_create(self):
        with self.assertRaises(ValueError):
            Field(name=None, value=None)

    def test_detects_name_limit(self):
        large_string = 'x' * 257
        with self.assertRaises(ValueError):
            Field(large_string, value='Batman')

    def test_detects_value_limit(self):
        large_string = 'x' * 1025
        with self.assertRaises(ValueError):
            Field(name='Bruce Wayne', value=large_string)
    
    def test_detect_missing_value(self):
        with self.assertRaises(ValueError):
            Field(name='Bruce Wayne', value=None)

    def test_detect_missing_name(self):
        with self.assertRaises(ValueError):
            Field(name=None, value='Batman')
    
    def test_create_with_name_and_value_only(self):
        x = Field('fruit', 'orange')        
        self.assertEqual(x.name, 'fruit')
        self.assertEqual(x.value, 'orange')
        self.assertEqual(x.inline, True)
        self.assertDictEqual(
            x.to_dict(),
            {
                'name': 'fruit',
                'value': 'orange',
                'inline': True
            }
        )

    def test_create_with_all_params(self):
        x = Field(name='fruit', value='orange', inline=False)       
        self.assertEqual(x.name, 'fruit')
        self.assertEqual(x.value, 'orange')
        self.assertEqual(x.inline, False)
        self.assertDictEqual(
            x.to_dict(),
            {
                'name': 'fruit',
                'value': 'orange',
                'inline': False
            }
        )

    def test_detect_invalid_inline_type(self):
        with self.assertRaises(TypeError):
            Field(name='fruit', value='orange', inline=int(5))


class TestFooter(unittest.TestCase):

    def test_detect_missing_params_on_create(self):
        with self.assertRaises(ValueError):
            Footer(None)

    def test_detects_wrong_type_inline(self):                        
        with self.assertRaises(TypeError):
            Footer('Justice League', inline=int(1))

    def test_create_with_name_only(self):
        x = Footer('Justice League')
        self.assertEqual(x.text, 'Justice League')
        self.assertDictEqual(
            x.to_dict(),
            {
                'text': 'Justice League'
            }
        )

    def test_create_with_all_params(self):
        x = Footer('Justice League', icon_url='url-1', proxy_icon_url='url-2')  
        self.assertEqual(x.text, 'Justice League')
        self.assertEqual(x.icon_url, 'url-1')
        self.assertEqual(x.proxy_icon_url, 'url-2')
        self.assertDictEqual(
            x.to_dict(),
            {
                'text': 'Justice League',
                'icon_url': 'url-1',
                'proxy_icon_url': 'url-2'
            }
        )


class TestImage(unittest.TestCase):
    
    def test_detect_missing_params_on_create(self):
        with self.assertRaises(ValueError):
            Image(None)
    
    def test_create_with_url_only(self):
        x = Image('my-url')        
        self.assertEqual(x.url, 'my-url')
        self.assertDictEqual(
            x.to_dict(),
            {
                'url': 'my-url'
            }
        )
    
    def test_create_with_all_params(self):
        x = Image(url='url-1', proxy_url='url-2', width=500, height=400)
        self.assertEqual(x.url, 'url-1')
        self.assertEqual(x.proxy_url, 'url-2')
        self.assertEqual(x.width, 500)
        self.assertEqual(x.height, 400)
        self.assertDictEqual(
            x.to_dict(),
            {
                'url': 'url-1',
                'proxy_url': 'url-2',
                'width': 500,
                'height': 400
            }
        )

    def test_detect_invalid_width(self):
        with self.assertRaises(ValueError):
            Image('my-url', width=-5)

    def test_detect_invalid_height(self):
        with self.assertRaises(ValueError):
            Image('my-url', height=-5)

  
class TestEmbed(unittest.TestCase):

    def test_create_with_description_only(self):
        x = Embed(
            description='They said the age of heroes would never come again.'
        )
        self.assertEqual(
            x.description, 
            'They said the age of heroes would never come again.'
        )
        self.assertEqual(x.type, 'rich')
        self.assertDictEqual(
            x.to_dict(),
            {
                'type': 'rich',
                'description': 'They said the age of heroes would never come again.'
            }
        )

    def test_create_with_full_params(self):
        now = datetime.datetime.utcnow()
        x = Embed(
            title='Justice League',            
            description='They said the age of heroes would never come again.',
            url='url-1',
            timestamp=now,
            color=0x5CDBF0,
            footer=Footer('TOP SECRET', 'url-2', 'url-11'),
            image=Image('url-3', 'url-4', height=200, width=150),
            thumbnail=Thumbnail('url-5', 'url-6', height=100, width=80),                        
            author=Author('Bruce Wayne', 'url-8', 'url-9'),
            fields=[
                Field('fruit', 'orange', False), 
                Field('vegetable', 'onion', True)
            ]
        )
        self.assertEqual(x.title, 'Justice League')
        self.assertEqual(
            x.description, 
            'They said the age of heroes would never come again.'
        )
        self.assertEqual(x.type, 'rich')
        self.assertEqual(x.url, 'url-1')
        self.assertEqual(x.timestamp, now.isoformat())
        self.assertEqual(x.color, 0x5CDBF0)
        self.assertEqual(x.footer, Footer('TOP SECRET', 'url-2', 'url-11'))
        self.assertEqual(
            x.image, 
            Image('url-3', 'url-4', height=200, width=150)
        )
        self.assertEqual(
            x.thumbnail, 
            Thumbnail('url-5', 'url-6', height=100, width=80)
        )        
        self.assertEqual(x.author, Author('Bruce Wayne', 'url-8', 'url-9'))
        self.assertEqual(
            x.fields, 
            [
                Field('fruit', 'orange', False), 
                Field('vegetable', 'onion', True)
            ]
        )  
        
        self.maxDiff = None
        self.assertDictEqual(
            x.to_dict(),
            {
                'title': 'Justice League',
                'type': 'rich',
                'description': 'They said the age of heroes would never come again.',
                'url': 'url-1',
                'timestamp': now.isoformat(),
                'color': 0x5CDBF0,              
                'image': {
                    'url': 'url-3',
                    'proxy_url': 'url-4',
                    'height': 200,
                    'width': 150
                },
                'thumbnail': {
                    'url': 'url-5',
                    'proxy_url': 'url-6',
                    'height': 100,
                    'width': 80
                },               
                'footer': {
                    'text': 'TOP SECRET',
                    'icon_url': 'url-2',
                    'proxy_icon_url': 'url-11'
                },
                'author': {
                    'name': 'Bruce Wayne',
                    'url': 'url-8',
                    'icon_url': 'url-9'
                },
                'fields': [
                    {
                        'name': 'fruit',
                        'value': 'orange',
                        'inline': False
                    },
                    {
                        'name': 'vegetable',
                        'value': 'onion',
                        'inline': True
                    }
                ]                
            }
        )

    def test_detects_wrong_type_timestamp(self):                        
        with self.assertRaises(TypeError):
            Embed(timestamp=int(1))

    def test_detects_wrong_type_footer(self):                        
        with self.assertRaises(TypeError):
            Embed(footer=int(1))

    def test_detects_wrong_type_image(self):                        
        with self.assertRaises(TypeError):
            Embed(image=int(1))

    def test_detects_wrong_type_thumbnail(self):                        
        with self.assertRaises(TypeError):
            Embed(thumbnail=int(1))

    def test_detects_wrong_type_author(self):
        with self.assertRaises(TypeError):
            Embed(author=int(1))

    def test_detects_wrong_type_fields_list(self):                        
        with self.assertRaises(TypeError):
            Embed(fields=int(1))

    def test_detects_wrong_type_fields_content(self):                        
        with self.assertRaises(TypeError):
            Embed(fields=[int(1), Field('x', 1)])

    def test_detects_max_embed_limit(self):                
        description = 'x' * 2000        
        fields = list()
        for x in range(5):
            fields.append(Field(
                name='name' + str(x),
                value='value' + 'x' * 1000
            ))
        with self.assertRaises(ValueError):
            x = Embed(description=description, fields=fields)

    def test_detects_max_description_limit(self):                
        large_string = 'x' * 2049
        with self.assertRaises(ValueError):
            Embed(description=large_string)

    def test_detects_max_title_limit(self):                
        large_string = 'x' * 257
        with self.assertRaises(ValueError):
            Embed(title=large_string)

    def test_detects_max_fields_limit(self):                
        fields = list()
        for x in range(26):
            fields.append(
                Field(name='name {}'.format(x), value='value {}'.format(x))
            )
        with self.assertRaises(ValueError):
            x = Embed(fields=fields)
