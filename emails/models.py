from django.db import models
from django.core import urlresolvers


class Email(models.Model):
	email_from = models.EmailField()
	email_from_name = models.CharField(default=None, blank=True, null=True, max_length=200)
	email_date = models.DateTimeField('date posted')
	subject = models.CharField(max_length=200)
	body = models.TextField()
	message_id = models.CharField(max_length=200, unique=True)

	in_reply_to = models.CharField(default=None, blank=True, null=True, max_length=200)
	#references = models.CharField(default=None, blank=True, null=True, max_length=200)


	def __unicode__(self):
		return self.message_id + ': ' + self.subject
	
	def display_email(self):
		return self.email_from.replace('@', ' AT ')

	def get_absolute_url(self):
		return urlresolvers.reverse('show_details', args=[self.pk])


#class EmailReply(models.Model):
#	email_id = models.ForeignKey(Email, to_field='message_id')
#	reply_email_id = models.ForeignKey(Email, to_field='message_id')


class EmailReference(models.Model):
	email_id = models.ForeignKey(Email, related_name='msg_id')
	#reference_id = models.CharField(max_length=200)
	reference_id = models.ForeignKey(Email, related_name='ref_id')
	
	
	def __unicode__(self):
		return self.reference_id.subject
