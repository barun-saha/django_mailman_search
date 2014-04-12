from django.core.management.base import BaseCommand, CommandError
from emails.models import Email, EmailReference


class Command(BaseCommand):
	help = 'Clear all loaded data'

	def handle(self, *args, **options):
		# Sqlite can't handle more than 999 records at a time
		#Email.objects.all().delete()
		# The solution below is only for sqlite
		# http://stackoverflow.com/a/18181477/147021
		while Email.objects.count():
			ids = Email.objects.values_list('pk', flat=True)[:100]
			Email.objects.filter(pk__in = ids).delete()
