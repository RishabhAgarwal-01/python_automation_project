from django.core.management import BaseCommand
from dataentry.models import Student

class Command(BaseCommand):
    help = "It will insert data to the database"

    def handle(self, *args, **kwargs):
        # logic for the insert data 
        
        self.stdout.write(self.style.SUCCESS("Data inserted successfully"))