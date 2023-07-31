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

admin.site.register(Register, RegisterAdmin)
admin.site.register(Login, LoginAdmin)
admin.site.register(Employee, EmployeeAdmin )
admin.site.register(StudentDefaultDB, StudentDefaultDB_Admin)
admin.site.register(StudentSecondDB, StudentSecondDB_Admin)
admin.site.register(Author)
admin.site.register(Book)