from awd_main.celery import app
import time
from django.core.management import call_command
from django.core.mail import EmailMessage
from django.conf import settings
from .utils import send_email_notification, generate_csv_file


@app.task
def celery_test_task():
    # Simulate a time-consuming task
    time.sleep(10)
    
    # Send an email
    mail_subject = "TEST SUBJECT"  # Fixed typo: mail_sunject
    message = "THIS IS A TEST EMAIL"
    to_email = settings.DEFAULT_TO_EMAIL  # ADD YOUR EMAIL HERE
    send_email_notification(mail_subject, message, to_email)
    return 'Email sent successfully'


@app.task
def import_data_task(file_path, model_name):
    try:
        call_command('importdata', file_path, model_name)
        
    except Exception as e:
        raise e

    #notify the user by email 
    mail_subject = 'Import Data Completed'
    message =  'Your data import has been successful'
    to_email = settings.DEFAULT_TO_EMAIL
    send_email_notification(mail_subject, message, to_email)

    return "Data imported successfully"


@app.task
def export_data_task(model_name):
    # trigger the call command
    try:
        call_command('exportdata', model_name)
    except Exception as e:
        raise e

    file_path = generate_csv_file(model_name)

    # send email with the attachment
    mail_subject = 'Export Data Completed'
    message =  'Your data Export has been successful, please find the attached file'
    to_email = settings.DEFAULT_TO_EMAIL
    send_email_notification(mail_subject, message, to_email, attachment=file_path)

    return "Data exported Successfully"
    
