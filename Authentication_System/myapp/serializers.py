from rest_framework import serializers

from .models import *

class UserCreteSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        style={'input_type': 'password'}
    )

    class Meta:
        model = Register
        fields = ['id', 'first_name','last_name', 'username' , 'mobile' , 'email', 'password' ,'confirm_password',]

    def create(self, validated_data):
       return Register.objects.create(**validated_data)


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





