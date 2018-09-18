from django.db import models
from users import models as users_models
from posts import models as posts_models


class Comment(models.Model):
    posted_by = models.ForeignKey(users_models.User, on_delete=models.CASCADE)
    comment = models.TextField(default='', null=True, blank=True, max_length=10000)
    votes = models.IntegerField(default=0, null=False)
    is_active = models.BooleanField(default=True, null=False)
    post = models.ForeignKey(posts_models.Post, on_delete=models.CASCADE)
    sticky = models.BooleanField(default=False, null=False)
    creation_date = models.DateTimeField(auto_now_add=True)
    parent_id = models.IntegerField(default=-1, null=True)

    class Meta:
        ordering = ('-votes', '-creation_date')

    def __str__(self):
        return self.comment
