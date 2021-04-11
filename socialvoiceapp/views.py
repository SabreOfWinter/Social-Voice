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
    context = {

    }
    return render(request, 'feed.html', context=context)