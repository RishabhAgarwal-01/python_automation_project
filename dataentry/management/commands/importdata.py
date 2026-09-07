from django.core.management import BaseCommand, CommandError
# from dataentry.models import Student
from django.apps import apps
from django.db import DataError
import csv

# proposed command -> python manage.py importdata file_path model_name
class Command(BaseCommand):
    help = "It will import data from csv file"

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='path to the csv file name')
        parser.add_argument('model_name', type=str, help='name of the model')


    def handle(self, *args, **kwargs):

        # logic for the insert data 
        file_path = kwargs['file_path']
        model_name = kwargs['model_name'].capitalize()

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
        model_fields = [field.name for field in model._meta.fields if  field.name != 'id']
        


        with open(file_path, 'r') as file:
            reader = csv.DictReader(file)
            csv_header =  reader.fieldnames # list of the first row of the csv as the header

            # compare csv header with model's field names
            if csv_header != model_fields:
                raise DataError(f"CSV File doesn't match with the {model_name} table fields")

            for row in reader:
                model.objects.create(**row)
        
        self.stdout.write(self.style.SUCCESS("Data imported from CSV successfully"))