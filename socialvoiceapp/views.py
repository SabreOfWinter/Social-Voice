# from socialvoiceapp.models import
from django.shortcuts import render
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required, permission_required
from django.http import JsonResponse, HttpResponse
from datetime import datetime
from datetime import date, timedelta
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import FormView,TemplateView
from django.contrib.auth.models import User
from django.views.generic import ListView, CreateView, UpdateView
from django.urls import reverse_lazy
from socialvoiceapp.models import Profile, Country, City, AudioMessage
from .forms import AddAudioMessageForm, DeleteAudioMessageForm, ProfileUpdateForm

from .forms import ProfileCreationForm, UserForm

from django.db import transaction
from pymongo import MongoClient
import gridfs
from gridfs import GridFS
from bson import ObjectId
import os

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
    user = Profile.objects.get(user=request.user.id)
    client = MongoClient('mongo', 27017, username='root', password='mongoadmin')
    db = client['socialvoice']

    audio_coll = db['socialvoiceapp_audiomessage']
    audio_messages = audio_coll.find(
        {'user_id': request.user.id}
    ).sort('upload_time', -1)

    messages = []
    for i in range(int(audio_messages.count())):
        messages.append({
        'id': audio_messages[i]['_id'],
        'audio_data': audio_messages[i]['audio_data'],
        'user_id': audio_messages[i]['user_id'],
        'upload_time': audio_messages[i]['upload_time'],
        'audio_id': audio_messages[i]['audio_data'].split('/')[1].split('.')[0]
        })

    addform = AddAudioMessageForm(request.POST, request.FILES, initial = {'user': request.user.id}) # Load the add audio form, with the user field initalized as the logged in user
    addform.fields['audio_data'].label = 'Audio' # Changes the audio field name in the form
    addform.fields['user'].disabled = True # The user input is selected by default as the current logged in user, no changes should be allowed

    deleteform = DeleteAudioMessageForm(request.POST, request.FILES)

    if request.method == "POST" and request.POST['action'] == 'Yes':
        audio_files_coll = db['myfiles.messages.files']
        audio_chuncks_coll = db['myfiles.messages.chunks']

        #Delete all chuncks with matching files_id to files id
        file_name = str(request.POST['pk']).split('/')[1]
        file_id = audio_files_coll.find_one({'filename': file_name})['_id']
        audio_chuncks_coll.delete_many({'files_id': file_id})


        #Delete all files with matching filename to audio message
        audio_files_coll.delete_many({'filename': file_name})

        #Delete audio message with id matching pk
        audio_coll.delete_one({'audio_data': request.POST['pk']})

        return HttpResponseRedirect('')

    #Build avatar
    avatar_fs = gridfs.GridFS(db, collection='myfiles.avatars')

    avatar_file_name = user.avatar.name.split('/')[1]  #Split the avatar url to get the file name to be used in query for the avatar files
    meta = avatar_fs.get_version(filename=avatar_file_name) #Gets file details using filename from profile
    avatar_bucket = gridfs.GridFSBucket(db, bucket_name='myfiles.avatars')
    avatar_file = open('socialvoiceapp/static/'+ user.avatar.name, 'wb')  #Write to file
    avatar_bucket.download_to_stream(file_id=meta._id, destination=avatar_file) #Download file to static folder
    avatar_file.close()

    #Update user details
    updateUserForm = ProfileUpdateForm(request.POST, request.FILES)#, initial={'country': user.country, 'city': user.city})

    if request.method == 'POST':
        #Add audio
        if request.POST['action'] == 'Upload':
            if addform.is_valid(): # Only allows for audio to be saved if valid audio file is uploaded
                addform.save()
                return HttpResponseRedirect('')
            #Update User Profile details
        elif request.POST['action'] == 'Update':
            if updateUserForm.is_valid():
                new_country = int(request.POST['country'])
                new_city = int(request.POST['city'])
                profiles_coll = db['socialvoiceapp_profile']
                #Try to 
                
                try:
                    if request.FILES['avatar']:
                        avatar = request.FILES['avatar']

                        avatar_files_coll = db['myfiles.avatars.files']
                        avatar_chuncks_coll = db['myfiles.avatars.chunks']

                        file_name=user.avatar.name.split('/')[1]
                        if not file_name.startswith("default"):
                            #Delete all chuncks with matching files_id to files id
                            file_id = avatar_files_coll.find_one({'filename': file_name})['_id']
                            avatar_chuncks_coll.delete_many({'files_id': file_id})
                            
                        
                            avatar_files_coll.delete_many({'filename': file_name})

                        profiles_coll.update_one(
                            {'user_id': user.user_id}, #Filter
                            {'$set': {'country_id': new_country, 'city_id': new_city, 'avatar': str('avatars/' + str(request.user) + str( avatar.name))}} #Update data                    
                        )
                        
                        #CREATE NEW DOCUMENT FOR IMAGE
                        avatar_fs.put(avatar, filename=str(str(request.user) + str(avatar.name)), contentType=avatar.content_type)
                        
                except:
                    if request.POST['avatar'] == '':
                        profiles_coll.update_one(
                            {'user_id': user.user_id}, #Filter
                            {'$set': {'country_id': new_country, 'city_id': new_city}} #Update data                    
                    )
                    

    context = {
        'profile': user,
        'messages': messages,
        'addAudioForm': addform,
        'deleteAudioForm': deleteform,
        'updateUserForm': updateUserForm
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

    users_ids = user_coll.find({'city_id': Profile.objects.get(user=request.user.id).city_id}, {'user_id', 'avatar'})

    users = []
    ids_to_search = []

    for i in users_ids:
        ids_to_search.append(i['user_id'])

        users.append(
            { 'user':auth_user_coll.find_one(
                        { #Query
                            'id': i['user_id']
                        },
                        { #Fields to get
                            'username','is_active', 'date_joined'
                        }
                    ),
                    'user_id': i['user_id'],
                    'avatar_id': i['avatar']
                }
        )
        print(int(i['user_id']))
        #Build avatar
        if i['avatar'] is '':
            file_name = 'default.png'
            profiles_coll = db['socialvoiceapp_profile']
            profiles_coll.update_one(
                            {'user_id': int(i['user_id'])}, #Filter
                            {'$set': {'avatar': 'avatars/default.png'}} #Update data                    
                    )         

        else:
            file_name = i['avatar'].split('/')[1]  #Split the avatar url to get the file name to be used in query for the avatar files
            meta = avatar_fs.get_version(filename=file_name) #Gets file details using filename from profile
            avatar_bucket = gridfs.GridFSBucket(db, bucket_name='myfiles.avatars')
            avatar_file = open('socialvoiceapp/static/'+i['avatar'], 'wb')  #Write to file
            avatar_bucket.download_to_stream(file_id=meta._id, destination=avatar_file) #Download file to static folder
            avatar_file.close()

    audio_coll = db['socialvoiceapp_audiomessage']
    audio_messages = audio_coll.find(
        {
            'user_id': {"$in": ids_to_search}
        }
    ).sort('upload_time', -1)

    messages = []
    for message in audio_messages:
        messages.append({
            'audio':message,
            'profile': auth_user_coll.find_one(
                {#Query
                    'id': message['user_id']
                },
                {#Fields to get
                    'username', 'is_active', 'date_joined'
                }
            ),
            'avatar': user_coll.find_one(
                {#Query
                    'user_id': message['user_id']
                },
                {#Fields to get
                    'avatar'
                }
            )

        })
        #Build audio
        file_name = message['audio_data'].split('/')[1]  #Split the audio url to get the file name to be used in query for the message files
        meta = audio_fs.get_version(filename=file_name) #Gets file details using filename from profile
        audio_bucket = gridfs.GridFSBucket(db, bucket_name='myfiles.messages')
        audio_file = open(str('socialvoiceapp/static/messages/'+file_name), 'wb')  #Write to file
        audio_bucket.download_to_stream(file_id=meta._id, destination=audio_file) #Download file to static folder
        audio_file.close()

    #Add audio
    form = AddAudioMessageForm(request.POST, request.FILES, initial = {'user': request.user.id}) # Load the add audio form, with the user field initalized as the logged in user
    form.fields['audio_data'].label = 'Audio' # Changes the audio field name in the form
    form.fields['user'].disabled = True # The user input is selected by default as the current logged in user, no changes should be allowed

    if request.method == 'POST':
        if form.is_valid(): # Only allows for audio to be saved if valid audio file is uploaded
            form.save()
            return HttpResponseRedirect('')

    context = {
        'profile': Profile.objects.get(user=request.user.id),
        'messages': messages,
        'addAudioForm': form
    }
    return render(request, 'feed.html', context=context)



@transaction.atomic
def create_user_view(request):
    user_form = UserForm(request.POST)
    profile_form = ProfileCreationForm(request.POST, request.FILES,initial = {'user': request.user.id})
    if request.method == 'POST':
        #profile_form.avatar = request.FILES['avatar']
        if user_form.is_valid():
            if profile_form.is_valid():
                user = user_form.save()
                # user.set_password(user.password)
                user.refresh_from_db()  # This will load the Profile created by the Signal
                profile_form = ProfileCreationForm(request.POST, instance=user.profile)  # Reload the profile form with the profile instance
                profile_form.full_clean()  # Manually clean the form this time. It is implicitly called by "is_valid()" method
                profile_form.save()  # save the form
                login(request, user)
                return redirect ('index')
                # return HttpResponseRedirect(reverse('login')) #upon successful submission, redirect user to login page.
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
