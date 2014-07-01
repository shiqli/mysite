from django.conf.urls import url, patterns
from books import views

urlpatterns = patterns('',
	url(r'^search-form/$', views.search_form),
	url(r'^search/$', views.search),
	url(r'^contact/thanks/$', views.thanks),
	url(r'^contact/$', views.contact),
)
