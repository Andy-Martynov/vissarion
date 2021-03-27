from django.db import models

from django.contrib.auth.models import User

# user_images = 'account/images/'

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    token = models.IntegerField(default=0)


