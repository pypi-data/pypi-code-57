from rest_framework import status
from sbc_drf.tests import TestCase

from . import factories


class UserTestCase(TestCase):
    USER_PASSWORD = 'z57^6EhdqMw&'
    ENDPOINT = '/users'

    def setUp(self):
        super().setUp()

        self.users = factories.UserFactory.create_batch(5)
        self.user = self.users[0]
        self.admin = factories.AdminUserFactory()
        self.admin_client = self.get_client(self.admin)
        self.user_client = self.get_client(self.user)

    def test_create(self):
        data = factories.RegistrationFactory()
        resp = self.client.post(self.ENDPOINT, data=data)

        self.assertEqual(resp.status_code, self.status_code.HTTP_201_CREATED, resp.data)

    def test_update(self):
        user = factories.StaffUserFactory()

        client = self.get_client(user)

        resp = client.patch('/users/%s' % user.id, data={'first_name': '456789'})

        user.refresh_from_db()
        self.assertEqual(user.first_name, resp.data['first_name'], resp.data)

    def test_password_change(self):
        user = factories.StaffUserFactory()
        client = self.get_client(user)
        resp = client.put('/users/%s/actions/change_password' % user.id, data={
            'new_password': 'PeMsOB0evhkf', 'old_password': self.USER_PASSWORD
        })
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT, resp.data)

        resp = client.put('/users/%s/actions/change_password' % user.id, data={
            'new_password': '7k16NZgBoA0P', 'old_password': 'abc'
        })

        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_change_blank(self):
        user = factories.UserFactory()

        response = self.user_client.put('/users/%s/actions/change_password' % user.id, data={
            'new_password': '7k16NZgBoA0P', 'old_password': ''
        })

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_reset_request(self):
        """ Ensures device user can request for password reset """
        user = factories.UserFactory()
        old_pw_reset_key = user.password_reset_key

        resp = self.client.post('/users/actions/password_reset', data={'email': user.email})
        self.assertEqual(resp.status_code, self.status_code.HTTP_204_NO_CONTENT)

        user.refresh_from_db()
        self.assertNotEqual(old_pw_reset_key, user.password_reset_key)
        self.assertEqual(user.is_password_reset, False)

        # with non-exists email
        resp = self.client.post('/users/actions/password_reset',
                                data={'email': 'no@mail.com'})
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND, resp.data)

    def test_password_reset_request_ntimes(self):
        """ Ensures if user tries to request password reset n-times, they should get same key """
        user = factories.UserFactory()

        self.client.post('/users/actions/password_reset', data={'email': user.email})
        user.refresh_from_db()
        old_pw_reset_key = user.password_reset_key

        self.client.post('/users/actions/password_reset', data={'email': user.email})
        user.refresh_from_db()

        self.assertEqual(old_pw_reset_key, user.password_reset_key)

    def test_password_reset(self):
        user = factories.UserFactory()
        data = {'email': user.email,
                'reset_key': user.password_reset_key,
                'new_password': '789'}

        # Lets try to reset password using default key of the user
        resp = self.client.put('/users/actions/password_reset', data=data)
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

        # request a reset now
        self.client.post('/users/actions/password_reset', data={'email': user.email})
        user.refresh_from_db()

        # reset password
        data['reset_key'] = user.password_reset_key
        resp = self.client.put('/users/actions/password_reset', data=data)

        # try to login with new password
        resp = self.client.post('/auth/login',
                                data={'username': user.email, 'password': '789'})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_user_non_editable_field(self):
        """ Ensure user cannot update few fields when updating themselves """
        data = {
            'groups': [],
            'is_active': False,
            'is_superuser': True,
            'first_name': 'test123'
        }

        self.users[1].save()
        client = self.get_client(self.users[1])
        resp = client.patch(self.ENDPOINT + '/{0}'.format(self.users[1].id), data=data)
        self.assertEqual(resp.status_code, self.status_code.HTTP_200_OK, resp.data)
        self.assertEqual(resp.data.get('is_staff'), False)
        self.assertEqual(resp.data.get('is_active'), True)
        self.assertEqual(resp.data.get('is_superuser'), False)
        self.assertEqual(resp.data.get('first_name'), 'test123')

    def test_only_admin_assign_staff_superuser(self):
        """ Ensure only admin can edit/create user with staff/superuser attribute """
        data = factories.RegistrationFactory.build(is_superuser=True, is_staff=True)
        response = self.admin_client.post('/users', data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.data)
        self.assertEqual(response.data.get('is_superuser'), True)
        self.assertEqual(response.data.get('is_staff'), True)
