#coding=utf-8
#django package
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.template.context import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login as auth_login,logout as auth_logout
from django.core.urlresolvers import reverse
from accounts.forms import RegisterForm
#用户的主界面可以用装饰符装饰一下，这样只有登录成功才能进入主页，登录不成
#功被重定向到settings设置中的LOGIN_REDIRECT_URL='/accounts/'中的url
@login_required
def index(request):
	return render(request,"accounts/index.html")

def register(request):
	template_var={}
	form=RegisterForm()
	if request.method == "POST":
	    #使用表单时直接request.POST.copy()这样把POST数据copy一份给表单
	    form=RegisterForm(request.POST.copy())
	    #生成表单之后，调用is_valid检查它的正确性，把clean那些数据全部执行
	    #一遍，把error信息全部放在form里,放进区之后怎么表现出来？
	    if form.is_valid():
	        username=form.cleaned_data["username"]
	        email=form.cleaned_data["email"]
		password=form.cleaned_data["password"]
		#获得用户名、密码、email后用这三者为参数创建用户
	        user=User.objects.create_user(username,email,password)
		#创建好用户之后要保存倒数据库中
	        user.save()
	        if _login(request,username,password,template_var):
	            return HttpResponseRedirect("/accounts/index")
	#把form中的错误信息填到模板对应得变量中,就可以在模板templates/accounts/
	#对应的html文件中展示出错误信息
	template_var["form"]=form
	return render(request,"accounts/register.html",template_var)

def login(request):
	template_var={}
	if request.method == "POST":
	    #获取用户填入的数据，获取数据后就可以对它进行判断
	    username = request.POST.get("username")
	    password=request.POST.get("password")
	    if _login(request,username,password,template_var):
	        try:
	            tmp=request.GET["next"]
	            return HttpResponseRedirect(tmp)
	        except:
	            return HttpResponseRedirect("/accounts/index")
	    template_var.update({"username":username})
	return render(request,"accounts/login.html",template_var)
def _login(request,username,password,dict_var):
	ret=False
	#authenticate(username="",password="")方法对明文密码进行加密
	uesr=authenticate(username=username,password=password)
	if user is not None:
		if user.is_active:
		    #登录与会话有关，把user信息存到会话中
		    auth_login(request,user)
		    ret=True
		else:
		    dict_var["error"] = u'用户'+username+u'不存在'
		return ret
def logout(request):
	#把存到会话中的用户信息删除
	auth_logout(request)
	return render(request,'accounts/logout.html')


