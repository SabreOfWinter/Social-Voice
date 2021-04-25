from django.contrib import admin
from .models import Country, City, Profile, AudioMessage

# Register your models here.
admin.site.register(Country)

@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('name', 'country')

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'city', 'country')
    list_filter = ('city', 'country')

@admin.register(AudioMessage)
class AudioMessageAdmin(admin.ModelAdmin):
    list_display = ('user', 'audio_data')
