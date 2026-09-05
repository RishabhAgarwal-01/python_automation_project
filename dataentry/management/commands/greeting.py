from django.core.management import BaseCommand


# proposed command = python manage.py greeting name
# proposed output = Hi {Name}, Good Morning
class Command(BaseCommand):
    help = "Does a simple Greeting"

    def add_arguments(self, parser):
        parser.add_argument('name', type=str, help='Specifies the user name')

    
    def handle(self, *args, **kwargs):
        name = kwargs['name']
        greeting =  f'Hi, {name}, good morning'
        self.stdout.write(self.style.SUCCESS(greeting))
