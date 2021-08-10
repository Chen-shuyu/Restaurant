"""djangoProject URL Configuration

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

from allenapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^hello/$', views.hello, name='hello'),
    url(r'^login/$', views.login, name='login'),
    url(r'^crudops/$', views.crudops),
    #url(r'^connection/', TemplateView.as_view(template_name = 'login.html'))
    url(r'^connection/$', views.formView),
    url(r'^articles/(?P<month>\d{2})/(?P<year>\d{4})/', views.viewArticles, name='articles'),
    #url(r'^articles/(?P<month>\d{2})/(?P<year>\d{4})/', cache_page(60 * 15)(views.viewArticles), name='articles'),
    #url(r'^simpleemail/(?P<emailto>[\w.%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4})/',
    #    views.sendSimpleEmail, name='sendSimpleEmail'),
    #url(r'^massEmail/(?P<emailto1>[\w.%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4})/(?P<emailto2>[\w.%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4})',
    #   views.sendMassEmail, name='sendMassEmail'),
    #url(r'^sendAdminsEmail/', views.sendAdminsEmail, name='sendAdminsEmail'),
    #url(r'^sendManagersEmail/', views.sendManagersEmail, name='sendManagersEmail'),
    #url(r'^sendHttpEmail/(?P<emailto>[\w.%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4})/', views.sendHttpEmail,
    #    name='sendHttpEmail'),
    #url(r'^profile/', TemplateView.as_view(template_name='profile.html')),
    #url(r'^saved/', views.SaveProfile, name='SaveProfile'),

    #url(r'^%s/' % settings.DAJAXICE_MEDIA_PREFIX, include('dajaxice.urls')),
    url(r'^profile/', TemplateView.as_view(template_name='profile.html')),
    url(r'^saved/', views.SaveProfile, name='SaveProfile'),
    url(r'^bootstrapSample/', views.bootstrapSample, name='bootstrapSample'),
    url(r'^pixnetSample/', views.pixnetSample, name='pixnetSample'),
    url(r'^fireBaseDBtest/', views.fireBaseDBtest, name='fireBaseDBtest'),

    url(r'^$', TemplateView.as_view(template_name='index.html')),
    url(r'^(\d+)/$', views.index, name='index'),
    url(r'^Delicacy/$', views.Delicacy, name='Delicacy'),
    #url(r'^generic/', TemplateView.as_view(template_name='generic.html')),
    url(r'^boardpost/$', views.boardpost, name='BoardPost'),
    url(r'^boardlist/$', views.boardlist, name='BoardList'),
    url(r'^boardlist/(\w+)/$', views.boardlist, name='BoardList'),
    url(r'^(\d+)/boardlist/(\w+)/$', views.boardlist2, name='BoardList'),
    url(r'^logout/$', views.logout, name='logout'),
]

urlpatterns += staticfiles_urlpatterns()