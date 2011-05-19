from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'alertme.views.home', name='home'),
    url(r'^$', 'alertme.accounts.views.login_view', name='login_view'),
    # url(r'^alertme/', include('alertme.foo.urls')),

    url(r'^register', 'alertme.accounts.views.signup', name='signup'),
    #url(r'^login', 'django.contrib.auth.views.login', {'template_name': 'registration/login.html'}),
    #url(r'^login', 'alertme.accounts.views.login_status', name='login_status'),
    url(r'^login', 'alertme.accounts.views.login_view', name='login_view'),
    url(r'^logout', 'alertme.accounts.views.logout_view', name='logout_view'),
    #redirect to this url after user logs in
    url(r'^home', 'alertme.accounts.views.home', name='home'),
    url(r'^settings', 'alertme.accounts.views.user_settings', name='user_settings'),
    url(r'^alerts', 'alertme.accounts.views.user_alerts', name='user_alerts'),
    url(r'^invalid', 'alertme.accounts.views.invalid', name='invalid'),
    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
