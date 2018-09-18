from django.urls import reverse
from rest_framework import test
from . import models
from users import models as users_models
from posts import models as posts_models
from communities import models as community_models


class CommentsApiTest(test.APITestCase):

    def setUp(self):
        """
            Setup for tests.
        """
        self.factory = test.APIClient(enforce_csrf_checks=False)
        self.user = users_models.User.objects.create(username="testttt")
        self.user.set_password("aiwjhriuh23")
        self.user.save()
        self.admin = users_models.User.objects.create(username="testttt2323")
        self.admin.set_password("aiwjhriuh23213")
        self.admin.save()
        self.community = community_models.Community.objects.create(name="ajsfjwehkj", administrator=self.admin)
        self.community.save()
        self.first_post = posts_models.Post.objects.create(title="kjasfhkawje", description="iuhwqe9 89  98",
                                                           community=self.community, posted_by=self.user)
        self.first_post.save()
        self.comment_parent = models.Comment.objects.create(posted_by=self.user, sticky=False, comment="aaaa",
                                                            post=self.first_post)
        self.comment_parent.save()
        self.comment_child = models.Comment.objects.create(posted_by=self.user, sticky=False, comment="aaaa122",
                                                           parent_id=self.comment_parent.pk, post=self.first_post)
        self.comment_child.save()
        self.comment_create_url = reverse('create-comment', kwargs={'slug': self.first_post.slug})
        self.comment_by_post_url = reverse('retrieve-comment-by-post', kwargs={'slug': self.first_post.slug})
        self.comment_delete_url = reverse('delete-comment', kwargs={'id': self.comment_parent.id})
        self.comment_update_url = reverse('update-comment', kwargs={'id': self.comment_parent.id})
        self.child_comment_url = reverse('retrieve-child-comment', kwargs={'slug': self.first_post.slug,
                                                                           'parent_id': self.comment_parent.id})

    def test_comment_create(self):
        """
            Tests comment creation.
        """

        self.factory.force_authenticate(user=self.user)
        response = self.factory.post(self.comment_create_url, {'comment': "asdf", 'sticky': False}, format='json')
        self.assertEqual(201, response.status_code)

    def test_retrieve_comment_by_post(self):
        """
            Tests retrieving comments by post.
        """

        self.factory.force_authenticate(user=self.user)
        response = self.factory.get(self.comment_by_post_url)
        self.assertEqual(1, response.data.get('count'))

    def test_delete_comment(self):
        """
            Tests comment deletion.
        """

        self.factory.force_authenticate(user=self.user)
        response = self.factory.put(self.comment_delete_url, {'is_active': False}, format='json')
        self.assertEqual(200, response.status_code)

    def test_update_comment(self):
        """
            Tests comment update.
        """

        self.factory.force_authenticate(user=self.user)
        response = self.factory.put(self.comment_update_url, {'comment': "bbbb"}, format='json')
        self.assertEqual("bbbb", response.data.get('comment'))

    def test_retrieve_child_comment(self):
        """
            Tests retrieving child comment.
        """

        self.factory.force_authenticate(user=self.user)
        response = self.factory.get(self.child_comment_url)
        self.assertEqual(1, response.data.get('count'))

    def test_comment_permission(self):
        """
            Tests permissions if owner of a comment.
        """

        self.factory.force_authenticate(user=self.admin)
        response = self.factory.put(self.comment_update_url, {'comment': "bbbb"}, format='json')
        self.assertNotEqual("bbbb", response.data.get('comment'))
