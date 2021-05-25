from django import forms
# from djongo import forms
from django.contrib.auth.models import User
from django.forms import widgets
from django.forms.fields import DateTimeField
from socialvoiceapp.models import Profile, City, Country, AudioMessage


#
class UserForm(forms.ModelForm):
    # first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    # last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    # email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password')


class ProfileCreationForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['country', 'city']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['city'].queryset = City.objects.none()

        if 'country' in self.data:
            try:
                country_id = int(self.data.get('country'))
                self.fields['city'].queryset = City.objects.filter(country_id=country_id).order_by('name')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            self.fields['city'].queryset = self.instance.country.city_set.order_by('name')

class AddAudioMessageForm(forms.ModelForm):
    class Meta:
        model = AudioMessage
        fields = ['audio_data', 'user']
        widgets = {'user': forms.HiddenInput()}

class DeleteAudioMessageForm(forms.ModelForm):
    class Meta:
        model = AudioMessage
        fields = []