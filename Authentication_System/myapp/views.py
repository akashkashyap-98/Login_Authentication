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
    permission_classes = [IsAuthenticated]
    authentication_classes=[ JWTAuthentication ]

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


class LoginUserPostAndGet(APIView):
    permission_classes = []
    authentication_classes=[]

    def post(self,request):
        data=request.data
        print(data)
        serializer = LoginUserCreateSerializer(data=data)
        if serializer.is_valid():
            dbuser = Register.objects.get(email=data.get('email'))
            if dbuser is not None:

                print("i am db user", dbuser.email , dbuser.password)
                if Register.objects.filter(email=dbuser.email) and Register.objects.filter(password=dbuser.password):
                    logging.warning("Email and password matched")

                    serializer.save()

                    #----if user login the is_active field turns True-----
                    userr = Login.objects.filter(email=dbuser.email).update(is_active=True)
                    print("----------debugging---------------")
                    print(userr)

                    #-----creating token manually------------------

                    refresh = RefreshToken.for_user(dbuser)

                    return Response(
                        {'message':'user LoggedIn successfully',
                        'staus_code': 201,
                        'response': 'success',
                        'refresh': str(refresh),
                        'access': str(refresh.access_token),}, 201
                    )
                else:
                    return Response(
                        {'message':'Please Check Your Credentials',
                        'staus_code': 401,}, 401
                    )
            else:
                logging.warning("EMAIL OR PASSWORD IS INCORRECT")
                return Response(
                    {'message':'Please Check Your Credentials',
                        'staus_code': 401,}, 401
                )
        else:
            return Response({
                "error" :serializer.errors,
                'status_code': 400, }, 400)
        

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

                return Response({'message':'page after login , This page can only be seen by the user who have proper login credentials' ,
                                 'inactive_users':list(inactive_users)})
        except Exception as e:
            logging.warning("Please enter a valid token")
            logging.info("AKASH KASHYAP")
            return Response({'message':'please check your token and try again'}, status=status.HTTP_400_BAD_REQUEST)
        

        
class Logout(APIView):
    permission_classes = []
    authentication_classes=[]

    def post(self, request , format = None):
        data=request.data
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
                    return Response({'message':'Please check your email and password and try again'})
            else:
                logger.error("please enter email and password to logout")
                return Response({'message':'please enter email and password to logout'})
            
        except Exception as e:
            logger.error("Invalid token.")
            return Response({"message": "Invalid token."}, status=status.HTTP_400_BAD_REQUEST)
        





# class Logout(APIView):
#     permission_classes = []
#     authentication_classes=[]

#     def post(self, request):
#         data=request.data
#         # serializer=LogoutUserSerializer(data=data)
#         print("-------testting  1 for logout--------------")
#         # if serializer.is_valid():
#         print("-------testting for logout--------------")
#         user_email = data.get('email')
#         user_password = data.get('password')
#         if Login.objects.filter(email = user_email) and Login.objects.filter(password = user_password) :
#             Login.objects.filter(email='user_email').delete()
#             print("-------user deleted from login table--------")
#             return Response(
#             {'message':'user Logged Out successfully',
#             'staus_code': 201,
#             'response': 'success'}, 201
#             )
#         else:
#             return Response({
#                 'message':'please check your credentials',
#                 'status_code': 400, }, 400)

