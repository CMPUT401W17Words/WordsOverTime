
from django.core.management.base import BaseCommand, CommandError
from words.databaseinput import run, enterdata

class Command(BaseCommand):
    help = 'Creates the database with the files provided. Use '

    def handle(self, *args, **options):
        sentPath = raw_input("Please input the Sentiment Dictionary Path: ")
        corpusPath = raw_input("Please input the Corpus Path: ")
        run(sentPath, corpusPath)
        self.stdout.write('Successfully generated database')
