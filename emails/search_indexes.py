import datetime
from haystack import indexes
from emails.models import Email

class EmailIndex(indexes.SearchIndex, indexes.Indexable):
	text = indexes.CharField(document=True, use_template=True)

	email_from = indexes.CharField(model_attr='email_from')
	email_from_name = indexes.CharField(model_attr='email_from_name', null=True)
	email_date = indexes.DateTimeField(model_attr='email_date')
	subject = indexes.CharField(model_attr='subject')
	body = indexes.CharField(model_attr='body')
	message_id = indexes.CharField(model_attr='message_id')
	in_reply_to = indexes.CharField(model_attr='in_reply_to', null=True)
	

	def get_model(self):
		return Email

	def index_queryset(self, using=None):
		"""Used when the entire index for model is updated."""
		return self.get_model().objects.filter(email_date__lte=datetime.datetime.now())
