from django.contrib import admin
from django.urls import path , include
from myapp.views import *
from myapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', RegisterUserPostAndGet.as_view()),
    path('user/<int:id>/' , RegisterUserDetailById.as_view()),
    path('login/', LoginUserPostAndGet.as_view()),
    path('login_response/', LoginResponsePage.as_view()),
    path('logout/', Logout.as_view()),
    path('orm_implementation/', Orm_Implementation.as_view()),

    # ===== url for function based api=====================================
    path('create_employee/', views.create_employee, name='create_employee'),
    path('get_all_employees/', views.get_all_employees, name='get_all_employees'),
    path('get_employee_by_id/<int:id>/', views.get_employee_by_id, name='get_employee_by_id'),
    path('update_employee_by_id/<int:id>/', views.update_employee_by_id, name='update_employee_by_id'),

    # ===== url for apis for default and second databse=====================
    path('create_student_multiple_db/', views.create_student_multiple_db, name='create_student_multiple_db'),
]