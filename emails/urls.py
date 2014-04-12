from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from emails import views


urlpatterns = patterns('',
	url(r'^(?P<eid>\d+)/$', views.show_details, name='show_details'),
	url(r'^$', TemplateView.as_view(template_name="index.html")),
)
