# this test script expects the dhooks_lite module to be installed
# in the current environment, e.g. with pip install -e

import logging
from unittest import TestCase
from unittest.mock import Mock, patch

from dhooks_lite.client import Webhook, WebhookResponse
from dhooks_lite import Embed

from . import set_test_logger

MODULE_PATH = 'dhooks_lite.client'
logger = set_test_logger(MODULE_PATH, __file__)

TEST_URL_1 = 'https://www.example.com/test-url-1/'
TEST_URL_2 = 'https://www.example.com/test-url-2/'


def extract_contents(mock_requests):
    """extract results from mock requests"""
    url = None
    json = None
    for x in mock_requests.post.call_args:
        if type(x) == dict and 'url' in x:
            url = x['url']
        if type(x) == dict and 'json' in x:
            json = x['json']

    return url, json


def my_sleep(value):
    """mock function for sleep that also checks for valid values"""
    if value < 0:
        raise ValueError('sleep length must be non-negative')


@patch(MODULE_PATH + '.requests', spec=True)
class TestWebhook(TestCase):
    
    def setUp(self):        
        mock_response = Mock()
        mock_response.headers = {'headers': True}
        mock_response.status_code = 200
        mock_response.ok = True
        mock_response.json.return_value = {'message': True}
        mock_response.headers = {'dummy-header': 'abc'}
        self.response = mock_response
    
    def test_can_set_webhook_url(self, mock_requests):                        
        mock_requests.post.return_value = self.response

        hook = Webhook(TEST_URL_2)        
        self.assertEqual(hook.url, TEST_URL_2)
        hook.execute('Hi there')
        url, json = extract_contents(mock_requests)        
        self.assertEqual(url, TEST_URL_2)
    
    def test_detects_missing_webhook_url(self, mock_requests):        
        with self.assertRaises(ValueError):
            Webhook(None)

    def test_can_set_content(self, mock_requests):                
        mock_requests.post.return_value = self.response
        hook = Webhook(TEST_URL_1)        
        hook.execute('Hi there')
        url, json = extract_contents(mock_requests)                
        self.assertDictEqual(json, {'content': 'Hi there'})        

    def test_detects_max_character_limit(self, mock_requests):
        hook = Webhook(TEST_URL_1)
        large_string = 'x' * 2001        
        with self.assertRaises(ValueError):
            hook.execute(large_string)
    
    def test_can_get_send_report(self, mock_requests):         
        mock_requests.post.return_value = self.response
        hook = Webhook(TEST_URL_1)        
        response = hook.execute('Hi there', wait_for_response=True)        
        self.assertDictEqual(response.content, {'message': True})
    
    def test_detects_missing_content_and_embed(self, mock_requests):
        hook = Webhook(TEST_URL_1)
        with self.assertRaises(ValueError):
            hook.execute()
    
    def test_can_set_username(self, mock_requests):                
        mock_requests.post.return_value = self.response        
        hook = Webhook(TEST_URL_1, username='Bruce Wayne')
        self.assertEqual(hook.username, 'Bruce Wayne')
        hook.execute('Hi there')
        url, json = extract_contents(mock_requests)                
        self.assertIn('username', json)
        self.assertEqual(json['username'], 'Bruce Wayne')

    def test_can_set_avatar_url(self, mock_requests):                
        mock_requests.post.return_value = self.response
        hook = Webhook(TEST_URL_1, avatar_url='abc')
        self.assertEqual(hook.avatar_url, 'abc')
        hook.execute('Hi there')
        url, json = extract_contents(mock_requests)
        self.assertIn('avatar_url', json)
        self.assertEqual(json['avatar_url'], 'abc')

    def test_can_send_with_tts(self, mock_requests):                
        mock_requests.post.return_value = self.response
        hook = Webhook('abc')        
        hook.execute('Hi there', tts=True)
        url, json = extract_contents(mock_requests)
        self.assertIn('tts', json)
        self.assertEqual(json['tts'], True)

    def test_detect_wrong_tts_type(self, mock_requests):                
        hook = Webhook('abc')        
        with self.assertRaises(TypeError):
            hook.execute('Hi there', tts=int(5))
    
    def test_detects_wrong_embeds_type(self, mock_requests):
        hook = Webhook(TEST_URL_1)                
        with self.assertRaises(TypeError):
            hook.execute('dummy', embeds=int(5))
    
    def test_detects_wrong_embeds_element_type(self, mock_requests):
        hook = Webhook(TEST_URL_1)
        e = [int(5), float(5)]
        with self.assertRaises(TypeError):
            hook.execute('dummy', embeds=e)
    
    def test_returns_none_on_invalid_response(self, mock_requests):        
        mock_requests.post.return_value.json.side_effect = ValueError
        hook = Webhook(TEST_URL_1)        
        response = hook.execute('Hi there')
        self.assertIsNone(response.content)

    @patch(MODULE_PATH + '.logger.getEffectiveLevel', return_value=logging.DEBUG)
    def test_produce_debug_logging(self, mock_requests, mock_logger):
        mock_requests.post.return_value = self.response
        hook = Webhook('abc')        
        hook.execute('Hi there')

    @patch(MODULE_PATH + '.logger.getEffectiveLevel', return_value=logging.INFO)
    def test_produce_normal_logging_with_http_error(
        self, mock_requests, mock_logger
    ):
        mock_response = Mock()
        mock_response.headers = {'headers': True}
        mock_response.status_code = 404
        mock_response.ok = False
        mock_response.json.return_value = {'message': True}
        mock_requests.post.return_value = mock_response
        hook = Webhook('abc')        
        hook.execute('Hi there')

    @patch(MODULE_PATH + '.logger.getEffectiveLevel', return_value=logging.INFO)
    def test_produce_no_logging_when_http_ok(
        self, mock_requests, mock_logger
    ):
        mock_requests.post.return_value = self.response
        hook = Webhook('abc')        
        hook.execute('Hi there')

    @patch(MODULE_PATH + '.BACKOFF_FACTOR', 0.5)
    @patch(MODULE_PATH + '.MAX_RETRIES', 3)
    @patch(MODULE_PATH + '.sleep')
    def test_can_retry_on_retryable_error_502(self, mock_sleep, mock_requests):
        self.response.status_code = 502
        self.response.ok = False
        mock_requests.post.return_value = self.response
        mock_sleep.side_effect = my_sleep

        hook = Webhook(TEST_URL_1)        
        hook.execute('Hi there')
        self.assertEqual(mock_requests.post.call_count, 4)

        call_list = mock_sleep.call_args_list
        result = [args[0] for args, kwargs in [x for x in call_list]]
        expected = [1.0, 2.0]
        self.assertListEqual(expected, result)

    @patch(MODULE_PATH + '.MAX_RETRIES', 3)
    @patch(MODULE_PATH + '.sleep')
    def test_can_retry_on_retryable_error_503(self, mock_sleep, mock_requests):
        self.response.status_code = 503
        self.response.ok = False
        mock_requests.post.return_value = self.response
        mock_sleep.side_effect = my_sleep

        hook = Webhook(TEST_URL_1)        
        hook.execute('Hi there')
        self.assertEqual(mock_requests.post.call_count, 4)
    
    @patch(MODULE_PATH + '.MAX_RETRIES', 3)
    @patch(MODULE_PATH + '.sleep')
    def test_can_retry_on_retryable_error_504(self, mock_sleep, mock_requests):
        self.response.status_code = 504
        self.response.ok = False
        mock_requests.post.return_value = self.response
        mock_sleep.side_effect = my_sleep

        hook = Webhook(TEST_URL_1)        
        hook.execute('Hi there')
        self.assertEqual(mock_requests.post.call_count, 4)
        

