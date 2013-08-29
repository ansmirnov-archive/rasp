from django.core.management.base import BaseCommand, CommandError
from main import utils

class Command(BaseCommand):
    args = '<CSV filename>'
    help = 'Import database from CSV file'

    def handle(self, *args, **options):
        try:
            fn = args[0]
            utils.import_csv(fn)
        except (IndexError, IOError):
            print "Could not open file"
            return

        return
