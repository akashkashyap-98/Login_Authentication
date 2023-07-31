from django.shortcuts import render
from django.http import JsonResponse

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

from django.db.models import Min, Max
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
    authentication_classes = []

    def post(self,request):
        try:
            data=request.data
            print(data)
            serializer = LoginUserCreateSerializer(data=data)
            if serializer.is_valid():
                dbuser = Register.objects.filter(email=data.get('email')).values('email','password','OTP')
                print("========= debug ============")
                print(dbuser)
                # print(dbuser[0]['OTP'])
                if dbuser:
                    if data.get('otp'):
                        if dbuser[0]['OTP'] == data.get('otp'):

                            print("i am db user", dbuser[0]['email'] , dbuser[0]['password'] , data.get('otp'))
                            if Register.objects.filter(email= data.get('email')) and Register.objects.filter(password=data.get('password')):
                                logging.warning("Email and password matched")

                                serializer.save()

                                #----if user login the is_active field turns True-----
                                userr = Login.objects.filter(email=dbuser[0]['email']).update(is_active=True)
                                print("----------debugging---------------")
                                print(userr)

                                #-----creating token manually------------------
                                user_obj=Register.objects.get(email=data.get('email'))
                                refresh = RefreshToken.for_user(user_obj)

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
                            return Response(
                                {'message':'Invalid otp , please check your otp and try again',
                                    'staus_code': 400,}, 400
                            )
                    else:
                        return Response(
                            {'message':'please enter the otp to login'}
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
        


class Orm_Implementation(APIView):
    permission_classes = []
    authentication_classes=[]

    def get(self, request):
        #  To get all the register users
        all_registered_users = Register.objects.all()

        # Filter the users on tha basis of email
        filter_users = Register.objects.filter(email='akash@gmail.com').values('email','first_name', 'last_name')

        # find the first registered user
        first_user = Register.objects.all().values_list('email').first()

        # find the last registered  user
        last_user = Register.objects.all().values_list('email').last()

        # Find the first five registered users
        first_five_users = Register.objects.all().values_list('email')[0:5]

        # Find the last five registered users
        last_five_users = Register.objects.order_by('-id').values_list('email')[0:5]

        # find the user whose id is 1
        user_id_1 = Register.objects.filter(id=1).values_list('email')

        # find the users whose id is less then 5 
        user_id_lt_5= Register.objects.filter(id__lt=5).values_list('email')

        # find the users whose id is greater then or equals to 5 
        user_id_gte_5= Register.objects.filter(id__gte=5).values_list('email')

        # union operation
        union_all_users = user_id_lt_5.union(user_id_gte_5)

        # return all the users except the user having id = 1
        list_of_users_except_id_1 = Register.objects.exclude(id=1).values_list('email')

        # list of all users whose id in between 5 to 10
        list_of_users_having_id_between_5to10 = Register.objects.filter(id__range=(5,10)).values_list('email')

        # list of users having 'a' in username
        list_of_user_having_a_alphabet_in_username = Register.objects.filter(username__icontains='a').values_list('email','username')

        # list of users username starts with 'a'
        list_of_users_username_startswith_a = Register.objects.filter(username__istartswith='a').values_list('email','username')

        # list of users having id in list [1,2,3]
        users_in_list = Register.objects.filter(id__in=[1,2,3]).values_list('id','email')

        # list of active useres from login Table
        active_users = Login.objects.filter(is_active='True').values_list('email')

        # count all the registered users
        number_of_users = Register.objects.count()

        # user who is having minimum id
        minimum_id = Register.objects.all().aggregate(Min('id'))

        # maximum id
        maximum_id = Register.objects.all().aggregate(Max('id'))


        return JsonResponse(
            {
                'list of all registered users': list(all_registered_users.values_list('email')),
                'filter_users': list(filter_users),
                'first_user': list(first_user),
                'last_user': list(last_user),
                'first_five_users': list(first_five_users),
                'last_five_users':list(last_five_users),
                'user_id_1': list(user_id_1),
                'user_id_lt_5':list(user_id_lt_5),
                'user_id_gte_5': list(user_id_gte_5),
                'union_all_users': list(union_all_users),
                'list_of_users_except_id_1': list(list_of_users_except_id_1),
                'list_of_users_having_id_between_5to10' : list(list_of_users_having_id_between_5to10),
                'list_of_user_having_a_alphabet_in_usernamr' : list(list_of_user_having_a_alphabet_in_username),
                'list_of_users_username_startswith_a':list(list_of_users_username_startswith_a),
                'users_in_list' : list(users_in_list),
                'active_users' : list(active_users),
                'number_of_users': number_of_users,
                'minimum_id': minimum_id,
                'maximum_id': maximum_id

            },
            status=200  
        )


# =========================== Function based post api for Employee model =============================================

from rest_framework.decorators import api_view
from rest_framework.permissions import AllowAny


@api_view(['POST'])
@permission_classes([AllowAny])
def create_employee(request):
    data = request.data
    print("---i am data-----", data)
    serializer = EmployeeSerializer(data=data)
    if serializer.is_valid():
        serializer.save() 

        # Log the creation event
        logger.info(f"Employee created: {serializer.data}")

        return Response({
            'status':'True',
            'message': 'Employee created successfully',
            'response': serializer.data
        }, 201)
    else:
        return Response({
            'status': 'False',
            'response': serializer.errors
        }, 400)
    
@api_view(['GET'])
@permission_classes([AllowAny])
def get_all_employees(request):
    try:
        # method to return all instances over resource '''
        emp_objs = Employee.objects.all()
        serializer = EmployeeSerializer(emp_objs, many=True)
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
    
@api_view(['GET'])
@permission_classes([AllowAny])
def get_employee_by_id(request , id):
    try:
        
        if Employee.objects.filter(id=id).exists():
            emp_obj = Employee.objects.filter(id=id)
            serializer = EmployeeSerializer(emp_obj, many=True)
            logger.info("Fetched employee by id successfully")
            return Response({'status':200 , 'payload':serializer.data})
        else:
            logger.error("employee id dosen't exists ")
            return Response({'status':400 , 'message':'employee id dosent exists'})

    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
        return Response(
            {
                'message': 'An error occurred',
                'status_code': 500,
            },
            500
        )
    
@api_view(['PUT'])
@permission_classes([AllowAny])
def update_employee_by_id(request , id):
    try:
        
        if Employee.objects.filter(id=id).exists():
            data=request.data
            emp_obj = Employee.objects.get(id=id)
            serializer = EmployeeUpdateSerializer(emp_obj, data=data)
            if serializer.is_valid():
                serializer.save()
                logger.info("Employee Updated successfully")
                return Response({'status':200 , 'payload':serializer.data})
        else:
            logger.error("employee id dosen't exists ")
            return Response({'status':400 , 'message':'employee id dosent exists'})

    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
        return Response(
            {
                'message': 'An error occurred',
                'status_code': 500,
            },
            500
        )
    
# ======================= post api for default and second database =====================================


@api_view(['POST'])
@permission_classes([AllowAny])
def create_student_multiple_db(request):
    try:
        data = request.data
        if data.get('database'):
            database = data.get('database', 'default')  # Get the 'database' value from the request data
            print(database)
            if database not in ['default', 'second_db']:
                return Response({'error': 'Invalid database specified.'}, status=400)
            
            # checking for the database
            if database == 'default':
                serializer = StudentDefaultDBSerializer(data=request.data)
            else:
                serializer = StudentSecondDBSerializer(data=request.data)

            if serializer.is_valid():
                serializer.save()  

                logger.info(f"Employee created: {serializer.data}")
                return Response({
                    'status':'True',
                    'message': 'Employee created successfully',
                    'response': serializer.data
                }, 201)
            else:
                return Response({
                    'status': 'False',
                    'response': serializer.errors
                }, 400)
        else:
            return Response({
                    'status': 'False',
                    'response': 'please mention the type of database'
                }, 400)


    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
        return Response(
            {
                'message': 'An error occurred',
                'status_code': 400,
                'errors': str(e)
            },
            400
        )
        
#  ======================= GET all the users from multiple database =========================================
@api_view(['GET'])
@permission_classes([AllowAny])
def get_student_multiple_db(request):
    try:
        data = request.data
        if data.get('database'):
            database = data.get('database', 'default')
            print(database)
            if database not in ['default', 'second_db']:
                return Response({'error': 'Invalid database specified.'}, status=400)

            # checking for the database
            if database == 'default':
                student_objs = StudentDefaultDB.objects.using('default').all()
                serializer = StudentDefaultDB_Get_Serializer(student_objs , many=True)
                return Response({'status':200 , 'payload':serializer.data})
            else:
                student_objs = StudentSecondDB.objects.using('second_db').all()
                serializer = StudentSecondDB_Get_Serializer(student_objs , many=True)
                return Response({'status':200 , 'payload':serializer.data})
        
        else:
            return Response({
                    'status': 'False',
                    'response': 'please mention the type of database'
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
    
# ========================================= GET the particular user by id fromk multiple database =========================================
@api_view(['GET'])
@permission_classes([AllowAny])
def get_student_by_id_multiple_db(request, id):
    try:
        data = request.data
        if data.get('database'):
            database = data.get('database', 'default')
            print(database)
            if database not in ['default', 'second_db']:
                return Response({'error': 'Invalid database specified.'}, status=400)

            # checking for the database
            if database == 'default':
                if StudentDefaultDB.objects.using('default').filter(id=id).exists():
                    print("TRUE")
                    student_objs = StudentDefaultDB.objects.using('default').filter(id=id).values('id', 'full_name', 'email', 'school', 'city')
                    print(student_objs)
                    serializer = StudentDefaultDB_Get_Serializer(student_objs , many=True)
                    return Response({'status':200 , 'payload':serializer.data})
                else:
                    return Response({'error': 'id  does not exist.'}, status=400)
                
            if database == 'second_db':
                if StudentSecondDB.objects.using('second_db').filter(id=id).exists():
                    student_objs = StudentSecondDB.objects.using('second_db').filter(id=id).values('id', 'full_name', 'email', 'school', 'city')
                    serializer = StudentSecondDB_Get_Serializer(student_objs , many=True)
                    return Response({'status':200 , 'payload':serializer.data})
                else:
                    return Response({'error': 'id  does not exist.'}, status=400)
        
        else:
            return Response({
                    'status': 'False',
                    'response': 'please mention the type of database'
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
    

# ========================================= UPDATE the particular user by id fromk multiple database =========================================
@api_view(['PUT'])
@permission_classes([AllowAny])
def update_student_by_id_multiple_db(request, id):
    try:
        data = request.data
        if data.get('database'):
            database = data.get('database', 'default')
            print(database)
            if database not in ['default', 'second_db']:
                return Response({'error': 'Invalid database specified.'}, status=400)

            # checking for the database
            if database == 'default':
                if StudentDefaultDB.objects.using('default').filter(id=id).exists():
                    print("TRUE")
                    student_obj = StudentDefaultDB.objects.using('default').get(id=id)
                    print(student_obj)
                    serializer = StudentDefaultDB_Update_Serializer(student_obj , data=data)
                    
                    if serializer.is_valid():
                        # print(serializer.data)
                        serializer.save()
                        logger.info("Student in default database  Updated successfully")
                        return Response({'status':200 , 'payload':serializer.data})
                else:
                    return Response({'error': 'id  does not exist.'}, status=400)
                
            if database == 'second_db':
                if StudentSecondDB.objects.using('second_db').filter(id=id).exists():
                    print("TRUE")
                    student_obj = StudentSecondDB.objects.using('second_db').get(id=id)
                    print(student_obj)
                    serializer = StudentDefaultDB_Update_Serializer(student_obj , data=data)
                    if serializer.is_valid():
                        serializer.save()
                        logger.info("Student in second_db database  Updated successfully")
                        return Response({'status':200 , 'payload':serializer.data})
                else:
                    return Response({'error': 'id  does not exist.'}, status=400)
        
        else:
            return Response({
                    'status': 'False',
                    'response': 'please mention the type of database'
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
    
# ========================================= DELETE the particular student by id from multiple database ==================================
        
@api_view(['DELETE'])
@permission_classes([AllowAny])
def delete_student_by_id_multiple_db(request, id):
    try:
        data = request.data
        if data.get('database'):
            database = data.get('database', 'default')
            print(database)
            if database not in ['default', 'second_db']:
                return Response({'error': 'Invalid database specified.'}, status=400)

            # checking for the database
            if database == 'default':
                if StudentDefaultDB.objects.using('default').filter(id=id).exists():
                    print("TRUE")
                    student_obj = StudentDefaultDB.objects.using('default').get(id=id)
                    print(student_obj)
                    student_obj.delete()
                    logger.info("Student in default database  Deleted successfully")
                    return Response({'status':200 , 'message':'Student deleted from Table of default Database successfully'})
                else:
                    return Response({'error': 'id  does not exist.'}, status=400)
                
            if database == 'second_db':
                if StudentSecondDB.objects.using('second_db').filter(id=id).exists():
                    print("TRUE")
                    student_obj = StudentSecondDB.objects.using('second_db').get(id=id)
                    print(student_obj)
                    student_obj.delete()
                    logger.info("Student in second_db database  Updated successfully")
                    return Response({'status':200 , 'message':'Student deleted from Table of second_db Database successfully'})
                else:
                    return Response({'error': 'id  does not exist.'}, status=400)
        
        else:
            return Response({
                    'status': 'False',
                    'response': 'please mention the type of database'
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

# ===================================== creating views for Author and Book (Many to Many Relationship)==================================

class BookGetAndPostApi(APIView):
    permission_classes = []
    authentication_classes=[]

    def post(self, request):
        try:
            data = request.data
            serializer = BookCreateSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                logger.info("BOOK CREATED SUCCESSFULLY")
                return Response({
                'message':'BOOK CREATED SUCCESSFULLY',
                'status':'true',
                'status_code':'201',
                'response':serializer.data,
                },201)
            else:
                return Response({'status':'False' , 'message':'NOT ABLE TO CREATE BOOK', 'status_code': 400} , 400)

        except Exception as e:
            logger.error(f"An error occurred: {str(e)}")
            return Response(
                {
                    'message': 'An error occurred',
                    'status_code': 500,
                },
                500
            ) 
    
    def get(self, request):

        book_obj=Book.objects.all()
        serializer=BookGetSerializer(book_obj , many=True)
        return Response({'status':'True' , "data":serializer.data},200)
    
class BookDetailById(APIView):
    permission_classes = []
    authentication_classes=[]

    def get(self, request, id, format=None):
        try:
            if Book.objects.filter(id=id).exists():
                book_obj = Book.objects.get(id=id)
                serializer = BookGetSerializer(book_obj, context={'request':request})
                return Response({'status':'True' , 'data':serializer.data} , 200)
            else:
                return Response({'status':'False' , 'response':'UNABLE TO FIND THE BOOK' , 'status_code':400}, 400)
            
        except Exception as e:
            logger.error(f"An error occurred: {str(e)}")
            return Response(
                {
                    'message': 'An error occurred',
                    'status_code': 500,
                },
                500
            )  

    def put(self , request , id , format=None):
        try:
            data=request.data
            if Book.objects.filter(id=id).exists():
                book_obj=Book.objects.get(id=id)
                serializer=BookUpdateSerializer(book_obj , data=data)
                if serializer.is_valid():
                    serializer.save()
                    return Response({'status':'True' , 'response':serializer.data} , 200)
                else:
                    return Response({'status':'False' , 'error':serializer.errors }  , status=status.HTTP_400_BAD_REQUEST )
            else:
                return Response(
                    {'status':'False',
                     'message':'id of book dosent exists'}
                )
                
        except Exception as e:
            logger.error(f"An error occurred: {str(e)}")
            return Response(
                {
                    'message': 'An error occurred',
                    'status_code': 500,
                },
                500
            )  


    def delete(self , request , id , format=None):
        try:
            if Book.objects.filter(id=id).exists():
                book_obj=Book.objects.get(id=id)
                book_obj.delete()
                return Response({'status':'True' , 'response': 'Book deleted successfully!!' } , 200)
            else:
                return Response({"status": "false" , "error" :"Book doesn't exists. " } , status=status.HTTP_400_BAD_REQUEST)
            
        except Exception as e:
            logger.error(f"An error occurred: {str(e)}")
            return Response(
                {
                    'message': 'An error occurred',
                    'status_code': 500,
                },
                500
            )  


class AuthorGetAndPost(APIView):
    permission_classes = []
    authentication_classes=[]

    def post(self, request):
        try:
            data = request.data
            serializer = AuthorCreateSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                logger.info("AUTHOR CREATED SUCCESSFULLY")
                print(serializer.data)
                return Response({
                    'message':'AUTHOR CREATED SUCCESSFULLY',
                    'status':'true',
                    'status_code':'201',
                    'response':serializer.data,
                    },201)
            else:
                return Response({'status':'False' , 'message':'NOT ABLE TO CREATE AUTHOR', 'status_code': 400} , 400)

        except Exception as e:
            logger.error(f"An error occurred: {str(e)}")
            return Response(
                {
                    'message': 'An error occurred',
                    'status_code': 500,
                },
                500
            ) 
        
        
    def get(self, request):
        try:
            author_objs = Author.objects.all()
            serializer = AuthorGetSerializer(author_objs, many=True)
            return Response(
                {'status':'True' ,
                  "data":serializer.data}
                  ,200)
        except Exception as e:
            logger.error(f"An error occurred: {str(e)}")
            return Response(
                {
                    'message': 'An error occurred',
                    'status_code': 500,
                },
                500
            ) 
        




    
