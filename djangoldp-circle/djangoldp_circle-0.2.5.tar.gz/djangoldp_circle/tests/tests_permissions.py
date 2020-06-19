import uuid
import json
from datetime import datetime, timedelta
from rest_framework.test import APITestCase, APIClient
from guardian.shortcuts import assign_perm

from djangoldp_circle.models import Circle, CircleMember
from djangoldp_circle.tests.models import User


class PermissionsTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()

    def setUpLoggedInUser(self):
        self.user = User(email='test@mactest.co.uk', first_name='Test', last_name='Mactest', username='test',
                         password='glass onion')
        self.user.save()
        self.client.force_authenticate(user=self.user)

    def setUpCircle(self, status_choice='Public', owner=None):
        if owner is None:
            owner = self.user

        self.circle = Circle.objects.create(name='Test', status=status_choice, owner=owner)

    def _get_random_user(self):
        return User.objects.create(email='{}@test.co.uk'.format(str(uuid.uuid4())), first_name='Test', last_name='Test',
                                   username=str(uuid.uuid4()))

    # GET circle - not logged in
    def test_get_circle_anonymous_user(self):
        another_user = self._get_random_user()
        self.setUpCircle('Public', another_user)

        response = self.client.get('/circles/1/')
        self.assertEqual(response.status_code, 403)

    # GET circle public
    def test_get_public_circle(self):
        self.setUpLoggedInUser()
        another_user = self._get_random_user()
        self.setUpCircle('Public', another_user)

        response = self.client.get('/circles/1/')
        self.assertEqual(response.status_code, 200)

    # GET circle private - I am a member
    def test_get_circle_private_member(self):
        self.setUpLoggedInUser()
        self.setUpCircle('Private')

        response = self.client.get('/circles/1/')
        self.assertEqual(response.status_code, 200)

    # GET circle private - I am not a member
    def test_get_circle_private_not_member(self):
        self.setUpLoggedInUser()
        another_user = self._get_random_user()

        self.setUpCircle('Private', another_user)

        response = self.client.get('/circles/1/')
        self.assertEqual(response.status_code, 403)

    # POST a new circle - anyone authenticated can do this
    def test_post_circle(self):
        self.setUpLoggedInUser()

        response = self.client.post('/circles/', json.dumps({}), content_type='application/ld+json')
        self.assertEqual(response.status_code, 201)

    # POST a new circle - anonymous user
    def test_post_circle_anonymous_user(self):
        response = self.client.post('/circles/')
        self.assertEqual(response.status_code, 403)

    # PATCH circle public - denied
    def test_patch_public_circle(self):
        self.setUpLoggedInUser()
        another_user = self._get_random_user()

        self.setUpCircle('Public', another_user)

        response = self.client.patch('/circles/1/', json.dumps({}), content_type='application/ld+json')
        self.assertEqual(response.status_code, 403)

    # PATCH circle - I am a member but not an admin - denied
    def test_patch_circle_not_admin(self):
        self.setUpLoggedInUser()
        another_user = self._get_random_user()

        self.setUpCircle('Public', another_user)
        CircleMember.objects.create(circle=self.circle, user=self.user, is_admin=False)

        response = self.client.patch('/circles/1/', json.dumps({}), content_type='application/ld+json')
        self.assertEqual(response.status_code, 403)

    # PATCH circle - I am an admin
    def test_patch_circle_admin(self):
        self.setUpLoggedInUser()
        another_user = self._get_random_user()

        self.setUpCircle('Private', another_user)
        CircleMember.objects.create(circle=self.circle, user=self.user, is_admin=True)

        response = self.client.patch('/circles/1/')
        self.assertEqual(response.status_code, 200)

    # adding a CircleMember - I am not a member myself
    def test_post_circle_member_not_member(self):
        self.setUpLoggedInUser()
        another_user = self._get_random_user()

        self.setUpCircle('Private', another_user)

        payload = {
            'user': {'@id': self.user.urlid},
            'circle': {'@id': self.circle.urlid},
            '@context': {
                '@vocab': "http://happy-dev.fr/owl/#",
                'rdf': "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
                'rdfs': "http://www.w3.org/2000/01/rdf-schema#",
                'ldp': "http://www.w3.org/ns/ldp#",
                'foaf': "http://xmlns.com/foaf/0.1/",
                'name': "rdfs:label",
                'acl': "http://www.w3.org/ns/auth/acl#",
                'permissions': "acl:accessControl",
                'mode': "acl:mode",
                'inbox': "http://happy-dev.fr/owl/#inbox",
                'object': "http://happy-dev.fr/owl/#object",
                'author': "http://happy-dev.fr/owl/#author",
                'account': "http://happy-dev.fr/owl/#account",
                'jabberID': "foaf:jabberID",
                'picture': "foaf:depiction",
                'firstName': "http://happy-dev.fr/owl/#first_name",
                'lastName': "http://happy-dev.fr/owl/#last_name",
                'isAdmin': "http://happy-dev.fr/owl/#is_admin"
            }
        }

        response = self.client.post('/circle-members/', json.dumps(payload), content_type='application/ld+json')
        self.assertEqual(response.status_code, 403)

    def test_post_circle_member_nested_not_member(self):
        self.setUpLoggedInUser()
        another_user = self._get_random_user()

        self.setUpCircle('Private', another_user)

        payload = {
            'user': {'@id': self.user.urlid},
            'circle': {'@id': self.circle.urlid},
            '@context': {
                '@vocab': "http://happy-dev.fr/owl/#",
                'rdf': "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
                'rdfs': "http://www.w3.org/2000/01/rdf-schema#",
                'ldp': "http://www.w3.org/ns/ldp#",
                'foaf': "http://xmlns.com/foaf/0.1/",
                'name': "rdfs:label",
                'acl': "http://www.w3.org/ns/auth/acl#",
                'permissions': "acl:accessControl",
                'mode': "acl:mode",
                'inbox': "http://happy-dev.fr/owl/#inbox",
                'object': "http://happy-dev.fr/owl/#object",
                'author': "http://happy-dev.fr/owl/#author",
                'account': "http://happy-dev.fr/owl/#account",
                'jabberID': "foaf:jabberID",
                'picture': "foaf:depiction",
                'firstName': "http://happy-dev.fr/owl/#first_name",
                'lastName': "http://happy-dev.fr/owl/#last_name",
                'isAdmin': "http://happy-dev.fr/owl/#is_admin"
            }
        }

        response = self.client.post('/circles/1/members/', json.dumps(payload), content_type='application/ld+json')
        self.assertEqual(response.status_code, 403)

        # TODO
        '''payload.pop('user')
        response = self.client.post('/users/{}/circles/'.format(self.user.pk), data=json.dumps(payload),
                                    content_type='application/ld+json')
        self.assertEqual(response.status_code, 403)'''

    # adding a CircleMember - I am a member but not an admin
    def test_post_circle_member(self):
        self.setUpLoggedInUser()
        another_user = self._get_random_user()

        self.setUpCircle('Private', another_user)
        CircleMember.objects.create(circle=self.circle, user=self.user, is_admin=False)

        payload = {
            'user': {'@id': self.user.urlid},
            '@context': {
                '@vocab': "http://happy-dev.fr/owl/#",
                'rdf': "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
                'rdfs': "http://www.w3.org/2000/01/rdf-schema#",
                'ldp': "http://www.w3.org/ns/ldp#",
                'foaf': "http://xmlns.com/foaf/0.1/",
                'name': "rdfs:label",
                'acl': "http://www.w3.org/ns/auth/acl#",
                'permissions': "acl:accessControl",
                'mode': "acl:mode",
                'inbox': "http://happy-dev.fr/owl/#inbox",
                'object': "http://happy-dev.fr/owl/#object",
                'author': "http://happy-dev.fr/owl/#author",
                'account': "http://happy-dev.fr/owl/#account",
                'jabberID': "foaf:jabberID",
                'picture': "foaf:depiction",
                'firstName': "http://happy-dev.fr/owl/#first_name",
                'lastName': "http://happy-dev.fr/owl/#last_name",
                'isAdmin': "http://happy-dev.fr/owl/#is_admin"
            }
        }

        response = self.client.post('/circles/1/members/', json.dumps(payload), content_type='application/ld+json')
        self.assertEqual(response.status_code, 201)

    # removing a CircleMember - I am not an admin
    def test_delete_circle_member(self):
        self.setUpLoggedInUser()
        another_user = self._get_random_user()

        self.setUpCircle('Private', another_user)
        CircleMember.objects.create(circle=self.circle, user=self.user, is_admin=False)

        response = self.client.delete('/circle-members/1/')
        self.assertEqual(response.status_code, 403)

    # removing a circle member - I am not logged in
    def test_delete_circle_member_anonymous_user(self):
        another_user = self._get_random_user()
        self.setUpCircle('Private', another_user)

        response = self.client.delete('/circle-members/1/')
        self.assertEqual(response.status_code, 403)

    # removing myself from CircleMember - I am not an admin
    def test_delete_myself_circle_member(self):
        self.setUpLoggedInUser()
        another_user = self._get_random_user()

        self.setUpCircle('Private', another_user)
        CircleMember.objects.create(circle=self.circle, user=self.user, is_admin=False)

        response = self.client.delete('/circle-members/2/')
        self.assertEqual(response.status_code, 204)

    # adding a CircleMember - I am an admin
    def test_post_circle_member_admin(self):
        self.setUpLoggedInUser()
        self.setUpCircle('Private', self.user)

        another_user = self._get_random_user()

        body = {
            'user': {'@id': another_user.urlid},
            'circle': {'@id': self.circle.urlid},
            '@context': {
                '@vocab': "http://happy-dev.fr/owl/#",
                'rdf': "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
                'rdfs': "http://www.w3.org/2000/01/rdf-schema#",
                'ldp': "http://www.w3.org/ns/ldp#",
                'foaf': "http://xmlns.com/foaf/0.1/",
                'name': "rdfs:label",
                'acl': "http://www.w3.org/ns/auth/acl#",
                'permissions': "acl:accessControl",
                'mode': "acl:mode",
                'inbox': "http://happy-dev.fr/owl/#inbox",
                'object': "http://happy-dev.fr/owl/#object",
                'author': "http://happy-dev.fr/owl/#author",
                'account': "http://happy-dev.fr/owl/#account",
                'jabberID': "foaf:jabberID",
                'picture': "foaf:depiction",
                'firstName': "http://happy-dev.fr/owl/#first_name",
                'lastName': "http://happy-dev.fr/owl/#last_name",
                'isAdmin': "http://happy-dev.fr/owl/#is_admin"
            }
        }

        response = self.client.post('/circle-members/', data=json.dumps(body),
                                    content_type='application/ld+json')
        self.assertEqual(response.status_code, 201)
        circle = Circle.objects.get(pk=self.circle.pk)
        self.assertEqual(len(circle.members.all()), 2)

    # adding a CircleMember - nested field
    def test_post_circle_member_nested_admin(self):
        self.setUpLoggedInUser()
        self.setUpCircle('Private', self.user)

        another_user = self._get_random_user()

        body = {
            'user': {'@id': another_user.urlid},
            'circle': {'@id': self.circle.urlid},
            '@context': {
                '@vocab': "http://happy-dev.fr/owl/#",
                'rdf': "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
                'rdfs': "http://www.w3.org/2000/01/rdf-schema#",
                'ldp': "http://www.w3.org/ns/ldp#",
                'foaf': "http://xmlns.com/foaf/0.1/",
                'name': "rdfs:label",
                'acl': "http://www.w3.org/ns/auth/acl#",
                'permissions': "acl:accessControl",
                'mode': "acl:mode",
                'inbox': "http://happy-dev.fr/owl/#inbox",
                'object': "http://happy-dev.fr/owl/#object",
                'author': "http://happy-dev.fr/owl/#author",
                'account': "http://happy-dev.fr/owl/#account",
                'jabberID': "foaf:jabberID",
                'picture': "foaf:depiction",
                'firstName': "http://happy-dev.fr/owl/#first_name",
                'lastName': "http://happy-dev.fr/owl/#last_name",
                'isAdmin': "http://happy-dev.fr/owl/#is_admin"
            }
        }

        response = self.client.post('/circles/1/members/', data=json.dumps(body),
                                    content_type='application/ld+json')
        self.assertEqual(response.status_code, 201)
        circle = Circle.objects.get(pk=self.circle.pk)
        self.assertEqual(len(circle.members.all()), 2)

        another_user = self._get_random_user()

        body.pop('user')
        response = self.client.post('/users/{}/circles/'.format(another_user.pk), data=json.dumps(body),
                                    content_type='application/ld+json')
        self.assertEqual(response.status_code, 201)
        circle = Circle.objects.get(pk=self.circle.pk)
        self.assertEqual(len(circle.members.all()), 3)

    # removing a CircleMember - I am an admin
    def test_delete_circle_member_admin(self):
        self.setUpLoggedInUser()
        self.setUpCircle('Private', self.user)

        another_user = self._get_random_user()
        CircleMember.objects.create(circle=self.circle, user=another_user, is_admin=False)

        response = self.client.delete('/circle-members/2/')
        self.assertEqual(response.status_code, 204)

    # removing another admin from the Circle
    def test_delete_circle_admin(self):
        self.setUpLoggedInUser()
        self.setUpCircle('Private')

        another_user = self._get_random_user()
        CircleMember.objects.create(circle=self.circle, user=another_user, is_admin=True)

        response = self.client.delete('/circle-members/2/')
        self.assertEqual(response.status_code, 403)

    # removing myself from Circle - I am an admin, but I'm the last admin
    def test_delete_circle_member_admin_last_admin(self):
        self.setUpLoggedInUser()
        self.setUpCircle('Private')

        another_user = self._get_random_user()
        CircleMember.objects.create(circle=self.circle, user=another_user, is_admin=False)

        response = self.client.delete('/circle-members/1/')
        self.assertEqual(response.status_code, 403)

    # removing myself from Circle - I am an admin, and I'm not the last admin
    def test_delete_circle_member_admin_not_last_admin(self):
        self.setUpLoggedInUser()
        self.setUpCircle('Private')

        another_user = self._get_random_user()
        CircleMember.objects.create(circle=self.circle, user=another_user, is_admin=True)

        self.assertEqual(self.circle.members.count(), 2)
        self.assertEqual(self.circle.members.all()[0].user, self.user)
        self.assertEqual(self.circle.members.all()[0].is_admin, True)

        response = self.client.delete('/circle-members/1/')
        self.assertEqual(response.status_code, 204)

    # PATCH circle-member - I am not an admin
    def test_patch_circle_member_not_admin(self):
        self.setUpLoggedInUser()
        another_user = self._get_random_user()

        self.setUpCircle('Private', another_user)
        CircleMember.objects.create(circle=self.circle, user=self.user, is_admin=False)

        response = self.client.patch('/circle-members/1/')
        self.assertEqual(response.status_code, 403)

    # make another admin - I am a circle member
    def test_make_circle_member_admin(self):
        self.setUpLoggedInUser()
        self.setUpCircle('Private', self.user)

        another_user = self._get_random_user()
        CircleMember.objects.create(circle=self.circle, user=another_user, is_admin=False)

        body = {
            'is_admin': True,
            '@context': {
                '@vocab': "http://happy-dev.fr/owl/#",
                'rdf': "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
                'rdfs': "http://www.w3.org/2000/01/rdf-schema#",
                'ldp': "http://www.w3.org/ns/ldp#",
                'foaf': "http://xmlns.com/foaf/0.1/",
                'name': "rdfs:label",
                'acl': "http://www.w3.org/ns/auth/acl#",
                'permissions': "acl:accessControl",
                'mode': "acl:mode",
                'inbox': "http://happy-dev.fr/owl/#inbox",
                'object': "http://happy-dev.fr/owl/#object",
                'author': "http://happy-dev.fr/owl/#author",
                'account': "http://happy-dev.fr/owl/#account",
                'jabberID': "foaf:jabberID",
                'picture': "foaf:depiction",
                'firstName': "http://happy-dev.fr/owl/#first_name",
                'lastName': "http://happy-dev.fr/owl/#last_name",
                'isAdmin': "http://happy-dev.fr/owl/#is_admin"
            }
        }

        response = self.client.patch('/circle-members/2/', json.dumps(body), content_type='application/ld+json')

        self.assertEqual(response.status_code, 200)

        cm = CircleMember.objects.get(pk=2)
        self.assertEqual(cm.is_admin, True)

    # test that django guardian object-level permission is applied
    def test_guardian_view_applied(self):
        self.setUpLoggedInUser()
        another_user = self._get_random_user()
        self.setUpCircle('Private', another_user)

        assign_perm('view_circle', self.user, self.circle)

        response = self.client.get('/circles/1/')

        self.assertEqual(response.status_code, 200)

    # even with object-permission, I can't remove an admin
    def test_delete_circle_admin_guardian(self):
        self.setUpLoggedInUser()
        another_user = self._get_random_user()
        self.setUpCircle('Private', another_user)

        assign_perm('delete_circle', self.user, self.circle)
        assign_perm('view_circle', self.user, self.circle)

        response = self.client.delete('/circle-members/2/')

        self.assertEqual(response.status_code, 403)

    # security test - admin changing which circle they are an admin of
    def test_hack_myself_admin_of_another_circle(self):
        self.setUpLoggedInUser()
        self.setUpCircle('Private', self.user)

        another_user = self._get_random_user()
        circle = Circle.objects.create(name='Test 2', status='Private', owner=another_user)

        payload = {
            'circle': {'@id': circle.urlid},
            '@context': {
                '@vocab': "http://happy-dev.fr/owl/#",
                'rdf': "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
                'rdfs': "http://www.w3.org/2000/01/rdf-schema#",
                'ldp': "http://www.w3.org/ns/ldp#",
                'foaf': "http://xmlns.com/foaf/0.1/",
                'name': "rdfs:label",
                'acl': "http://www.w3.org/ns/auth/acl#",
                'permissions': "acl:accessControl",
                'mode': "acl:mode",
                'inbox': "http://happy-dev.fr/owl/#inbox",
                'object': "http://happy-dev.fr/owl/#object",
                'author': "http://happy-dev.fr/owl/#author",
                'account': "http://happy-dev.fr/owl/#account",
                'jabberID': "foaf:jabberID",
                'picture': "foaf:depiction",
                'firstName': "http://happy-dev.fr/owl/#first_name",
                'lastName': "http://happy-dev.fr/owl/#last_name",
                'isAdmin': "http://happy-dev.fr/owl/#is_admin"
            }
        }

        response = self.client.patch('/circle-members/1/', json.dumps(payload), content_type='application/ld+json')
        self.assertEqual(response.status_code, 403)

        cm = CircleMember.objects.get(pk=1)
        self.assertEqual(cm.circle.pk, self.circle.pk)

    def test_hack_otheruser_member_of_another_circle(self):
        self.setUpLoggedInUser()
        self.setUpCircle('Private', self.user)

        my_accomplice = self._get_random_user()
        CircleMember.objects.create(circle=self.circle, user=my_accomplice, is_admin=False)

        another_user = self._get_random_user()
        circle = Circle.objects.create(name='Test 2', status='Private', owner=another_user)

        payload = {
            'circle': {'@id': circle.urlid},
            'is_admin': True,
            '@context': {
                '@vocab': "http://happy-dev.fr/owl/#",
                'rdf': "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
                'rdfs': "http://www.w3.org/2000/01/rdf-schema#",
                'ldp': "http://www.w3.org/ns/ldp#",
                'foaf': "http://xmlns.com/foaf/0.1/",
                'name': "rdfs:label",
                'acl': "http://www.w3.org/ns/auth/acl#",
                'permissions': "acl:accessControl",
                'mode': "acl:mode",
                'inbox': "http://happy-dev.fr/owl/#inbox",
                'object': "http://happy-dev.fr/owl/#object",
                'author': "http://happy-dev.fr/owl/#author",
                'account': "http://happy-dev.fr/owl/#account",
                'jabberID': "foaf:jabberID",
                'picture': "foaf:depiction",
                'firstName': "http://happy-dev.fr/owl/#first_name",
                'lastName': "http://happy-dev.fr/owl/#last_name",
                'isAdmin': "http://happy-dev.fr/owl/#is_admin"
            }
        }

        response = self.client.patch('/circle-members/1/', data=json.dumps(payload),
                                     content_type='application/ld+json')
        self.assertEqual(response.status_code, 403)

        cm = CircleMember.objects.get(pk=1)
        self.assertEqual(cm.circle.pk, self.circle.pk)

    def test_hack_post_circle_member_to_admin(self):
        self.setUpLoggedInUser()
        another_user = self._get_random_user()
        self.setUpCircle('Private', another_user)

        payload = {
            'circle': {'@id': self.circle.urlid},
            'user': {'@id': self.user.urlid},
            'is_admin': True,
            '@context': {
                '@vocab': "http://happy-dev.fr/owl/#",
                'rdf': "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
                'rdfs': "http://www.w3.org/2000/01/rdf-schema#",
                'ldp': "http://www.w3.org/ns/ldp#",
                'foaf': "http://xmlns.com/foaf/0.1/",
                'name': "rdfs:label",
                'acl': "http://www.w3.org/ns/auth/acl#",
                'permissions': "acl:accessControl",
                'mode': "acl:mode",
                'inbox': "http://happy-dev.fr/owl/#inbox",
                'object': "http://happy-dev.fr/owl/#object",
                'author': "http://happy-dev.fr/owl/#author",
                'account': "http://happy-dev.fr/owl/#account",
                'jabberID': "foaf:jabberID",
                'picture': "foaf:depiction",
                'firstName': "http://happy-dev.fr/owl/#first_name",
                'lastName': "http://happy-dev.fr/owl/#last_name",
                'isAdmin': "http://happy-dev.fr/owl/#is_admin"
            }
        }

        response = self.client.post('/circles/1/members/', data=json.dumps(payload), content_type='application/ld+json')
        self.assertEqual(response.status_code, 403)

    def test_hack_post_circle_member_again_to_admin(self):
        self.setUpLoggedInUser()
        another_user = self._get_random_user()
        self.setUpCircle('Private', another_user)

        CircleMember.objects.create(user=self.user, circle=self.circle, is_admin=False)

        payload = {
            'circle': {'@id': self.circle.urlid},
            'user': {'@id': self.user.urlid},
            'is_admin': True,
            '@context': {
                '@vocab': "http://happy-dev.fr/owl/#",
                'rdf': "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
                'rdfs': "http://www.w3.org/2000/01/rdf-schema#",
                'ldp': "http://www.w3.org/ns/ldp#",
                'foaf': "http://xmlns.com/foaf/0.1/",
                'name': "rdfs:label",
                'acl': "http://www.w3.org/ns/auth/acl#",
                'permissions': "acl:accessControl",
                'mode': "acl:mode",
                'inbox': "http://happy-dev.fr/owl/#inbox",
                'object': "http://happy-dev.fr/owl/#object",
                'author': "http://happy-dev.fr/owl/#author",
                'account': "http://happy-dev.fr/owl/#account",
                'jabberID': "foaf:jabberID",
                'picture': "foaf:depiction",
                'firstName': "http://happy-dev.fr/owl/#first_name",
                'lastName': "http://happy-dev.fr/owl/#last_name",
                'isAdmin': "http://happy-dev.fr/owl/#is_admin"
            }
        }

        self.client.post('/circles/1/members/', data=json.dumps(payload), content_type='application/ld+json')
        self.assertFalse(CircleMember.objects.filter(user=self.user, circle=self.circle, is_admin=True).exists())

    def test_update_circle_owner_distant(self):
        self.setUpLoggedInUser()
        self.setUpCircle('Public', self.user)

        payload = {
            "description": "Test Circle",
            "name": "Test Circle 1",
            "owner": {"@id": "https://distant.com/users/1/"},
            "@id": self.circle.urlid,
            "@context": {"@vocab": "http://happy-dev.fr/owl/#",
                         "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
                         "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
                         "ldp": "http://www.w3.org/ns/ldp#",
                         "foaf": "http://xmlns.com/foaf/0.1/",
                         "name": "rdfs:label",
                         "acl": "http://www.w3.org/ns/auth/acl#",
                         "permissions": "acl:accessControl",
                         "mode": "acl:mode",
                         "geo": "http://www.w3.org/2003/01/geo/wgs84_pos#",
                         "lat": "geo:lat",
                         "lng": "geo:long",
                         "inbox": "http://happy-dev.fr/owl/#inbox",
                         "object": "http://happy-dev.fr/owl/#object",
                         "author": "http://happy-dev.fr/owl/#author",
                         "account": "http://happy-dev.fr/owl/#account",
                         "jabberID": "foaf:jabberID",
                         "picture": "foaf:depiction"}
        }

        response = self.client.patch('/circles/{}/'.format(self.circle.pk),
                                     data=json.dumps(payload), content_type='application/ld+json')
        self.assertEqual(response.status_code, 200)

        circle = Circle.objects.get(pk=self.circle.pk)
        self.assertEqual(circle.owner.urlid, 'https://distant.com/users/1/')