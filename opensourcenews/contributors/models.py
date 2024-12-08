from django.db import models
from django.contrib.auth.models import User
from django.utils.text import Truncator
from django.utils.text import slugify


# Create your models here.
class Journalist(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='journalists/', blank=True, null=True)

    def __str__(self):
        return self.user.username