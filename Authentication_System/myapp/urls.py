from django.contrib import admin
from django.urls import path , include
# from rest_framework.urlpatterns import format_suffix_patterns
from myapp.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', RegisterUserPostAndGet.as_view()),
    path('user/<int:id>/' , RegisterUserDetailById.as_view()),
]