from django.urls import reverse
from rest_framework import test
from . import models


class UsersTest(test.APITestCase):

    def setUp(self):
        self.factory = test.APIClient(enforce_csrf_checks=False)
        self.good_username = "123000"
        self.good_password = "Password123"
        self.good_email = "goodemail@gmail.com"
        self.bad_username = "a"
        self.bad_password = "a"
        self.bad_email = "a"
        self.create_path = reverse('create-user-profile')
        self.get_profile = reverse('get-user-profile')

    def test_create_good_user(self):
        """
            Tests creation of an user.
        """
        response = self.factory.post(self.create_path, {'username': self.good_username, 'email': self.good_email,
                                                       'password': self.good_password}, format='json')
        self.assertEqual(201, response.status_code)

    def test_email_validator(self):
        """
            Tests email validator
        """

        response = self.factory.post(self.create_path, {'username': self.good_username, 'email': self.bad_email,
                                                       'password': self.good_password}, format='json')
        self.assertEqual(400, response.status_code)

    def test_username_validator(self):
        """
            Tests username validator
        """

        user = models.User.objects.create(username=self.good_username, email=self.good_email, ip='0.0.0.0')
        user.set_password(self.good_password)
        user.save()
        response = self.factory.post(self.create_path, {'username': self.good_username, 'email': self.good_email,
                                                           'password': self.good_password}, format='json')
        self.assertEqual(400, response.status_code)

    def test_password_validator(self):
        """
            Tests password validator
        """

        response = self.factory.post(self.create_path, {'username': self.good_username, 'email': self.good_email,
                                                       'password': self.bad_password}, format='json')
        self.assertEqual(400, response.status_code)

    def test_get_user(self):
        """
            Tests getting user information
        """
        user = models.User.objects.create(username=self.good_username, email=self.good_email, ip='0.0.0.0')
        user.set_password(self.good_password)
        user.save()
        self.factory.force_authenticate(user=user)
        response = self.factory.get(self.get_profile)
        self.assertEqual(200, response.status_code)
        self.factory.force_authenticate(user=None)
        response = self.factory.get(self.get_profile)
        self.assertEqual(403, response.status_code)



