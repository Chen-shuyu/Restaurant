from django.conf.urls import url
from django.urls import path, include

from myapp import views

urlpatterns = [
    # url(r'^hello', views.hello),
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