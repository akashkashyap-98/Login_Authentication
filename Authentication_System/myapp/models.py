from django.db import models
from django.core.validators import RegexValidator

# Create your models here.
class Register(models.Model):
    first_name = models.CharField(max_length=50 , null=False , blank=False)
    last_name = models.CharField(max_length=50 , null=False , blank=False)
    username = models.CharField(max_length=50 , null=False , blank=False)
    mobile = models.CharField(
        max_length=10,
        unique=True,
        validators=[
            RegexValidator(
                regex=r'^\d{10}$',
                message='Mobile number must be a 10-digit number',
            ),
        ],
        help_text='Enter your 10-digit mobile number',
    )
    email = models.EmailField(null=False, blank=False , unique=True)
    password = models.CharField(max_length=50, null=False, blank=False )
    confirm_password = models.CharField(max_length=50, null=False, blank=False)
    OTP = models.CharField(max_length=10 , null=True , blank=True)
    
    
    def __str__(self):
        return self.email

class Login(models.Model):
    email = models.EmailField(null=False, blank=False , unique=True)
    password = models.CharField(max_length=50, null=False, blank=False )
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.email 

# ================ creating model Emoloyee for function based api==================================================

class Employee(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(null=True, blank=True , unique=True)
    designation = models.CharField(max_length=100)
    salary = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name
    
# ================= creating student model for default and second databse ===============================================

class StudentDefaultDB(models.Model):
    full_name = models.CharField(max_length=100)
    email = models.EmailField(null=True, blank=True , unique=True)
    school = models.CharField(max_length=100)
    city = models.CharField(max_length=100)

    def __str__(self):
        return self.email

class StudentSecondDB(models.Model):
    full_name = models.CharField(max_length=100)
    email = models.EmailField(null=True, blank=True , unique=True)
    school = models.CharField(max_length=100)
    city = models.CharField(max_length=100)

    def __str__(self):
        return self.email