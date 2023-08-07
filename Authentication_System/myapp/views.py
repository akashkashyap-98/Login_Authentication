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


class AuthorDetailsById(APIView):
    permission_classes = []
    authentication_classes=[]

    def get(self, request, id, format=None):
        try:
            if Author.objects.filter(id=id).exists():
                author_obj = Author.objects.get(id=id)
                serializer = AuthorGetSerializer(author_obj, context={'request':request})
                print(serializer.data)
                return Response(
                    {
                        'status':'True',
                        'data':serializer.data
                    } , 200
                )
            else:
                return Response(
                    {
                        'status':'False',
                        'response':'UNABLE TO FIND THE AUTHOR with the given ID',
                        'status_code':400
                    }, 400
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

    def put(self, request, id, format=None):
        try:
            data=request.data
            if Author.objects.filter(id=id).exists():
                author_obj = Author.objects.get(id=id)
                serializer = AuthorUpdateSerializer(author_obj, data=data)
                if serializer.is_valid():
                    serializer.save()
                    return Response({'status':'True' , 'response':serializer.data} , 200)
                else:
                    return Response({'status':'False' , 'error':serializer.errors }  , status=status.HTTP_400_BAD_REQUEST )
            else:
                return Response(
                    {
                        'status':'False',
                        'response':'UNABLE TO FIND THE AUTHOR with the given ID',
                        'status_code':400
                    }, 400
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
        
    def delete(self, request , id , format=None):
        try:
            if Author.objects.filter(id=id).exists():
                author_obj = Author.objects.get(id=id)
                author_obj.delete()
                return Response({'status':'True' , 'response': 'Author deleted successfully!!' } , 200)
            else:
                return Response({"status": "false" , "error" :"Author with  this is  doesn't exists. " } , status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            logger.error(f"An error occurred: {str(e)}")
            return Response(
                {
                    'message': 'An error occurred',
                    'status_code': 500,
                },
                500
            ) 
        
#======================= making GET api for implementing Queries based on Foreign key (models: University , Department , Student) =======================

class ForeignKey_ORM(APIView):
    permission_classes = []
    authentication_classes=[]

    def get(self, request):
        
        # 1. Get all students in a 'Computer Science and Engineering' department and their university name 
        students_in_CSE_with_university_name = Student.objects.filter(department__department_name='Computer Science and Engineering').select_related('department__university')
        
        # By specifying department__university, we are telling Django to include the related university data for each student 
        # in the result set. This way, when you access student.department.university in the loop, Django will not need to make
        #  a separate query to fetch the university object. Instead, it will fetch all the related university objects upfront 
        # using a SQL join and attach them to the corresponding departments in the result set.
        for student in students_in_CSE_with_university_name:
            student_name = student.student_name
            department_name = student.department.department_name
            university_name = student.department.university.university_name

            print('student_name = ',student_name  , 'department_name = ',department_name , 'university_name = ', university_name)


        # 2. Retrieve all departments of a university with related_name 'departments':
        university = University.objects.get(university_name='Babu Banarsi Das University')
        departments = university.departments.all().values()
        print(departments)
                        #  another method without using related name
        a= Department.objects.all().filter(university=University.objects.get(university_name='Babu Banarsi Das University')).values()
        print("================", a)
           
        # 3. Retrieve a specific student ('Akash Kashyap') and access their department using related_name:
        get_dept_of_specific_student=Student.objects.get(student_name='Akash Kashyap').department.department_name
        print(get_dept_of_specific_student)

        # 4. Retrieve all students of a specific university ('Babu Banarsi Das University'):
        specific_university = University.objects.get(university_name='Babu Banarsi Das University')
        print(specific_university)
        students = Student.objects.filter(department__university=specific_university).values()
        print(students)

        # 5. Retrieve all departments and their corresponding university names 
        departments = Department.objects.all().values_list('department_name', 'university__university_name')
        print("###################", departments)
        list1 = list(departments)


        # 6. Fetch all students of a department with department_name = 'Computer Science and Engineering':
        department = Department.objects.get(department_name='Computer Science and Engineering')
        students = department.students.all().values()
                            # second method without using related name
        second_method = Student.objects.all().filter(department = Department.objects.get(department_name= 'Computer Science and Engineering')).values()


        # 7. Fetch all students of all departments of a specific university with university_name = 'Babu Banarsi Das University':
        university = University.objects.get(university_name='Babu Banarsi Das University')
        print(university)
        all_students_of_all_departments_of_specific_university = Student.objects.all().filter(department__university=university).values()
                                                                    # filter all departments whose university is same i.e: BBDU
        print(all_students_of_all_departments_of_specific_university)


        # 8. Fetch all departments along with the count of students in each department:
        from django.db.models import Count
        list2=[]
        
        all_departments= Department.objects.all().annotate(student_count=Count('students'))
        
        for dept in all_departments:
            w=(dept.department_name, dept.student_count)
            list2.append(w)
            print(list2)


        # 9. Get all students in a 'Computer Science and Engineering' department and their university name   (without using for loop , modification in orm query no. 8)

        students_in_CSE_with_university_name = Student.objects.filter(department__department_name='Computer Science and Engineering').values('student_name','department__department_name','department__university__university_name')
        print(students_in_CSE_with_university_name)

        # 10. Fetch all departments along with the count of students in each department: (without using for loop , modification in orm query no. 8)
        print("#######################################################################")

        all_departments_with_count= Department.objects.all().annotate(student_count=Count('students')).values('department_name','student_count')
        print(all_departments_with_count)


        # 11. Fetch all departments that have no students:

        departments_with_no_students = Department.objects.all().filter(students=None).values()

        # 12. Fetch all universities along with the count of departments and the total number of students in each university:

        from django.db.models import Sum, IntegerField
        from django.db.models.functions import Cast
        universities_with_depsrtments_with_all_students = University.objects.all().annotate(dept_count=Count('departments'), total_stu=Cast(Sum('departments__students') , IntegerField())).values()
          

        # 13. Fetch all departments of a university ('Babu Banarsi Das University') with the related_name 'departments':

        all_departments_of_BBDU = University.objects.filter(university_name='Babu Banarsi Das University').values_list('departments__department_name')
                                        # second method without using related name
        aaaa = Department.objects.filter(university__university_name='Babu Banarsi Das University')


        # 14. Fetch all students of a department with the related_name 'students':
        all_students_of_dept_CSE = Department.objects.filter(department_name='Computer Science and Engineering').values_list('students__student_name')
                                        # second method without using related name
        second_method = Student.objects.filter(department__department_name='Computer Science and Engineering')


        # 15. Fetch all students and their respective department names:
        students_with_respective_dept_name = Student.objects.all().values('student_name', 'department__department_name')
        

        # 16. Fetch all universities and the count of departments in each university:
        all_universities_with_dept_count = University.objects.all().annotate(dept_count=Count('departments')).values('university_name', 'dept_count')


        #  17. Fetch the university of a specific student using the related_name 'university':

        university_of_specific_student = University.objects.filter(departments__students__student_name='Akash Kashyap').values()
                        # second method without using related name
        university_of_specific_student_2 = Student.objects.filter(student_name='Akash Kashyap').values('student_name', 'department__university__university_name')


        # 18. Fetch all departments along with their corresponding university names:
        all_departments_with_university_names = Department.objects.all().values('department_name', 'university__university_name')
    
                                # another method by using related name 
        all_departments_with_university_names_2 = University.objects.all().values('departments__department_name','university_name').exclude(departments__department_name=None)

        # 19. Fetch all students of a specific university using the related_name 'students':
        all_students_of_specific_university = University.objects.filter(university_name='Babu Banarsi Das University').values('departments__students__student_name')
        print("@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@@##@#@#@#@#", all_students_of_specific_university)



        return JsonResponse(
            {
                'students_with_university_name': list(students_in_CSE_with_university_name.values()),
                'departments of a university': list(departments),
                'get_dept_of_specific_student': get_dept_of_specific_student,
                'all_students_of_specific_university(BBDU)': list(students),
                'all_department_and _their_university': list1,
                'all_students_of_CSE_department': list(students),
                'all_students_of_all_departments_of_specific_university': list(all_students_of_all_departments_of_specific_university),
                'all_dept_with_all_count_of_students_in_each_dept': list2,
                'students_in_CSE_with_university_name':  list(students_in_CSE_with_university_name),
                'all_dept_with_all_count_of_students_in_each_dept_1': list(all_departments_with_count),
                'departments_with_no_students':list(departments_with_no_students),
                'universities_with_depsrtments_with_all_students': list(universities_with_depsrtments_with_all_students),
                'all_departments_of_BBDU': list(all_departments_of_BBDU),
                'all_students_of_dept_CSE': list(all_students_of_dept_CSE),
                'students_with_respective_dept_name': list(students_with_respective_dept_name),
                'all_universities_with_dept_count':list(all_universities_with_dept_count),
                'university_of_specific_student': list(university_of_specific_student),
                'all_departments_with_university_names':list(all_departments_with_university_names),
                'all_students_of_specific_university': list(all_students_of_specific_university)

            }
        )


# ====================== MULTIPLE DATABASE ===============================================================================

@api_view(['POST'])
@permission_classes([AllowAny])
def create_developer_second_db(request):
    try:
        data = request.data
        serializer = DeveloperPOST_SecondDBSerializer(data=data)
        if serializer.is_valid():
            serializer.save()  

            logger.info(f"Developer created: {serializer.data}")
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
    
@api_view(['GET'])
@permission_classes([AllowAny])
def get_all_developers_second_db(request):
    try:
        all_developers = DeveloperSecondDB.objects.using('second_db').all()
        serializer = DeveloperGET_SecondDBSerializer(all_developers , many=True)
        logger.info("FETCHED ALL THE DEVELOPERS FROM SECOND DATABASE")
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
    
@api_view(['PUT'])
@permission_classes([AllowAny])
def update_developers_second_db(request, id):
    try:
        data=request.data
        if DeveloperSecondDB.objects.using('second_db').filter(id=id).exists():
            developer_obj = DeveloperSecondDB.objects.using('second_db').get(id=id)
            serializer = developer_UPDATE_serializer(developer_obj, data=data)
            if serializer.is_valid():
                serializer.save()
                logger.info("DEVELOPER WITH UPDATED SUCCESSFULLY")
                return Response({'status':'True' , 'data':serializer.data} , 200)
        else:
            return Response({'status':'False' , 'response':'UNABLE TO FIND THE DEVELOPER' , 'status_code':400}, 400)
        
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
def get_developers_second_db(request, id):
    try:
        if DeveloperSecondDB.objects.using('second_db').filter(id=id).exists():
            developer_obj = DeveloperSecondDB.objects.using('second_db').get(id=id)
            serializer = DeveloperGET_SecondDBSerializer(developer_obj)
            logger.info("DEVELOPER WITH ID  FETCHED SUCCESSFULLY")
            return Response({'status':'True' , 'data':serializer.data} , 200)
        else:
            return Response({'status':'False' , 'response':'UNABLE TO FIND THE DEVELOPER' , 'status_code':400}, 400)
        
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
        return Response(
            {
                'message': 'An error occurred',
                'status_code': 500,
            },
            500
        )  
    
@api_view(['DELETE'])
@permission_classes([AllowAny])
def delete_developers_second_db(request, id):
    try:
        if DeveloperSecondDB.objects.using('second_db').filter(id=id).exists():
            developer_obj = DeveloperSecondDB.objects.using('second_db').get(id=id)
            developer_obj.delete()
            logger.info("DEVELOPER  DELETED SUCCESSFULLY FROM SECOND DATABASE")
            return Response({'status':'True' , 'message':'DEVELOPER  DELETED SUCCESSFULLY FROM SECOND DATABASE' }, 200)
        else:
            return Response({'status':'False' , 'response':'UNABLE TO FIND THE DEVELOPER' , 'status_code':400}, 400)
        
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
        return Response(
            {
                'message': 'An error occurred',
                'status_code': 500,
            },
            500
        )  


