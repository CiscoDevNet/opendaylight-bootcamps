from django.conf.urls import patterns, include, url
from django.contrib import admin
import settings

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'odlcontroller.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', 'opt_routes.views.index', name='index'),
    url(r'^applist/$', 'opt_routes.views.applist', name='applist' ),
    url(r'^emu/$', 'emulator.views.emu', name='emu' ),
    
    url(r'^add/$', 'opt_routes.views.add', name='add' ),
    url(r'^add2/$', 'opt_routes.views.add2', name='add2' ),
    url(r'^addroutes/$', 'opt_routes.views.addroutes', name='addroutes' ),
    url(r'^admin/', include(admin.site.urls)),
    url( r'^static/(?P<path>.*)$', 'django.views.static.serve',{ 'document_root': settings.STATIC_URL }),
    url(r'^test/$', 'opt_routes.views.test', name='test'), 
    url(r'^appdetail/$', 'opt_routes.views.appdetail', name='appdetail'),
    url(r'^changeState/$', 'opt_routes.views.changeState', name='changeState' ),
)

