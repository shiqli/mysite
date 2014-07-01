from django.conf.urls import patterns, include, url

from django.contrib import admin

from mysite.views import hello, hours_ahead

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mysite.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', hello),
    url(r'^time/plus/(\d+)/$', hours_ahead),
    url(r'^polls/', include('polls.urls', namespace="polls")),
    url(r'^books/', include('books.urls', namespace="books")),
    url(r'^admin/', include(admin.site.urls)),
)
