from django.db import models
# from djongo import models
from django.contrib.auth.models import User
from .validators import validate_audio_file_extension, validate_image_file_extension

from django.conf import settings
from djongo.storage import GridFSStorage
from django.db.models.signals import post_save
from django.dispatch import receiver

from datetime import datetime
import django

# Define your GrifFSStorage instance
grid_fs_storage = GridFSStorage(collection='myfiles', base_url=''.join([settings.BASE_URL, 'myfiles/']))

# Create your models here.
class Country(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class City(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Profile(models.Model):
    # This model is extended from the default User model, it deals with data outside of authentication
    # default user model attributes:
        # username
        # password
        # email  
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True)
    avatar = models.ImageField(upload_to='avatars', storage=grid_fs_storage, null=True, validators=[validate_image_file_extension])

class AudioMessage(models.Model):
    managed = True
    audio_data = models.FileField(upload_to='messages', storage=grid_fs_storage, null=True, validators=[validate_audio_file_extension])
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    upload_time = models.DateTimeField(default=django.utils.timezone.now)

@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()