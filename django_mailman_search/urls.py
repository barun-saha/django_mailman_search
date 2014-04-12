from django.conf.urls import patterns, include, url
from django.contrib import admin
from haystack.forms import SearchForm
from haystack.views import SearchView

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'django_mailman_search.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^search/$', SearchView(form_class=SearchForm)),
    url(r'^emails/', include('emails.urls')),
)
