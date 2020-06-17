from django.contrib.auth.models import User
from django.test import TestCase

from jauth.serializers import AuthResultSerializer


class Tests(TestCase):
    def add_test_user(self, email: str='test@example.com', password: str='test1234'):
        self.user = User.objects.create_user(email, email, password)

    def setUp(self):
        self.add_test_user()

    def tearDown(self):
        pass

    def test_serializers(self):
        data = AuthResultSerializer(self.user).data
        self.assertIn('token', data)
        self.assertIn('user', data)
        self.assertIn('id', data['user'])
        self.assertIn('username', data['user'])
        self.assertIn('email', data['user'])
        self.assertDictEqual(data['user'], {'id': self.user.id, 'email': self.user.email, 'username': self.user.username})
