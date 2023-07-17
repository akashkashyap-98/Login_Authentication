from django.contrib import admin
from .models import*
# Register your models here.

class RegisterAdmin(admin.ModelAdmin):
    list_display = ('email', 'username', 'mobile')

class LoginAdmin(admin.ModelAdmin):
    list_display = ('email', 'is_active')

admin.site.register(Register, RegisterAdmin)
admin.site.register(Login, LoginAdmin)
