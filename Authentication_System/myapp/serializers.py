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

# class LogoutUserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Login
#         fileds = [ 'email', 'password' ]






