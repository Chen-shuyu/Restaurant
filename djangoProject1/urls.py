"""djangoProject1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path
from django.conf.urls import url
from django.views.generic import TemplateView

from myapp import views


urlpatterns = [
    path('admin/', admin.site.urls),

    url(r'^fireBaseDBtest/', views.fireBaseDBtest, name='fireBaseDBtest'),
    url(r'^signIn/', views.login, name='signIn'),
    url(r'^postsignIn/', views.postsignIn, name='postsignIn'),
    url(r'^enroll/', views.enroll, name='enroll'),
    url(r'^postsignUp/', views.postsignUp, name='postsignUp'),
    # path('certification/', include('views.certification')),
    url(r'^certification/([A-Za-z0-9]{16})/', views.certification, name='certification'),
    url(r'^logout/', views.logout, name='logout'),
    url(r'^reset/', views.reset, name='reset'),
    url(r'^postReset/', views.postReset, name='postReset'),
    url(r'^detail/', views.detail, name='detail'),
    url(r'^test/', views.test, name='test'),

    #============================================================================
    #============================================================================

    url(r'^$', TemplateView.as_view(template_name='index.html')),
    url(r'^(\d+)/$', views.index, name='index'),
    url(r'^Delicacy/$', views.Delicacy, name='Delicacy'),
    # url(r'^generic/', TemplateView.as_view(template_name='generic.html')),
    url(r'^boardpost/$', views.boardpost, name='BoardPost'),
    url(r'^boardlist/$', views.boardlist, name='BoardList'),
    url(r'^boardlist/(\w+)/$', views.boardlist, name='BoardList'),
    url(r'^(\d+)/boardlist/(\w+)/$', views.boardlist2, name='BoardList'),
    url(r'^logout/$', views.logout, name='logout'),
]

urlpatterns += staticfiles_urlpatterns()
