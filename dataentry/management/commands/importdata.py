from django.core.management import BaseCommand, CommandError
# from dataentry.models import Student
from django.apps import apps
from django.db import DataError
import csv
from dataentry.utils import check_csv_errors

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

        # utils.py check for the csv error before execution of the creating the records in the models
        # the check_csv_errors return a model which we got after searching through all installed apps
        model = check_csv_errors(file_path, model_name)

        # read the file, take every record and create it 
        with open(file_path, 'r') as file:
            reader = csv.DictReader(file)

            # batching 
            batch_size = 5000 
            records = []

            for row in reader:
                # Use model(**row) to prep the record without saving it to the DB yet
                records.append(model(**row))
                
                # When we hit 5,000 records, do one massive database insert
                if len(records) >= batch_size:
                    model.objects.bulk_create(records)
                    records = [] # Clear the list to free up your laptop's RAM

            if records:
                model.objects.bulk_create(records)
        
        self.stdout.write(self.style.SUCCESS("Data imported from CSV successfully"))