from django.contrib.auth import get_user_model

from celery import shared_task
from django.core.mail import send_mail
from Authentication_System import settings
from django.utils import timezone
from datetime import timedelta

@shared_task(bind=True)
def send_mail_func(self):
    user = 'akash.kashyap@oodles.io'
    #timezone.localtime(users.date_time) + timedelta(days=2)
    
    mail_subject = "Hi! Celery Testing by Akash"
    message = "Hello , My name is akash kashyap and i am testing CELERY send mail functionality"
    to_email = user
    send_mail(
        subject = mail_subject,
        message=message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[to_email],
        fail_silently=True,
    )
    return "Done" 

# -------- task to send the email , export the data to pdf and send it to email attachment---------------

from django.core.mail import EmailMessage
from django.conf import settings
from django.http import HttpResponse
import pandas as pd
from io import BytesIO
from openpyxl.workbook import Workbook

from myapp.models import Student

@shared_task(bind=True)
def generate_excel_and_send_email(request):
    # Retrieve data from the Student model
    students = Student.objects.all()

    # Create a DataFrame from the QuerySet
    data = {
        'Student ID': [student.id for student in students],
        'Student Name': [student.student_name for student in students],
        'Department': [student.department for student in students],
    }
    df = pd.DataFrame(data)

    # Save the DataFrame as an Excel file
    excel_buffer = BytesIO()
    df.to_excel(excel_buffer, index=False, sheet_name='Student Data')
    excel_buffer.seek(0)

    # Create an email message with the Excel attachment
    email_subject = "Student Data Excel Report"
    email_body = "Please find the attached Excel report."
    from_email = settings.EMAIL_HOST_USER
    to_email = 'akash.kashyap@oodles.io' 

    email = EmailMessage(
        email_subject, email_body, from_email, [to_email]
    )
    email.attach('student_data_report.xlsx', excel_buffer.read(), 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    email.send()

    return "Email sent with Excel attachment."


