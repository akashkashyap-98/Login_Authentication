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

    # ========= url for studying and implementation of ORM queries =================
    path('orm_implementation/', Orm_Implementation.as_view()),

    # ===== url for function based api=====================================
    path('create_employee/', views.create_employee, name='create_employee'),
    path('get_all_employees/', views.get_all_employees, name='get_all_employees'),
    path('get_employee_by_id/<int:id>/', views.get_employee_by_id, name='get_employee_by_id'),
    path('update_employee_by_id/<int:id>/', views.update_employee_by_id, name='update_employee_by_id'),

    # ===== url for apis for default and second databse=====================
    path('create_student_multiple_db/', views.create_student_multiple_db, name='create_student_multiple_db'),
    path('get_student_multiple_db/', views.get_student_multiple_db, name='get_student_multiple_db'), 
    path('get_student_by_id_multiple_db/<int:id>/', views.get_student_by_id_multiple_db, name='get_student_by_id_multiple_db'), 
    path('update_student_by_id_multiple_db/<int:id>/', views.update_student_by_id_multiple_db, name='update_student_by_id_multiple_db'),
    path('delete_student_by_id_multiple_db/<int:id>/', views.delete_student_by_id_multiple_db, name='delete_student_by_id_multiple_db'),

    # ======== url for Author and Book (Many to Many relation) ===========================================================================
    path('create_book/', BookGetAndPostApi.as_view()),
    path('get_all_books/', BookGetAndPostApi.as_view()),
    path('get_particulat_book/<int:id>/', BookDetailById.as_view()),
    path('update_book/<int:id>/', BookDetailById.as_view()),
    path('delete_book/<int:id>/', BookDetailById.as_view()),
    path('create_author/', AuthorGetAndPost.as_view()),
    path('get_all_authors/', AuthorGetAndPost.as_view()),
    path('get_author_by_id/<int:id>/', AuthorDetailsById.as_view()),
    path('update_author_by_id/<int:id>/', AuthorDetailsById.as_view()),
    path('delete_author_by_id/<int:id>/', AuthorDetailsById.as_view()),

    # ========== get api for ORM implementation for models: University , Department , Student (Foreign Key Relation) ==============================
    path('get_orm_foreignKey_relation/', ForeignKey_ORM.as_view()),

    # ========== url for model 'DeveloperSecondDB' to post the data in second database  ==================
    path('create_developer_second_db/', views.create_developer_second_db, name='create_developer_second_db'),
    path('get_all_developers_second_db/', views.get_all_developers_second_db, name='get_all_developers_second_db'),      
    path('update_developers_second_db/<int:id>/', views.update_developers_second_db, name='update_developers_second_db'),
    path('get_developers_second_db/<int:id>/', views.get_developers_second_db, name='get_developers_second_db'),
    path('delete_developers_second_db/<int:id>/', views.delete_developers_second_db, name='delete_developers_second_db'),

    # =========== url for many to many relation ORM =========================================================
    path('MANY_TO_MANY_ORM/', MANY_TO_MANY_ORM.as_view()),


    # ========== url for Horse model and save image in database =====================================
    path('Create_Horse/', views.Create_Horse, name='Create_Horse'),
    path('get_all_horses/', views.get_all_horses, name='get_all_horses'),  
    path('get_horse_by_id/<int:id>/', views.get_horse_by_id, name='get_horse_by_id'), 
    path('update_Horse/<int:id>/', views.update_Horse, name='update_Horse'), 
    path('delete_horse/<int:id>/', views.delete_horse, name='delete_horse'), 

    # ============= url for Django-Celery ==================================
    path('django_celery_task/', views.test , name="tests"),
    path('send_mail_to_user/', views.send_mail_to_user, name='send_mail_to_user'),
    path('schedulemail/', views.schedule_mail, name='schedulemail'),
    path('schedule_mail_with_attachment/', views.schedule_mail_with_attachment, name='schedule_mail_with_attachment'),  
    
    # ============== urls for dynamic template (questions and answers) ================================
    path('questions/', QuestionList.as_view()), 
    path('QuestionDetail/<int:id>/', QuestionDetail.as_view()),
    path('answers/', AnswerDetail.as_view()),
    path('answers_by_id/<int:id>/', AnswerDetailById.as_view()),
                  
] 


