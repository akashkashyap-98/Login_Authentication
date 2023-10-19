from rest_framework import serializers
import random
import traceback
from .models import *

class UserCreteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Register
        fields = ['id', 'first_name','last_name', 'username' , 'mobile' , 'email', 'password' ,'confirm_password',]

    def create(self, validated_data):
        instance =  Register.objects.create(**validated_data)

        # --------logic for creating 6 digit random number OTP---------------
        random_number=random.randint(111111,999999)

        # ----- saving the random number in CustomUser table in OTP field---------
        instance.OTP = random_number
        print("----------OTP-------------")
        print(instance.OTP)
        instance.save()

        return instance


class UserUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Register
        fields = ['first_name','last_name', 'password', 'confirm_password' , 'mobile']


    def update(self, instance, validated_data):
        """
        Update and return an existing `Snippet` instance, given the validated data.
        """
        # instance.first_name = validated_data.get('first_name', instance.first_name)
        # instance.last_name = validated_data.get('last_name', instance.last_name)
        # instance.email = validated_data.get('email', instance.email)
        # instance.mobile = validated_data.get('mobile', instance.mobile)
        # instance.role = validated_data.get('role', instance.role)
        # instance.save()
        super().update(instance = instance, validated_data = validated_data)
        return instance  

class UserGetSerializer(serializers.ModelSerializer):
     class Meta:
        model = Register
        fields = ['id', 'first_name','last_name', 'username' , 'mobile' , 'email', 'password' ,'confirm_password']

class LoginUserCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Login
        fields = ['email', 'password']

    def create(self, validated_data):
        return Login.objects.create(**validated_data)

# ==================== creating serializer for function based view ===============================================

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'

class EmployeeUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Employee
        fields = ['name', 'designation', 'salary']

    def update(self, instance, validated_data):
        super().update(instance = instance, validated_data = validated_data)
        return instance
    
# =================== creating serializers for default and second databse =====================================

class StudentDefaultDBSerializer(serializers.ModelSerializer):
    # database = serializers.CharField(max_length=20, default='Demo_db', read_only=True)

    class Meta:
        model = StudentDefaultDB
        fields = ['full_name', 'email', 'school', 'city']

    def create(self, validated_data):
        return StudentDefaultDB.objects.using('default').create(**validated_data)

    # def create(self, validated_data):
    #     # Set the 'database' field to 'Demo_db'
    #     validated_data['database'] = 'Demo_db'
    #     return super().create(validated_data)

class StudentSecondDBSerializer(serializers.ModelSerializer):
    # database = serializers.CharField(max_length=20, default='Demo_db', read_only=True)

    class Meta:
        model = StudentSecondDB
        fields = ['full_name', 'email', 'school', 'city']
    
    def create(self, validated_data):
        return StudentSecondDB.objects.using('second_db').create(**validated_data)
    
class StudentDefaultDB_Get_Serializer(serializers.ModelSerializer):
     class Meta:
        model = StudentDefaultDB
        fields = ['id', 'full_name', 'email', 'school', 'city']

class StudentSecondDB_Get_Serializer(serializers.ModelSerializer):
     class Meta:
        model = StudentSecondDB
        fields = ['id', 'full_name', 'email', 'school', 'city']




class StudentDefaultDB_Update_Serializer(serializers.ModelSerializer):

    class Meta:
        model = StudentDefaultDB
        fields = ['full_name', 'school', 'city']

    def update(self, instance, validated_data):
        super().update(instance = instance, validated_data = validated_data)
        return instance
    
class StudentSecondDB_Update_Serializer(serializers.ModelSerializer):

    class Meta:
        model = StudentSecondDB
        fields = ['full_name', 'school', 'city']

    def update(self, instance, validated_data):
        super().update(instance = instance, validated_data = validated_data)
        return instance


# ------------making serializer for Book Model--------------

class BookCreateSerializer(serializers.ModelSerializer):

	class Meta:
		model=Book
		fields = ['title' , 'description' , 'publisher' , 'release_date'] 
                
	def create(self , validated_data):
		return Book.objects.create(**validated_data)

