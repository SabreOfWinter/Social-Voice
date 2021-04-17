from django.contrib import admin
from .models import Profile, Country, City, AudioMessage, Thread, ThreadMessage
# Register your models here.

admin.site.register(Profile)
admin.site.register(Country)
admin.site.register(City)
admin.site.register(AudioMessage)
admin.site.register(Thread)
admin.site.register(ThreadMessage)