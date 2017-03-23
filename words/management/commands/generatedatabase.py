
from django.core.management.base import BaseCommand, CommandError
from words.databaseinput import run, enterdata

class Command(BaseCommand):
    help = 'Creates the database'

    def add_arguements(self, parser):
        parser.add_arguement('-f', action = 'store', type = 'string', default = False, dest = 'filename')

    def handle(self, *args, **options):
        
        if options.f:
            csvpath = options.f
            enterdata(csvpath)
        else:
            run()
        self.stdout.write('Successfully generated database')