class TestWebhookResponse(TestCase):

    def setUp(self):
        self.response = WebhookResponse(
            headers={
                'Content-Type': 'application/json'
            },            
            content={
                'username': 'Bruce Wayne',
                'content': 'Checkout this new report'
            },
            status_code=200,
        )
    
    def test_headers(self):
        expected = {
            'Content-Type': 'application/json'
        }
        self.assertDictEqual(self.response.headers, expected)

    def test_status_code(self):
        expected = 200
        self.assertEqual(self.response.status_code, expected)

    def test_content(self):
        expected = {
            'username': 'Bruce Wayne',
            'content': 'Checkout this new report'
        }
        self.assertDictEqual(self.response.content, expected)
    
    def test_create(self):
        obj = WebhookResponse(
            headers={'headers': True},
            status_code=200,
            content={'content': True}
        )
        self.assertEqual(obj.headers, {'headers': True})
        self.assertEqual(obj.status_code, 200)
        self.assertEqual(obj.content, {'content': True})

        obj_2 = WebhookResponse(
            headers={'headers': True},
            status_code=200,
            content=None
        )
        self.assertIsNone(obj_2.content)

    def test_status_ok(self):
        x = WebhookResponse(
            headers={'headers': True},
            status_code=199
        )
        self.assertFalse(x.status_ok)

        x = WebhookResponse(
            headers={'headers': True},
            status_code=200
        )
        self.assertTrue(x.status_ok)

        x = WebhookResponse(
            headers={'headers': True},
            status_code=300,
            content=None
        )
        self.assertFalse(x.status_ok)


@patch(MODULE_PATH + '.requests', spec=True)
class TestWebhookAndEmbed(TestCase):
    
    def setUp(self):        
        x = Mock()
        x.headers = {'headers': True}
        x.status_code = 200
        x.json.return_value = {'message': True}
        self.response = x

    def test_can_send_with_embed_only(self, mock_requests):
        mock_requests.post.return_value = self.response

        hook = Webhook(TEST_URL_1)        
        e = Embed(description='Hello, world!')        
        hook.execute(embeds=[e])
        url, json = extract_contents(mock_requests)
        self.assertIn('embeds', json)
        self.assertEqual(len(json['embeds']), 1)
        self.assertDictEqual(
            json['embeds'][0], {'description': 'Hello, world!', 'type': 'rich'}
        )
    
    def test_can_add_multiple_embeds(self, mock_requests):
        mock_requests.post.return_value = self.response

        hook = Webhook(TEST_URL_1)        
        e1 = Embed(description='Hello, world!')
        e2 = Embed(description='Hello, world! Again!')
        hook.execute('How is it going?', embeds=[e1, e2])
        url, json = extract_contents(mock_requests)
        self.assertIn('embeds', json)
        self.assertEqual(len(json['embeds']), 2)
        self.assertDictEqual(
            json['embeds'][0], {'description': 'Hello, world!', 'type': 'rich'}
        )
        self.assertDictEqual(
            json['embeds'][1], {'description': 'Hello, world! Again!', 'type': 'rich'}
        )
