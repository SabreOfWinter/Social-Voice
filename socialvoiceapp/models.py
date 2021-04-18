from django.db import models
from django.contrib.auth.models import User
from .validators import validate_file_extension, validate_image_file_extension

from django.conf import settings
from djongo.storage import GridFSStorage

# Define your GrifFSStorage instance 
grid_fs_storage = GridFSStorage(collection='myfiles', base_url=''.join(['./', 'myfiles/']))

# def validate_file_extension(value):
#     import os
#     from django.core.exceptions import ValidationError
#     ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
#     valid_extensions = ['.mp3']
#     if not ext.lower() in valid_extensions:
#         raise ValidationError('Unsupported file extension.')

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
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True)
    avatar = models.ImageField(upload_to='avatars', storage=grid_fs_storage, null=True, validators=[validate_image_file_extension])
#     # avatar = models.ImageField(upload_to='avatars', height_field=128, width_field=128)

# class AudioMessage(models.Model):
#     # audio_data = models.FileField(upload_to='messages', validators=[validate_file_extension])
#     audio_data = models.CharField(max_length=2)
# class Thread(models.Model):
#     creation_timestamp = models.DateTimeField(auto_now_add=True)
#     user = models.ForeignKey(Profile, on_delete=models.CASCADE) #User who created the thread
#     message = models.OneToOneField(AudioMessage, on_delete=models.CASCADE) #Messaging that starts the topic being discussed

# class ThreadMessage(models.Model):
#     creation_timestamp = models.DateTimeField(auto_now_add=True) #Time and date created
#     user = models.ForeignKey(Profile, on_delete=models.CASCADE) #User who created the message
#     thread_posted_to = models.ForeignKey(Thread, on_delete=models.CASCADE) #Thread the user commented on
#     message = models.OneToOneField(AudioMessage, on_delete=models.CASCADE)