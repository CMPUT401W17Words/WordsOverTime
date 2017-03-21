
from django.core.management.base import BaseCommand, CommandError
from words.databaseinput import run

class Command(BaseCommand):
    help = 'Creates the database'



    def handle(self, *args, **options):
        
        run()
        self.stdout.write('Successfully generated database')
