from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_view, name='index'),
    # path('profile/<int:id>', views.ProfileDetailView.as_view(), name='profile'), # wasnt working  -will fix later
    path('userprofile', views.profile_view, name='profile-detail'),
    path('feed', views.feed_view, name='feed'),
]
