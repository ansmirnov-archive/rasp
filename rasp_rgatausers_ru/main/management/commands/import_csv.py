from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
	args = '<CSV filename>'
	help = 'Import database from CSV file'

	def handle(self, *args, **options):
		return
