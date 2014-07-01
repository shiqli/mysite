from django.conf.urls import patterns, url

from polls import views

urlpatterns = patterns('',
	# ex: /polls/
	url(r'^$', views.IndexView.as_view(), name='index'),
	# ex:/polls/5/
	url(r'^(?P<pk>\d+)/$', views.DetailView.as_view(), name='detail'),
	# ex:/polls/5/results/
	url(r'^(?P<pk>\d+)/results/$', views.ResultsView.as_view(), name='results'),
	# ex:/polls/5/vote/
	url(r'^(?P<poll_id>\d+)/vote/$', views.vote, name='vote'),
	url(r'^time_now/$',views.time_now,name='time_now'),
	url(r'^displayVoter/$',views.displayVoter),
	url(r'^displayMeta/$',views.display_meta),
)


