from django.core.management.base import BaseCommand, CommandError
from django.core.exceptions import ValidationError
from dateutil.parser import parse
from django.utils import dateparse
from emails.models import Email, EmailReference

import time
import os
import sys


# Location where the archive email files are stored
ARCHIVE_DIR = os.path.dirname(os.path.dirname(__file__))
ARCHIVE_DIR = os.path.join(ARCHIVE_DIR, '../../archive/files')

# Indicates the end of an email's contents
EMAIL_END_TEXT = '-------------- next part --------------'

fnames = ['2007-December.txt', '2008-January.txt', '2008-February.txt',]

class Command(BaseCommand):
	help = 'Load email data from archive file(s) into the model'

	def handle(self, *args, **options):
		fnames = self.file_names()

		for f in fnames:
			#print f
			fname = os.path.join(ARCHIVE_DIR, f)

			if os.path.isfile(fname):
				self.stdout.write('Loading ' + f)
				self.load_data(fname)


	def load_data(self, fname):
		with open(fname, 'r') as afile:
			is_beginning_of_file = True
			are_headers_over = False
			is_body_over = False

			email = ''
			name = ''
			e_date = ''
			subject = ''
			body = ''
			msg_id = ''

			in_reply = None
			all_references = None

			for line in afile:
				if is_beginning_of_file:
					is_beginning_of_file = False

				if are_headers_over:
					# Email body begins
					if line.startswith(EMAIL_END_TEXT):
						are_headers_over = False
						is_body_over = True
					else:
						body += line
				else:
					is_body_over = False

					if line.startswith('From:'):
						email, name = self.get_email_and_name(line)

					#if line.startswith('Date:'):
					if line.startswith('From '):
						# The date mentioned in this field does not use
						# local timezone. Hence, this date would give the
						# correct time ordering.
						# TODO: Incorporate time zone with the email date
						e_date = self.get_date(line)

					if line.startswith('Subject:'):
						subject = line.split(':')[1].strip(). \
									replace('?UTF-8?Q?', '').replace('?=', '')

					if line.startswith('In-Reply-To:'):
						in_reply = line.split(':')[1].strip() \
							.replace('<', '').replace('>', '')

					if line.startswith('References:'):
						all_references = self.get_all_references(line)

					if line.startswith('Message-ID:'):
						msg_id = line.split(':')[1].strip() \
							.replace('<', '').replace('>', '')

						# Message ID is the last header that appears in an email
						are_headers_over = True

				if is_body_over:
					# Save this email into the model (database)
					if email and msg_id:
						# If there is any multi-part message (perhaps in case
						# of a message digest?), the 'From ' part is missing.
						# So, can't obtain the (timezone free) date in this case
						# TODO: Fix this
						if e_date:
							#print 'Saving email', email, name, msg_id, in_reply, \
							#		all_references
							new_email = self.save_email(email, name, e_date, \
											subject, body, \
											msg_id, in_reply, all_references)
							self.save_references(new_email, all_references)

					# Reset all the fields to store the next entry
					email = ''
					name = ''
					e_date = ''
					subject = ''
					body = ''
					msg_id = ''

					in_reply = None
					all_references = None

			# Save the last email from the file -- this didn't end with the
			# EMAIL_END_TEXT
			if email and msg_id:
				# If there is any multi-part message (perhaps in case
				# of a message digest?), the 'From ' part is missing.
				# So, can't obtain the (timezone free) date in this case
				# TODO: Fix this
				if e_date:
					#print 'Saving email', email, name, msg_id, in_reply, all_references
					new_email = self.save_email(email, name, e_date, subject, \
								body, msg_id, in_reply, all_references)
					self.save_references(new_email, all_references)


	def get_email_and_name(self, text):
		# Get the email address, name
		email_and_name = text.split(':')[1].split('(')
		#print email_and_name
		# A particular email address was in this format
		email = email_and_name[0].strip().replace(' at ', '@'). \
					replace('?UTF-8?Q?', '').replace('?=', '')
		name = None
		if len(email_and_name) > 1:
			name = email_and_name[1].strip().replace(')', '')

		return (email, name)


	def get_date(self, text):
		e_date = text.strip().split(' ')[4:]
		e_date = ' '.join(e_date)
		e_date = parse(e_date)

		return e_date


	def get_all_references(self, text):
		all_references = text.split(':')[1].strip().replace('<', '')
		# There could be multiple references
		all_references = all_references.split('>')
		# Skip the last empty item
		all_references = all_references[:len(all_references)-1]

		return all_references


	def save_email(self, email, name, e_date, subject, body, msg_id, in_reply, all_references):
		new_email = Email(email_from=email, email_from_name=name, \
						email_date=e_date, subject=subject, body=body, \
						message_id=msg_id, in_reply_to=in_reply)

		try:
			new_email.full_clean()
			new_email.save()
			#print 'Saved email', msg_id
		except ValidationError as e:
			# Do something based on the errors contained in e.message_dict.
			# Display them to a user, or handle them programatically.
			self.stderr.write('Failed to save email! ' + str(e))
			#sys.exit(1)

		return new_email


	def save_references(self, email, all_references):
		if all_references:
			for ref in all_references:
				#print 'Ref:', ref
				try:
					new_reference = EmailReference(email_id=email, \
								reference_id= \
								Email.objects.get(message_id__exact=ref.strip()))
				except Email.DoesNotExist as dne:
					self.stderr.write('Error: ' + str(dne) + ' ' + str(email) + \
									  ' ' + str(ref))
					new_reference = None

				if new_reference:
					try:
						new_reference.full_clean()
						new_reference.save()
						#print 'Saved ref', new_reference
					except ValidationError as refe:
						self.stderr.write('Failed to save reference(s) ' \
								  + str(refe))
						#sys.exit(1)


	def file_names(self):
		years = [2014,]
		months = ['January', 'February', 'March', 'April', 'May', 'June', \
				  'July', 'August', 'September', 'October', 'November', 'December',]

		names = [str(y) + '-' + m + '.txt' for y in years for m in months]
		return names
