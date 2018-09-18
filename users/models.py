from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    ip = models.GenericIPAddressField(default="", null=True, blank=True)

    class Meta:
        ordering = ('id', )

    def save(self, *args, **kwargs):
        self.set_password(self.password)
        super(User, self).save(*args, **kwargs)

    def __str__(self):
        return self.username
