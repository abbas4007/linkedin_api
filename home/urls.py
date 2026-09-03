from django.urls import path
from .views import search_profiles,HomeView

app_name = 'home'

urlpatterns = [
    path('api/search/', search_profiles, name='search'),
    path('', HomeView.as_view(), name='home'),
]