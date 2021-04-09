from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Country(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class City(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
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
    avatar = models.ImageField(upload_to='avatars', height_field=128, width_field=128)

class AudioMessage(models.Model):
    audio_data = models.FileField(upload_to='messages', validators=[validate_file_extension])

class Thread(models.Model):
    creation_timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE) #User who created the thread
    message = models.OneToOneField(AudioMessage, on_delete=models.CASCADE) #Messaging that starts the topic being discussed

class ThreadMessage(models.Model):
    creation_timestamp = models.DateTimeField(auto_now_add=True) #Time and date created
    user = models.ForeignKey(Profile, on_delete=models.CASCADE) #User who created the message
    thread_posted_to = models.ForeignKey(Thread, on_delete=models.CASCADE) #Thread the user commented on
    message = models.OneToOneField(AudioMessage, on_delete=models.CASCADE)