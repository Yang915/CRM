"""crm01 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
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
from app01 import views

urlpatterns = [

    url(r'^admin/', admin.site.urls),
    url(r'^register/', views.register, name='register'),
    url(r'^login/', views.login, name='login'),
    url(r'^logout/', views.logout, name='logout'),
    url(r'^reset_psd/', views.reset_psd, name='reset_psd'),
    url(r'^get_cverification_code/', views.get_cverification_code, name='get_cverification_code'),

    url(r'^base/', views.base, name='base'),

    # 公户/私户获取（两个页面版本）
    # url(r'^customers/', views.Customers.as_view(), name='customers'),
    # url(r'^mycustomers/', views.mycustomers, name='mycustomers'),

    # 公户添加/编辑操作（两个页面版本）
    # url(r'^customer/add/', views.AddCustomer.as_view(), name='addcustomer'),
    # url(r'^customer/edit/(\d+)/', views.EditCustomer.as_view(), name='editcustomer'),

    # 公户/私户:获取/查询/批量处理（一个页面版本）
    url(r'^customer/$', views.Public_Private_Customers.as_view(), name='customers'),
    url(r'^mycustomer/$', views.Public_Private_Customers.as_view(), name='mycustomers'),

    # 客户添加/编辑操作（一个页面版本）
    url(r'^customer/add/', views.Add_Edit_Customer.as_view(), name='addcustomer'),
    url(r'^mycustomer/add/', views.Add_Edit_Customer.as_view(), name='addmycustomer'),

    url(r'^customer/edit/(\d+)/', views.Add_Edit_Customer.as_view(), name='editcustomer'),
    url(r'^mycustomer/edit/(\d+)/', views.Add_Edit_Customer.as_view(), name='editmycustomer'),

    # 公户/私户删除操作
    url(r'^customer/delete/(\d+)/', views.Deletecustomer.as_view(), name='deletecustomer'),
    url(r'^mycustomer/delete/(\d+)/', views.Deletecustomer.as_view(), name='deletemycustomer'),


    url(r'^followrecords/', views.Followrecord.as_view(), name='followrecord'),
    # 添加/编辑跟进记录（两个页面版本）
    # url(r'^followrecord/add/', views.AddFollowrecord.as_view(), name='addfollowrecord'),
    # url(r'^followrecord/edit/(\d+)/', views.EditFollowrecord.as_view(), name='editfollowrecord'),
    url(r'^followrecord/add/', views.Add_Edit_Followrecord.as_view(), name='addfollowrecord'),
    url(r'^followrecord/edit/(\d+)/', views.Add_Edit_Followrecord.as_view(), name='editfollowrecord'),
    url(r'^followrecord/delete/(\d+)/', views.DeleteFollowrecord.as_view(), name='deletefollowrecord'),
    url(r'^followrecord/more/(\d+)/', views.Followrecord.as_view(), name='morefollowrecord'),

]
