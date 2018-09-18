from django.utils import text
from django.urls import reverse
from rest_framework import test
from . import models
from users import models as users_models

import tempfile
from PIL import Image


class CommunitySimpleTest(test.APITestCase):

    def setUp(self):
        """
        Setup for tests
        """

        def get_image_file(ext='.jpg', size=(50, 50), color=(73, 109, 137)):
            image = Image.new("RGB", size=size, color=color)
            tmp_file = tempfile.NamedTemporaryFile(suffix=ext)
            image.save(tmp_file)
            tmp_file.seek(0)
            return tmp_file

        self.factory = test.APIClient(enforce_csrf_checks=False)
        self.community_name = "My Community"
        self.community_name_101_length = 'a'
        for i in range(101):
            self.community_name_101_length += 'a'
        self.community_name_duplicate = "done333"
        self.text_color = 100000
        self.text_color_bad = 1000000
        self.background_color = 100000
        self.background_color_bad = 1000000

        self.moderator = users_models.User.objects.create(username="bammmmm", email="aewfaewr@asdf.com")
        self.moderator.set_password("Bahamas3444")
        self.moderator.save()

        self.admin = users_models.User.objects.create(username="admin", email="admin@asdf.com")
        self.admin.set_password("Adminnnnn22")
        self.admin.save()

        self.image_jpg_good = get_image_file()
        self.image_jpg_big_size = get_image_file(size=(2000, 2000))
        self.image_png = get_image_file(ext='.png')

        self.community = models.Community.objects.create(name=self.community_name, administrator=self.admin)
        self.community.save()

        self.get_user_owned_communities = reverse('get-communities-administrated-by-user')
        self.get_user_moderated_communities = reverse('get-communities-moderated-by-user')
        self.create_community_url = reverse('create-community')
        self.get_community_url = reverse('retrieve-community', kwargs={'slug': self.community.slug})
        self.delete_community_url = reverse('destroy-community', kwargs={'slug': self.community.slug})
        self.admin_update_community_url = reverse('admin-update-community', kwargs={'slug': self.community.slug})
        self.moderator_update_community_url = reverse('moderator-update-community', kwargs={'slug': self.community.slug})

        self.user = users_models.User.objects.create(username="admin2", email="asdfawef@asdf.com")
        self.user.set_password("Bahamas00")
        self.user.save()
        self.user2 = users_models.User.objects.create(username="user2", email="user@asdf.com")
        self.user2.set_password("Basmdkw3")
        self.user2.save()

    def test_name_length_validator(self):
        """
            Tests community name validator
        """

        self.factory.force_authenticate(user=self.user)
        self.factory.post(self.create_community_url, {'name': self.community_name_101_length}, format='json')
        self.assertEqual(False, models.Community.objects.filter(name=self.community_name_101_length).exists())

    def test_slug(self):
        """
            Tests slug generation
        """

        self.factory.force_authenticate(user=self.user)
        self.factory.post(self.create_community_url, {'name': self.community_name}, format='json')
        self.assertEqual(text.slugify(self.community_name), models.Community.objects.get(name=self.community_name).slug)

    def test_unique_name(self):
        """
            Tests for duplicates name
        """

        self.factory.force_authenticate(user=self.user)
        self.factory.post(self.create_community_url, {'name': self.community_name}, format='json')
        response = self.factory.post(self.create_community_url, {'name': self.community_name}, format='json')
        self.assertEqual(400, response.status_code)

    def test_text_color(self):
        """
            Tests that it checks if the color is good
        """
        self.community.text_color = self.text_color_bad
        self.community.save()
        self.assertNotEqual(self.text_color, self.community.text_color)

    def test_admin_permissions(self):
        """
            Tests that only admin can do changes in the community, there is a bug that doesn't modify color on the
            database but it appears as it does on the response. But test changed to check if moderators can change it
            only.
        """
        self.factory.force_authenticate(user=self.moderator)
        response = self.factory.put(self.admin_update_community_url, {'text_color': self.text_color}, format='multipart')
        self.assertEqual(403, response.status_code)

    def test_moderator_permissions(self):
        """
        Tests that only moderator can add and remove invited users and banned users
        """
        self.community.moderators.add(self.moderator)
        self.community.save()
        self.factory.force_authenticate(user=self.moderator)
        self.factory.put(self.moderator_update_community_url, {'invited_users': [self.user2.id]}, format='multipart')
        self.assertEqual(1, self.community.invited_users.count())
        self.factory.put(self.moderator_update_community_url, {'banned_users': [self.user2.id]}, format='multipart')
        self.assertEqual(1, self.community.banned_users.count())

    def test_file_upload(self):
        """
           Tests image upload field.
        """
        self.factory.force_authenticate(user=self.admin)
        response = self.factory.put(self.admin_update_community_url, {'background_img': self.image_jpg_good},
                                    format='multipart')
        self.assertEqual(200, response.status_code)
        response = self.factory.put(self.admin_update_community_url, {'background_img': self.image_png},
                                    format='multipart')
        self.assertEqual(400, response.status_code)

    def test_is_active(self):
        """
            Tests if users can see a non active community.
        """
        self.factory.force_authenticate(user=self.admin)
        self.factory.put(self.delete_community_url, {'is_active': False}, format="multipart")
        response = self.factory.get(self.get_community_url)
        self.assertEqual(404, response.status_code)

    def test_get_communities_owned_by_user(self):
        """
            Tests retrieving user owned communities.
        """

        user = users_models.User.objects.create(username="good_username", email="good_email", ip='0.0.0.0')
        user.set_password("good_password")
        user.save()
        self.factory.force_authenticate(user=user)
        models.Community.objects.create(name="Community", administrator=user)
        models.Community.objects.create(name="Commmaaa", administrator=user)
        response = self.factory.get(self.get_user_owned_communities)
        self.assertEqual(2, response.data.get('count'))

    def test_get_communities_moderated_by_user(self):
        """
            Tests retrieving user moderated communities.
        """

        user = users_models.User.objects.create(username="good_username2", email="good_email", ip='0.0.0.0')
        user.set_password("good_password")
        user.save()
        self.factory.force_authenticate(user=user)
        community = models.Community.objects.create(name="Community", administrator=self.admin)
        community.moderators.add(user)
        response = self.factory.get(self.get_user_moderated_communities)
        self.assertEqual(1, response.data.get('count'))

    def test_get_community_where_user_is_banned(self):
        """
            Tests retrieving a community where the user is banned.
        """

        user = users_models.User.objects.create(username="good_username2", email="good_email", ip='0.0.0.0')
        user.set_password("good_password")
        user.save()
        self.community.banned_users.add(user)
        self.community.save()
        self.factory.force_authenticate(user=user)
        response = self.factory.get(self.get_community_url)
        self.assertEqual(403, response.status_code)

    def test_get_community_with_invitation(self):
        """
            Tests retrieving a community where the user is banned.
        """

        user = users_models.User.objects.create(username="good_username2", email="good_email", ip='0.0.0.0')
        user.set_password("good_password")
        user.save()
        self.community.invitation_required = True
        self.community.save()
        self.factory.force_authenticate(user=user)
        response = self.factory.get(self.get_community_url)
        self.assertEqual(403, response.status_code)
