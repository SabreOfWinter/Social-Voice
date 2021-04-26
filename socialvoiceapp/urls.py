from django.urls import include, path
from . import views

urlpatterns = [
    path('', views.index_view, name='index'),
    # path('profile/<int:id>', views.ProfileDetailView.as_view(), name='profile'), # wasnt working  -will fix later
    path('userprofile', views.profile_view, name='profile-detail'),
    path('feed', views.feed_view, name='feed'),
    # path('register', views.profile_create_view, name='register'),
    path('register', views.create_user_view, name='register'),

    path('ajax/load-cities/', views.load_cities, name='ajax_load_cities'), # AJAX

]
