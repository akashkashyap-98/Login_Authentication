from django.contrib import admin
from django.urls import path , include
from myapp.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', RegisterUserPostAndGet.as_view()),
    path('user/<int:id>/' , RegisterUserDetailById.as_view()),
    path('login/', LoginUserPostAndGet.as_view()),
    # path('logout/', LogoutUserPost.as_view()),
]