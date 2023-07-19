from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import *
from .models import *
from rest_framework import status
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken

from django.core.mail import send_mail
from django.contrib import messages
from django.conf import settings

import logging
# logging.basicConfig(
#     filename="myapp/logs/logfile1.log",
#     filemode='a',
#     format='%(asctime)s - %(levelname)s - %(message)s',
#     datefmt='%Y-%m-%d %H:%M:%S',
# )

logger = logging.getLogger('myapp.views')


# Create your views here.

class RegisterUserPostAndGet(APIView):
    permission_classes = []
    authentication_classes=[]

    def post(self,request):
        try:
            data=request.data
            serializer = UserCreteSerializer(data=data)
            if serializer.is_valid():
                if data.get('password')==data.get('confirm_password'):
                    instance = serializer.save()

                    # ------sending username and OTP to email-------------
                    subject = 'WELCOME TO THE TASK_TOKEN '
                    message = f"Hii! , {instance.email} your username is : {instance.email} and your OTP is {instance.OTP}"
                    from_email = settings.EMAIL_HOST_USER
                    recipient_list = [data['email']]
                    send_mail(subject , message , from_email , recipient_list , fail_silently=False)

                    
                    logger.info("user registered successfully")
                    return Response(
                        {'message':'user registered successfully',
                        'staus_code': 201,
                        'response': serializer.data,}, 201

                    )
                else:
                    logger.error("password and confirm password must be same , please check it and try again")
                    return Response({'message':'please check your password and try again',
                    'status_code': 400,}, 400)
            else:
                logger.error("serializer is not valid , please check the json data")
                return Response({
                    "error" :serializer.errors,
                    'status_code': 400
                    }, 400)
        except Exception as e:
            logger.error(f"An error occurred: {str(e)}")
            return Response(
                {
                    'message': 'An error occurred',
                    'status_code': 500,
                },
                500
            )




    def get(self,request):
        try:
            # method to return all instances over resource '''
            user_objs = Register.objects.all()
            serializer = UserCreteSerializer(user_objs, many=True)
            return Response({'status':200 , 'payload':serializer.data})
        except Exception as e:
            logger.error(f"An error occurred: {str(e)}")
            return Response(
                {
                    'message': 'An error occurred',
                    'status_code': 500,
                },
                500
            )

