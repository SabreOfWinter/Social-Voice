# from socialvoiceapp.models import
from django.shortcuts import render
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required, permission_required
from django.http import JsonResponse, HttpResponse
import datetime
from datetime import date, timedelta
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import FormView,TemplateView
from django.contrib.auth.models import User
from django.views.generic import ListView, CreateView, UpdateView
from django.urls import reverse_lazy
from socialvoiceapp.models import Profile, Country, City, AudioMessage

from pymongo import MongoClient
import gridfs
from gridfs import GridFS 
from bson import ObjectId

# Create your views here.
#@login_required
def index_view(request):
    """View function for home page of site."""

    context = {

    }

    if request.user.is_authenticated :
        # Redirect to a success page.
        return render(request, 'feed.html', context=context)
    else:
        # Return an 'invalid login' error message.
        return render(request, 'index.html', context=context)
#
# class ProfileCreateView(CreateView):
#     model = Profile
#     # template_name = 'profile_form.html'
#     fields = ( 'country', 'city')
#     success_url = reverse_lazy('feed')


# will change to class based view
@login_required
def profile_view(request):
    context = {

    }

    return render(request, 'user_profile.html', context=context)

# class ProfileDetailView(LoginRequiredMixin, generic.DetailView):
#     model = User



@login_required
def feed_view(request):
    client = MongoClient('mongo', 27017, username='root', password='mongoadmin')
    db = client['socialvoice']

    avatar_fs = gridfs.GridFS(db, collection='myfiles.avatars')
    audio_fs = gridfs.GridFS(db, collection='myfiles.messages')

    user_coll = db['socialvoiceapp_profile']
    auth_user_coll = db['auth_user']

    context = {

    }
    return render(request, 'feed.html', context=context)




from django.shortcuts import render, redirect, get_object_or_404

from .forms import ProfileCreationForm, UserForm

from django.db import transaction

@transaction.atomic
def create_user_view(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = ProfileCreationForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.refresh_from_db()  # This will load the Profile created by the Signal
            profile_form = ProfileCreationForm(request.POST, instance=user.profile)  # Reload the profile form with the profile instance
            profile_form.full_clean()  # Manually clean the form this time. It is implicitly called by "is_valid()" method
            profile_form.save()  # Gracefully save the form
    else:
        user_form = UserForm()
        profile_form = ProfileCreationForm()
    return render(request, 'socialvoiceapp/register.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })


# def profile_create_view(request):
#     form = ProfileCreationForm()
#     if request.method == 'POST':
#         form = ProfileCreationForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('register')
#     return render(request, 'socialvoiceapp/register.html', {'form': form})
#



# AJAX
def load_cities(request):
    country_id = request.GET.get('country_id')
    cities = City.objects.filter(country_id=country_id).all()
    return render(request, 'socialvoiceapp/city_dropdown_list_options.html', {'cities': cities})
    # return JsonResponse(list(cities.values('id', 'name')), safe=False)
