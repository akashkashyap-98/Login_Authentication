from rest_framework import serializers
import random
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

