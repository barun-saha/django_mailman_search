from django.contrib import admin
from emails.models import Email, EmailReference

class EmailAdmin(admin.ModelAdmin):
	list_display = ('subject', 'email_date', 'email_from', 'message_id', 'in_reply_to',)

admin.site.register(Email, EmailAdmin)


class EmailReferenceAdmin(admin.ModelAdmin):
		list_display = ('email_id', 'reference_id',)
						
admin.site.register(EmailReference, EmailReferenceAdmin)