class BookUpdateSerializer(serializers.ModelSerializer):

	class Meta:
		model=Book
		fields = ['title' , 'description' , 'publisher' , 'release_date'] 

	def update(self,instance , validated_data):
		super().update(instance=instance , validated_data=validated_data)
		return instance

class BookGetSerializer(serializers.ModelSerializer):

	class Meta:
		model=Book
		fields=['id', 'title' , 'description' , 'publisher' , 'release_date'] 

# ----------- making serializer for Author Model ------------------

# class AuthorCreteSerializer(serializers.ModelSerializer):
# 	books = serializers.ListField()
# 	# books=BookCreateSerializer(many=True , read_only=True)



# 	class Meta:
# 		model = Author
# 		fields = [ 'name' ,'biography' , 'date_of_birth' , 'books']
# 		# depth=1  

# 	def create(self, validated_data):
# 		try:
# 			books = validated_data.pop("books", None)
# 			instance =  Author.objects.create(**validated_data)

# 			if books:
# 				# book_objs = Book.objects.filter(id__in=books)
# 				instance.books.add(*Book.objects.filter(id__in=books))
					
# 		except Exception as e:
# 			traceback.print_exc()

# 		return instance


class AuthorCreateSerializer(serializers.ModelSerializer):
    books = serializers.PrimaryKeyRelatedField(queryset=Book.objects.all(), many=True)


    class Meta:
        model = Author
        fields = ['name', 'biography', 'date_of_birth', 'books']

    def create(self, validated_data):
        books_data = validated_data.pop('books')
        print("i am books data ", books_data)
        instance = Author.objects.create(**validated_data)

        for book in books_data:
            instance.books.add(book)

        return instance
    
class AuthorGetSerializer(serializers.ModelSerializer):
     books = BookGetSerializer(many=True)
     
     class Meta:
          model = Author
          fields = ['id', 'name', 'biography', 'date_of_birth', 'books']

class AuthorUpdateSerializer(serializers.ModelSerializer):
     
    class Meta:
        model = Author
        fields = ['name', 'biography', 'date_of_birth', 'books']

    def update(self,instance , validated_data):
        super().update(instance=instance , validated_data=validated_data)
        return instance

# ==================================================================================================


class DeveloperPOST_SecondDBSerializer(serializers.ModelSerializer):
     
    class Meta:
        model = DeveloperSecondDB
        fields = ['full_name', 'email', 'organization', 'city']

    def create(self, validated_data):
        return DeveloperSecondDB.objects.using('second_db').create(**validated_data)
    
class DeveloperGET_SecondDBSerializer(serializers.ModelSerializer):
     
    class Meta:
        model = DeveloperSecondDB
        fields = ['id', 'full_name', 'email', 'organization', 'city']

class developer_UPDATE_serializer(serializers.ModelSerializer):
     
    class Meta:
        model = DeveloperSecondDB
        fields = ['full_name', 'email', 'organization', 'city']

    def update(self,instance , validated_data ):
        super().update(instance=instance, validated_data=validated_data)
        return instance
    

# ========================== making serializer for Horse model ============================================================
class HorseCreteSerializer(serializers.ModelSerializer):

	class Meta:
		model = Horse
		fields = [ 'name', 'age', 'is_favourite', 'profile_image']

	def create(self, validated_data):
		return Horse.objects.create(**validated_data)

class Horse_get_serializer(serializers.ModelSerializer):
     
     class Meta:
        model = Horse
        fields = [ 'id', 'name', 'age', 'is_favourite', 'profile_image', 'created_at', 'updated_at']

class HorseUpdateSerializer(serializers.ModelSerializer):

	class Meta:
		model = Horse
		fields = ['name', 'age','profile_image','is_favourite']


	def update(self, instance, validated_data):

		super().update(instance = instance, validated_data= validated_data)
		return instance  
     

# =========================================================================================



class QuestionSerializer(serializers.ModelSerializer):

    class Meta:
         model = Question
         fields = ['text']

class AnswerSerializer(serializers.ModelSerializer):
    # question = QuestionSerializer()

    class Meta:
        model = Answer
        fields = ['question', 'text']