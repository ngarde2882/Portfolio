from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='poll-home'),
    path('results/', views.results, name='poll-results'),
]
