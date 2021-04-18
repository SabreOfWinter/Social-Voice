from django.contrib import admin
from .models import Country, City, Profile
#, #AudioMessage, Thread, ThreadMessage
# Register your models here.

admin.site.register(Country)
admin.site.register(City)
admin.site.register(Profile)
# admin.site.register(AudioMessage)
# admin.site.register(Thread)
# admin.site.register(ThreadMessage)