from django.contrib import admin
from django.urls import path , include
# from rest_framework.urlpatterns import format_suffix_patterns
from myapp.views import *

urlpatterns = [
    path('register/', RegisterUserPostAndGet.as_view()),

]