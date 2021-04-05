from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    # path('profile/<int:id>', views.ProfileDetailView.as_view(), name='profile'), # wasnt working  -will fix later
    path('userprofile', views.profile, name='profile-detail'),


]
