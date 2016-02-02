"""odlsc URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from service.views import myView, showNodes, showTemplate, showInstance, showBinding
from service.views import addtemplate, addins, addbind
from PIL.ImageShow import Viewer

db_str = "sqlite:///odltest.db"
ctrl_ip = "120.52.145.138"
viewer = myView(db_str, ctrl_ip)

# urlpatterns = [
#     url(r'^admin/', admin.site.urls),
#     url(r'^shownodes/', showNodes),
#     url(r'^showtemp/', showTemplate),
#     url(r'^showins/', showInstance),
#     url(r'^showbind/', showBinding),
#     
#     url(r'^addtmp$', addtemplate),
#     url(r'^addins$', addins),
#     url(r'^addbind$', addbind),
# ]

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^shownodes/', viewer.showNodes),
    url(r'^showtemp/', viewer.showTemplate),
    url(r'^showins/', viewer.showInstance),
    url(r'^showbind/', viewer.showBinding),
    
    url(r'^addtmp$', viewer.addtemplate),
    url(r'^addins$', viewer.addins),
    url(r'^addbind$', viewer.addbind),
    
    url(r'^updateType$', viewer.updateType),
]
