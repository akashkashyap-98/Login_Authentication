from django.db import models

# Create your models here.
class Register(models.Model):
    first_name = models.CharField(max_length=50 , null=False , blank=False)
    last_name = models.CharField(max_length=50 , null=False , blank=False)
    username = models.CharField(max_length=50 , null=False , blank=False)
    mobile = models.CharField(max_length=15 , null=False , blank=False)
    email = models.EmailField(null=False, blank=False , unique=True)
    password = models.CharField(max_length=50, null=False, blank=False )
    confirm_password = models.CharField(max_length=50, null=False, blank=False)
    
    
    def __str__(self):
        return self.email

class Login(models.Model):
    email = models.EmailField(null=False, blank=False , unique=True)
    password = models.CharField(max_length=50, null=False, blank=False )





