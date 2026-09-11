import logging
from typing import List
from django.apps import apps
from django.core.management import CommandError
import csv
from django.db import DataError
from django.core.mail import EmailMessage
from django.conf import settings
import datetime
import os



def get_all_custom_models():
    excluded_apps = {'admin', 'auth', 'contenttypes', 'sessions', 'messages', 'authtoken', 'uploads'}
    custom_models = []


    for model in apps.get_models():
        if model._meta.app_label not in excluded_apps:
            model_string = model.__name__
            custom_models.append(model_string)
            
    return custom_models




def check_csv_errors(file_path, model_name):

    # searching for the model name in all of the istalled apps
    model = None
    for app_config in apps.get_app_configs():
        try :
            model = apps.get_model(app_config.label, model_name)
            break # stop searching once the model is found
        except LookupError:
            continue # continue searching in next app

    if not model:
        raise CommandError(f'Model {model_name} not found in any app')

     # get all the field names of the model that we found
    model_fields = [field.name for field in model._meta.fields if  field.name !='id']

    try:
        with open(file_path, 'r') as file:
            reader = csv.DictReader(file)
            csv_header =  reader.fieldnames # list of the first row of the csv as the header/field names
        
            # compare csv header with model's field names
            if csv_header != model_fields:
                raise DataError(f"CSV File doesn't match with the {model_name} table fields")
    except Exception as e:
        raise e

    return model



# Optional: Set up a basic logger to record which emails failed
logger = logging.getLogger(__name__)

def send_email_notification(mail_subject, message, to_email_list, attachment=None):
    from_email = settings.DEFAULT_FROM_EMAIL
    
    # Loop through the list so one bad email doesn't crash the whole batch
    for email_address in to_email_list:
        try:
            # Send to one person at a time (fixes the privacy issue too!)
            email = EmailMessage(
                subject=mail_subject, 
                body=message, 
                from_email=from_email, 
                to=[email_address] 
            )
            
            if attachment is not None:
                email.attach_file(attachment)
                
            email.send()
            
        except Exception as e:
            # If this specific email fails, log it, but DON'T raise the error.
            # This allows the loop to 'continue' to the next person.
            logger.error(f"Failed to send email to {email_address}. Error: {str(e)}")
            continue




def generate_csv_file(model_name):
    # generate the timestamp of current date and time
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")

    # define the csv file name or path
    export_dir =  'exported_data'
    file_name = f'exported_{model_name}_data_{timestamp}.csv'

    # creation of full path from the C://User ..../media/ which is media root
    # then exportd dir and file name generated
    file_path = os.path.join(settings.MEDIA_ROOT, export_dir, file_name)

    return file_path