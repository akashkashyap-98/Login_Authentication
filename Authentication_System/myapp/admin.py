from django.contrib import admin
from .models import*
# Register your models here.

class RegisterAdmin(admin.ModelAdmin):
    list_display = ('email', 'username', 'mobile')

class LoginAdmin(admin.ModelAdmin):
    list_display = ('email', 'is_active')
    
class EmployeeAdmin(admin.ModelAdmin):
    list_display =  ('name', 'designation', 'salary')

class StudentDefaultDB_Admin(admin.ModelAdmin):
    list_display =  ('full_name', 'email', 'city')

class StudentSecondDB_Admin(admin.ModelAdmin):
    list_display =  ('full_name', 'email', 'city')

class University_Admin(admin.ModelAdmin):
    list_display =  ('id', 'university_name')

class Department_Admin(admin.ModelAdmin):
    list_display =  ('id', 'department_name', 'university')

class Student_Admin(admin.ModelAdmin):
    list_display =  ('id', 'student_name', 'department')

class DeveloperDefaultDB_Admin(admin.ModelAdmin):
    list_display =  ('id', 'full_name', 'email', 'organization', 'city')

class DeveloperSecondDB_Admin(admin.ModelAdmin):
    list_display =  ('id',  'full_name', 'email', 'organization', 'city')

class Horse_Admin(admin.ModelAdmin):
    list_display =  ('id',  'name', 'created_at', 'updated_at')

class Question_Admin(admin.ModelAdmin):
    list_display =  ('id',  'text')

class Answer_Admin(admin.ModelAdmin):
    list_display = ('question', 'text')

admin.site.register(Register, RegisterAdmin)
admin.site.register(Login, LoginAdmin)
admin.site.register(Employee, EmployeeAdmin )
admin.site.register(StudentDefaultDB, StudentDefaultDB_Admin)
admin.site.register(StudentSecondDB, StudentSecondDB_Admin)
admin.site.register(Author)
admin.site.register(Book)
admin.site.register(University, University_Admin)
admin.site.register(Department, Department_Admin)
admin.site.register(Student, Student_Admin)
admin.site.register(DeveloperDefaultDB, DeveloperDefaultDB_Admin)
admin.site.register(DeveloperSecondDB, DeveloperSecondDB_Admin)
admin.site.register(Horse, Horse_Admin)
admin.site.register(Question, Question_Admin)
admin.site.register(Answer, Answer_Admin)

