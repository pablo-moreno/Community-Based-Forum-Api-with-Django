from django.db import models
from django.utils import text
from rest_framework import exceptions
from users import models as users_models


def img_filename_generator(instance, filename):
    extension = filename.split('.')[-1]
    if extension != 'jpg':
        raise exceptions.ValidationError('You can only upload .jpg files')
    name = instance.name
    return 'media/communities/'+name+'.'+extension


def file_size_validator(file):
    limit = 2 * 1024 * 1024
    if file.size > limit:
        raise exceptions.ValidationError('Maximum file size limit is 2MB')


class Community(models.Model):
    """
        Community model.
    """

    name = models.CharField(max_length=100, null=False, unique=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    invitation_required = models.BooleanField(default=False)
    adult = models.BooleanField(default=False)
    text_color = models.PositiveSmallIntegerField(default=0)
    background_color = models.PositiveSmallIntegerField(default=0)
    background_img = models.ImageField(upload_to=img_filename_generator, validators=[file_size_validator], null=True,
                                       blank=True)
    banned_users = models.ManyToManyField(users_models.User, related_name='banned_users', blank=True)
    invited_users = models.ManyToManyField(users_models.User, related_name='invited_users', blank=True)
    moderators = models.ManyToManyField(users_models.User, related_name='community_moderators', blank=True)
    administrator = models.ForeignKey(users_models.User, on_delete=models.DO_NOTHING, default='')
    slug = models.SlugField(max_length=100, default='', null=False, blank=False, unique=True)

    class Meta:
        ordering = ('id', )

    def __str__(self):
        return self.name

    def is_moderator(self, user):
        return self.moderators.filter(id=user.id).exists()

    def is_administrator(self, user):
        return self.administrator == user

    def save(self, *args, **kwargs):
        self.slug = text.slugify(self.name)
        self.name = self.name.title()
        super(Community, self).save()
