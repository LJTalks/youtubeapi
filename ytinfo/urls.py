from django.urls import path
from . import views

urlpatterns = [
    # This will render the form at the homepage
    path('', views.fetch_data, name='home'),
    # originl URL
    path('fetch-data/', views.fetch_data, name='fetch_data'),
    ]
