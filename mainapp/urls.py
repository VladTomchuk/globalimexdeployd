from django.urls import path
from .views import *

urlpatterns = [
    path('', index_test, name='index_test'),
]