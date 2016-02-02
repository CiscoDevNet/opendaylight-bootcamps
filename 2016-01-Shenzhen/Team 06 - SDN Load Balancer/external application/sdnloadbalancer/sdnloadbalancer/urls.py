from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    # Examples:
    # url(r'^$', 'sdnloadbalancer.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'openflowmanager.views.index'),
    url(r'^addservice$', 'openflowmanager.views.add_virtual_service'),
    url(r'^backends', 'openflowmanager.views.add_backend_servers'),
    url(r'^clients', 'openflowmanager.views.add_clients'),
    url(r'^packetin', 'openflowmanager.views.packetin'),
    url(r'^delvirtualservice/(?P<serid>\d+)/',
        'openflowmanager.views.delvirtualservice'),
    url(r'^delclient/(?P<clientid>\d+)/', 'openflowmanager.views.del_client'),
    url(r'^delbackendserver/(?P<serverid>\d+)/',
        'openflowmanager.views.del_backend_servers'),

]
