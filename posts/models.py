from random import randint

from django.db import models
from users import models as users_models
from communities import models as community_models
from django.utils import timezone, text


class Post(models.Model):
    TYPE_CHOICES = ((0, "INTERNAL"), (1, "EXTERNAL"), (2, "IMG"), (3, "GIF"), (4, "VID"))

    type = models.IntegerField(choices=TYPE_CHOICES, default=0)
    creation_date = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=200, default='', null=False)
    description = models.TextField(default='', null=True, blank=True, max_length=10000)
    votes = models.IntegerField(default=0, null=False)
    locked = models.BooleanField(default=False)
    posted_by = models.ForeignKey(users_models.User, on_delete=models.DO_NOTHING, null=False)
    community = models.ForeignKey(community_models.Community, on_delete=models.DO_NOTHING, null=False)
    url = models.URLField(max_length=2000, null=True, blank=True)
    popularity = models.DecimalField(default=0, max_digits=10, decimal_places=3, null=False)
    comments_count = models.IntegerField(default=0, null=False)
    is_active = models.BooleanField(default=True, null=False)
    slug = models.CharField(max_length=255, default='', null=False, blank=False)
    sticky = models.BooleanField(default=False, null=False)

    class Meta:
        ordering = ('-creation_date', '-votes')

    def __str__(self):
        return self.title

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if self.url:
            extension = self.url.split('.')[-1]
            if 'gif' in extension:
                self.type = 3
            elif extension in ['jpg', 'png', 'jpeg', 'webp', 'bmp', 'exif']:
                self.type = 2
            elif extension in ['mp4', 'webm', 'flv', 'avi', 'mpg', 'gifv']:
                self.type = 4
            else:
                self.type = 1
        self.slug = text.slugify(self.title)+"-"+str(self.pk)
        if self.comments_count > 0:
            hours_passed = (self.creation_date - timezone.now()).total_seconds() * 3600
            self.popularity = self.comments_count/hours_passed
        super(Post, self).save()
