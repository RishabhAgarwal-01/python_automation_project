import csv
from django.core.management import BaseCommand, CommandError
# from  dataentry.models import Student
import datetime
from django.apps import apps


# proposed command -> python manage.py exportdata model_name
class Command(BaseCommand):
    help = "export data from a database to a CSV file"

    def add_arguments(self, parser):
        parser.add_argument('model_name', type=str, help='name of the model')

    
    def handle(self, *args, **kwargs):
        model_name = kwargs['model_name'].capitalize()

        # search through all the installed apps for the model
        model = None
        for app_config in apps.get_app_configs():
            try :
                model = apps.get_model(app_config.label, model_name)
                break # stop searching once the model is found
            except LookupError:
                continue # continue searching in next app

        if not model:
                raise CommandError(f'Model {model_name} not found in any app')


        # fetch the data from database
        data = model.objects.all()

        # generate the timestamp of current date and time
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")

        # define the csv file name or path
        file_path = f'exported_{model_name}_data_{timestamp}.csv'

        # open the csv file and write the data
        with open(file_path, 'w', newline='') as file:
            writer = csv.writer(file)

            #write the CSV header
            # we want to print the field names of the model that we are trying to export

            writer.writerow([field.name for field in model._meta.fields])

            # write data rows
            for dt in data:
                writer.writerow([getattr(dt, field.name) for field in model._meta.fields])


        self.stdout.write(self.style.SUCCESS("Data exported successfully"))
