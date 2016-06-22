#coding=utf-8
from django.test import TestCase
from django.test import Client
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth.models import check_password
from django.core.urlresolvers import reverse
from accounts.forms import RegisterForm

PASSWORD = "test123456"

# Create your tests here.

class LoginPageTestCase(TestCase):
    #首先用setUp方法告诉测试之前应该做哪些事情,这时django会自动产生一个临时数据库
    def setUp(self):
        #创建一个可以登录的用户
        self.user = User.objects.create_user(username="test",email="test@123.com",password=PASSWORD)
        self.user.save()
        #创建一个no_active用户
        self.no_active_user = User.objects.create_user(username="test1",email="test1@123.com",password=PASSWORD)
        self.no_active_user.is_active=False
        self.no_active_user.save()
        #创建一个fail_username这是不存在的用户 
        self.fail_username = "testff"
        #enforce_csrf_checks=True
        #创建一个客户端
        self.client = Client()
    #定义测试用例
    def test_login_get(self):
        #获取请求
        response = self.client.get(reverse('accounts:login'))
        #请求后状态码返回200，说明请求成功
        self.assertEqual(response.status_code,200)

    def test_assertTrue(self):
        #这里assertTrue后边无值，测试时会出现一个错误
        self.assertEqual("")
    def test_assertFalse(self):
        self.assertFalse("")
        self.assertFalse(0)
        self.assertFalse(None)

    def test_login_post_correct(self):
        #POST request
	response = self.client.post(reverse('accounts:login'),{'username':self.user.username,'password':PASSWORD})
        #重定向，地址用url逆向解析
        self.assertEqual(response.status_code,302)
        self.assertRedirects(reponse,reverse('accounts:index'))
    def test_login_post_noactive(self):
        #POST request
        reponse=self.client.post(reverse('accounts:login'),{'username':self.no_active_user.username,'password':PASSWORD})
        self.assertEqual(response.status_code,200)
        self.assertEqual(response.context['error'],u'用户'+self.no_active_user.username+u'没有激活')
    def test_login_post_wrong(self):
        #POST request
        reponse = self.client.post(reverse('accounts:login'),{'username':self.fail_username,'password':PASSWORD})
        self.assertEqual(response.status_code,200)
        self.assertEqual(response.context['error'],u'用户'+self.fail_username+u'不存在')

class IndexPageTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testindex",email="test@123.com",password=PASSWORD)
        self.user.save()
        self.client = Client()

    def test_login_sucess(self):
        self.assertEqual(True,self.client.login(username=self.user.username,password=PASSWORD))
        response = self.client.get(reverse('accounts:index'))
        self.assertEqual(response.status_code,200)

    def test_nologin(self):
        reponse = self.client.get(reverse('accounts:index'))
        self.assertEqual(reponse.status_code,302)
        self.assertRedirects(reaponse,'/accounts/login/?next=/accounts/index')
#测试表单
class RegisterFormTestCase(TestCase):
    def setUp(self):
        self.correct_data = {"username":"test","email":"test@123.com",
                "password":PASSWORD,"re_password":PASSWORD}
    def test_empty(self):
        form=RegisterForm({})
        self.assertFalse(form.is_valid())
        self.assertTrue(form['username'].errors)
        self.assertTrue(form['email'].errors)
        self.assertTrue(form['password'].errors)
        self.assertTrue(form['re_password'].errors)
        self.assertTrue(form.non_field_erroes)
    def test_correct(self):
        form=RegisterForm(self.correct_data)
        self.assertTrue(form.is_valid())

#测试注册页面
class RegisterPageTestCase(TestCase):
    def setUp(self):
        self.correct_data = {"username":"test","email":"test@123.com",
                "password":PASSWORD,"re_password":PASSWORD}
        self.client = Client()

#测试一个空提交
    def test_empty(self):
        response = self.client.post(reverse('accounts:register'),{})
        self.assertTrue(response.context['form']['email'])
        self.assertTrue(response.context['form']['username'])


#测试一个正确的提交
    def test_correct(self):
        response = self.client.post(reverse('accounts:register'),self.correct_data)
        self.assertEqual(response.stattus_code,302)
        self.assertRedirects(response,reverse('accounts:index'))


        

