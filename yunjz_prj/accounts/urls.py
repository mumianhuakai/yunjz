#coding=utf-8
from django.conf.urls import patterns,include,url
from django.contrib import admin
from accounts import views

admin.autodiscover()
#创建url与views.py中对应的调用数据库中数据的函数之间的映射
urlpatterns=patterns('',

	url(r'^index',views.index,name='index'),
	url(r'^login',views.login,name='login'),
	url(r'^logout',views.logout,name='logout'),
	url(r'^register',views.register,name='register'),
)






