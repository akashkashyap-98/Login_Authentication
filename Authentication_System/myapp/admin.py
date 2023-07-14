from django.contrib import admin
from .models import*
# Register your models here.

class RegisterAdmin(admin.ModelAdmin):
    list_display = ('email', 'username', 'mobile')

admin.site.register(Register, RegisterAdmin)
admin.site.register(Login)