class RegisterUserDetailById(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes=[ JWTAuthentication ]

    def get(self, request , id , format=None):
        try:
            if Register.objects.filter(id=id).exists():
                user_obj = Register.objects.get(id=id)
                serializer = UserGetSerializer(user_obj, context={'request':request})
                logger.info("user fetched by id successfully")
                return Response({"status": "true" , "data" :serializer.data},200)
            else:
                logger.error("unable to fetch the user by the entered id")
                return Response({"status": "false" , "response" :"unable to find the User!"},404)
            
        except Exception as e:
            logger.error(f"An error occurred: {str(e)}")
            return Response(
                {
                    'message': 'An error occurred',
                    'status_code': 500,
                },
                500
            )

    def put(self, request , id , format=None):
        try:
            if Register.objects.filter(id=id).exists():
                data=request.data
                user_obj = Register.objects.get(id=id)
                serializer = UserUpdateSerializer(user_obj, data=data)
                print("---------TESTING----------------")
                
                print(data)
                if serializer.is_valid():

                    if data.get('password')==data.get('confirm_password'):
                        serializer.save()
                        logger.info("user updated successfully")
                        return Response(
                            {'message':'user updated successfully',
                            'staus_code': 201,
                            'response': serializer.data,}, 201)
                    else:
                        logger.error("incorrect password")
                        return Response({'message':'please check your password and try again',
                        'status_code': 400,}, 400)
                    
                else:
                    logger.error("invalid  serializer data")
                    return Response({"status": "false" , "error" :serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
            else:
                logger.error("unable to find the user with the entered id")
                return Response({"status": "false" , "response" :"unable to find the User!"},404)
        
        except Exception as e:
            logger.error(f"An error occurred: {str(e)}")
            return Response(
                {
                    'message': 'An error occurred',
                    'status_code': 500,
                },
                500
            )

    def delete(self, request, id , format=None):
        try:
            if Register.objects.filter(id=id).exists():
                user_obj=Register.objects.get(id=id)
                user_obj.delete()
                logger.info("user deleted successfully")
                return Response({"status": "true",'response': "User deleted successfully!!"},200)
            else:
                logger.error("incorrect id , user with this id does not exists.")
                return Response({"status": "false" , "error" :"User doesn't exists. " }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"An error occurred: {str(e)}")
            return Response(
                {
                    'message': 'An error occurred',
                    'status_code': 500,
                },
                500
            )


class LoginUserPostAndGet(APIView):
    permission_classes = []
    authentication_classes=[]

    def post(self,request):
        try:
            data=request.data
            print(data)
            serializer = LoginUserCreateSerializer(data=data)
            if serializer.is_valid():
                dbuser = Register.objects.get(email=data.get('email'))
                if dbuser is not None:

                    print("i am db user", dbuser.email , dbuser.password , data.get['entered_otp'])
                    if Register.objects.filter(email=dbuser.email) and Register.objects.filter(password=dbuser.password):
                        logging.warning("Email and password matched")

                        serializer.save()

                        #----if user login the is_active field turns True-----
                        userr = Login.objects.filter(email=dbuser.email).update(is_active=True)
                        print("----------debugging---------------")
                        print(userr)

                        #-----creating token manually------------------

                        refresh = RefreshToken.for_user(dbuser)

                        logger.info("user logged in successfully")
                        return Response(
                            {'message':'user LoggedIn successfully',
                            'staus_code': 201,
                            'response': 'success',
                            'refresh': str(refresh),
                            'access': str(refresh.access_token),}, 201
                        )
                    else:
                        logger.error("invalid credentials")
                        return Response(
                            {'message':'Please Check Your Credentials',
                            'staus_code': 401,}, 401
                        )
                else:
                    logger.error("EMAIL OR PASSWORD IS INCORRECT")
                    return Response(
                        {'message':'Please Check Your Credentials',
                            'staus_code': 401,}, 401
                    )
            else:
                logger.error("invalid serializer data")
                return Response({
                    "error" :serializer.errors,
                    'status_code': 400, }, 400)
            
        except Exception as e:
            logger.error(f"An error occurred: {str(e)}")
            return Response(
                {
                    'message': 'An error occurred',
                    'status_code': 500,
                },
                500
            )
            

class LoginResponsePage(APIView):
    permission_classes = []
    authentication_classes=[]

    def post(self, request):
        data = request.data
        try:
            print("------I am TRY---------")
            token = request.META['HTTP_AUTHORIZATION'].split(' ')[1]
            print(token)

            token_obj = RefreshToken(token)
            if token_obj:
                inactive_users = Login.objects.filter(is_active=False).values('email')

                logger.info("welcome to login response page")
                return Response({'message':'page after login , This page can only be seen by the user who have proper login credentials' ,
                                 'inactive_users':list(inactive_users)})
        except Exception as e:
            logger.error("Please enter a valid token")
            return Response({'message':'please check your token and try again'}, status=status.HTTP_400_BAD_REQUEST)
        

        
# class Logout(APIView):
#     permission_classes = []
#     authentication_classes=[]

#     def post(self, request , format = None):
#         data=request.data
#         try:
#             print("======i am try=========")
#             refresh_token = request.META['HTTP_AUTHORIZATION'].split(' ')[1]
#             token = RefreshToken(refresh_token)
#             print(token)

#             user_email = data.get('email')
#             print(user_email)
#             user_password = data.get('password')
#             print(user_password)
#             print("---------------------------------")
#             if user_email and user_password:
#                 print("-------------------------")
#                 if Login.objects.filter(email=user_email) and Login.objects.filter(password=user_password):
#                     print("=====Email and password matched successfully====")
#                     Login.objects.filter(email=user_email).update(is_active=False)

#                     # token.blacklist()
#                     logger.info("Successfully logged out.")
#                     return Response({"message": "Successfully logged out."}, status=status.HTTP_200_OK)
#                 else:
#                     logger.error("please enter valid credentials for logout")
#                     return Response({'message':'Please check your email and password and try again'})
#             else:
#                 logger.error("please enter email and password to logout")
#                 return Response({'message':'please enter email and password to logout'})
            
#         except Exception as e:
#             logger.error("Invalid token.")
#             return Response({"message": "Invalid token."}, status=status.HTTP_400_BAD_REQUEST)


from functools import wraps

def authenticate(func):
    @wraps(func)  # Preserves the original function's name and docstring
    def wrapper(self, request, *args, **kwargs):
        data = request.data
        try:
            print("======i am try=========")
            refresh_token = request.META['HTTP_AUTHORIZATION'].split(' ')[1]
            token = RefreshToken(refresh_token)
            print(token)

            user_email = data.get('email')
            print(user_email)
            user_password = data.get('password')
            print(user_password)
            print("---------------------------------")
            if user_email and user_password:
                print("-------------------------")
                if Login.objects.filter(email=user_email) and Login.objects.filter(password=user_password):
                    print("=====Email and password matched successfully====")
                    Login.objects.filter(email=user_email).update(is_active=False)

                    # token.blacklist()
                    logger.info("Successfully logged out.")
                    return Response({"message": "Successfully logged out."}, status=status.HTTP_200_OK)
                else:
                    logger.error("please enter valid credentials for logout")
                    return Response({'message': 'Please check your email and password and try again'})
            else:
                logger.error("please enter email and password to logout")
                return Response({'message': 'please enter email and password to logout'})

        except Exception as e:
            logger.error("Invalid token.")
            return Response({"message": "Invalid token."}, status=status.HTTP_400_BAD_REQUEST)

    return wrapper


class Logout(APIView):
    permission_classes = []
    authentication_classes = []

    @authenticate  # Applying the decorator to the 'post' method
    def post(self, request, format=None):
        data = request.data
        try:
            print("======i am try=========")
            refresh_token = request.META['HTTP_AUTHORIZATION'].split(' ')[1]
            token = RefreshToken(refresh_token)
            print(token)

            user_email = data.get('email')
            print(user_email)
            user_password = data.get('password')
            print(user_password)
            print("---------------------------------")
            if user_email and user_password:
                print("-------------------------")
                if Login.objects.filter(email=user_email) and Login.objects.filter(password=user_password):
                    print("=====Email and password matched successfully====")
                    Login.objects.filter(email=user_email).update(is_active=False)

                    # token.blacklist()
                    logger.info("Successfully logged out.")
                    return Response({"message": "Successfully logged out."}, status=status.HTTP_200_OK)
                else:
                    logger.error("please enter valid credentials for logout")
                    return Response({'message': 'Please check your email and password and try again'})
            else:
                logger.error("please enter email and password to logout")
                return Response({'message': 'please enter email and password to logout'})

        except Exception as e:
            logger.error("Invalid token.")
            return Response({"message": "Invalid token."}, status=status.HTTP_400_BAD_REQUEST)




