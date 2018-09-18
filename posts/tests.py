from django.urls import reverse
from rest_framework import test
from . import models
from users import models as users_models
from communities import models as communities_models


class PostsSimpleTest(test.APITestCase):

    def setUp(self):
        """
        Setup for tests
        """

        self.factory = test.APIClient(enforce_csrf_checks=False)
        self.admin = users_models.User.objects.create(username="itsmymario", is_superuser=True)
        self.admin.set_password("thankyoumario2")
        self.admin.save()
        self.normal_user = users_models.User.objects.create(username="normalUser")
        self.normal_user.set_password("jkhawiu3hr3i2u43")
        self.normal_user.save()
        self.community = communities_models.Community.objects.create(name="hellomellow", administrator=self.admin)
        self.community.save()
        self.first_post = models.Post.objects.create(title="kjasfhkawje", description="iuhwqe9 89  98",
                                                     community=self.community, posted_by=self.normal_user)
        self.second_post = models.Post.objects.create(title="akj", posted_by=self.normal_user, community=self.community,
                                                      description="", url="https://www.test.com/akwje.jpg")
        self.third_post = models.Post.objects.create(title="cc", description="", url="https://www.test.com/akwje.webm",
                                                     community=self.community, posted_by=self.normal_user)
        self.first_post.save()
        self.second_post.save()
        self.third_post.save()
        self.post_list = reverse('retrieve-post-list', kwargs={'community': self.community.slug})
        self.post_individual = reverse('retrieve-post', kwargs={'slug': self.second_post.slug})
        self.post_update = reverse('update-post', kwargs={'slug': self.third_post.slug})
        self.post_create = reverse('create-post', kwargs={'community': self.community.slug})
        self.post_delete = reverse('delete-post', kwargs={'slug': self.third_post.slug})

    def test_retrieve_post_list(self):
        """
            Tests retrieving post list.
        """

        response = self.factory.get(self.post_list)
        self.assertEqual(3, len(response.data.get('results')))

    def test_post_individual(self):
        """
            Tests retrieving individual post.
        """
        response = self.factory.get(self.post_individual)
        self.assertEqual(200, response.status_code)

    def test_post_update(self):
        """
            Tests updating post.
        """

        self.factory.force_authenticate(user=self.normal_user)
        response = self.factory.put(self.post_update, {'description': 'description test message'}, format='json')
        self.assertEqual('description test message', response.data.get('description'))

    def test_post_create(self):
        """
            Tests post creation.
        """

        self.factory.force_authenticate(user=self.normal_user)
        response = self.factory.put(self.post_update, {'title': 'awefawefawe', 'description': 'akjwefhk22',
                                                       'community': self.community.pk,
                                                       'posted_by': self.normal_user.pk}, format='json')
        self.assertEqual(200, response.status_code)

    def test_post_delete(self):
        """
           Tests post deletion.
        """

        self.factory.force_authenticate(user=self.normal_user)
        response = self.factory.put(self.post_delete, {'is_active': False}, format='json')
        self.assertEqual(200, response.status_code)

    def test_post_individual_permission_when_banned(self):
        """
            Tests individual post permissions.
        """

        self.factory.force_authenticate(user=self.normal_user)
        self.community.banned_users.add(self.normal_user)
        self.community.save()
        response = self.factory.get(self.post_individual)
        self.assertEqual(403, response.status_code)

    def test_post_list_permission_when_banned(self):
        """
            Tests post list permissions.
        """

        self.factory.force_authenticate(user=self.normal_user)
        self.community.banned_users.add(self.normal_user)
        self.community.save()
        response = self.factory.get(self.post_list)
        self.assertEqual(0, len(response.data.get('results')))
