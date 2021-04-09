from django.contrib import admin
from .models import Profile, Country, City 
# Register your models here.

admin.site.register(Profile)
admin.site.register(Country)
admin.site.register(City)