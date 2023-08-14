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
    


# ================= creating models Author and Books for Many to Many Relationships =================================================

# Retrieve all books and their authors as a dictionary-like data
# books_with_authors_data = Book.objects.values('title', 'release_date', 'authors__name')

class Book(models.Model):

	title = models.CharField(max_length=100, null=True, blank=True)
	description = models.CharField(max_length=500, null=True, blank=True)
	publisher = models.CharField(max_length=200, null=True, blank=True)
	release_date = models.DateField()

class Author(models.Model):
	name = models.CharField(max_length=100, null=True, blank=True)
	biography = models.TextField(null=True, blank=True)
	date_of_birth = models.DateField()
	books = models.ManyToManyField(Book, related_name='author_book' , blank=True)
        
# ====================  creating model for FOREIGN KEY RELATION  for implementing ORM Query ===================================


class University(models.Model):
    university_name = models.CharField(max_length=100)

    def __str__(self):
        return self.university_name
    
class Department(models.Model):
    department_name = models.CharField(max_length=100)
    university = models.ForeignKey(University, on_delete=models.CASCADE, related_name='departments')

    def __str__(self):
        return self.department_name

class Student(models.Model):
    student_name = models.CharField(max_length=100)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='students')

    def __str__(self):
        return self.student_name
    

# ======================== creating models for MULTIPLE DTABASE ==================================

class DeveloperDefaultDB(models.Model):
    full_name = models.CharField(max_length=100)
    email = models.EmailField(null=True, blank=True , unique=True)
    organization  = models.CharField(max_length=100)
    city = models.CharField(max_length=100)

    def __str__(self):
        return self.email


class DeveloperSecondDB(models.Model):
    full_name = models.CharField(max_length=100)
    email = models.EmailField(null=True, blank=True , unique=True)
    organization = models.CharField(max_length=100)
    city = models.CharField(max_length=100)

    def __str__(self):
        return self.email


# ============================= model for HORSE IMAGE================================================


class Horse(models.Model):
	
	name=models.CharField(max_length=50, null=True, blank=True)
	age = models.PositiveIntegerField(null=True, blank=True)
	profile_image=models.ImageField(null=True , blank=True)
	is_favourite=models.BooleanField(null=True , blank=True)
	created_at = models.DateField(auto_now_add = True)
	updated_at = models.DateField(auto_now = True)
        
    # ---OVERRIDING THE DELETE FUNCTION----this will delete the model and its realted files from databse also-----
	def delete(self, *args, **kwargs):
		# You have to prepare what you need before delete the model
		storage, path = self.profile_image.storage, self.profile_image.path
		# Delete the model before the file
		super(Horse, self).delete(*args, **kwargs)
		# Delete the file after the model
		storage.delete(path)




