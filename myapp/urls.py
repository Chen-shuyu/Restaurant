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


]