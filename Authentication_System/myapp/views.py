from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import *
from rest_framework.decorators import authentication_classes, permission_classes


# Create your views here.

class RegisterUserPostAndGet(APIView):
    permission_classes = ()
    authentication_classes=()

    def post(self,request):
        data=request.data
        serializer = UserCreteSerializer(data=data)
        if serializer.is_valid():
            if data.get('password')==data.get('confirm_password'):
                serializer.save()
                return Response(
                    {'message':'user registered successfully',
                    'staus_code': 201,
                    'response': serializer.data,}, 201

                )
            else:
                return Response({'message':'please check your password and try again',
                'status_code': 400,}, 400)
        else:
            return Response({
				"error" :serializer.errors,
				'status_code': 400
				}, 400)
    
    def get(self,request):
		# method to return all instances over resource '''
        user_objs = Register.objects.all()
        serializer = UserCreteSerializer(user_objs, many=True)
        return Response({'status':200 , 'payload':serializer.data})

class RegisterUserDetailById(APIView):
    permission_classes = ()
    authentication_classes=()

    def get(self, request , id , format=None):
        if Register.objects.filter(id=id).exists():
            user_obj = Register.objects.get(id=id)
            serializer = UserGetSerializer(user_obj, context={'request':request})
            return Response({"status": "true" , "data" :serializer.data},200)
        else:
            return Response({"status": "false" , "response" :"unable to find the User!"},404)

    def put(self, request , id , format=None):
        if Register.objects.filter(id=id).exists():
            data=request.data
            user_obj = Register.objects.get(id=id)
            serializer = UserUpdateSerializer(user_obj, data=data)
            print("---------TESTING----------------")
            
            print(data)
            if serializer.is_valid():

                if data.get('password')==data.get('confirm_password'):
                    serializer.save()
                    return Response(
                        {'message':'user updated successfully',
                        'staus_code': 201,
                        'response': serializer.data,}, 201)
                else:
                    return Response({'message':'please check your password and try again',
                    'status_code': 400,}, 400)
                
            else:
                return Response({"status": "false" , "error" :serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"status": "false" , "response" :"unable to find the User!"},404)

    def delete(self, request, id , format=None):
        if Register.objects.filter(id=id).exists():
            user_obj=Register.objects.get(id=id)
            user_obj.delete()
            return Response({"status": "true",'response': "User deleted successfully!!"},200)
        else:
            return Response({"status": "false" , "error" :"User doesn't exists. " }, status=status.HTTP_400_BAD_REQUEST)
