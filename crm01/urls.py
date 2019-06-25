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

    # 注册登录重置密码
    url(r'^register/', views.register, name='register'),
    url(r'^login/', views.login, name='login'),
    url(r'^logout/', views.logout, name='logout'),
    url(r'^reset_psd/', views.reset_psd, name='reset_psd'),
    url(r'^get_cverification_code/', views.get_cverification_code, name='get_cverification_code'),

    # 首页
    url(r'^base/', views.base, name='base'),

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

    # 跟进记录
    url(r'^followrecord/$', views.Followrecord.as_view(), name='followrecord'),
    # 添加/编辑跟进记录（一个页面版本）
    url(r'^followrecord/add/', views.Add_Edit_Followrecord.as_view(), name='addfollowrecord'),
    url(r'^followrecord/edit/(\d+)/', views.Add_Edit_Followrecord.as_view(), name='editfollowrecord'),
    # 跟进记录删除，详情
    url(r'^followrecord/delete/(\d+)/', views.DeleteFollowrecord.as_view(), name='deletefollowrecord'),
    url(r'^followrecord/more/(\d+)/', views.Followrecord.as_view(), name='morefollowrecord'),

    # 学生信息
    url(r'^student/$', views.Student.as_view(), name='student'),
    url(r'^student/add/', views.Add_Edit_Student.as_view(), name='addstudent'),
    url(r'^student/edit/(\d+)/', views.Add_Edit_Student.as_view(), name='editstudent'),
    url(r'^student/delete/(\d+)/', views.DeleteStudent.as_view(), name='deletestudent'),

    # 教学信息
    url(r'^teach/$', views.Teach.as_view(), name='teach'),
    url(r'^teach/add/', views.Add_Edit_Teach.as_view(), name='addteach'),
    url(r'^teach/edit/(\d+)/', views.Add_Edit_Teach.as_view(), name='editteach'),
    url(r'^teach/delete/(\d+)/', views.DeleteTeach.as_view(), name='deleteteach'),

    # 学习情况详情(批量操作：原生版和formset版)
    url(r'^studydetail/(\d+)', views.Studydetail.as_view(), name='studydetail'),

    # 学习信息
    url(r'^study/$', views.Study.as_view(), name='study'),
    url(r'^study/add/', views.Add_Edit_Study.as_view(), name='addstudy'),
    url(r'^study/edit/(\d+)/', views.Add_Edit_Study.as_view(), name='editstudy'),
    url(r'^study/delete/(\d+)/', views.DeleteStudy.as_view(), name='deletestudy'),
    url(r'^study/more/(\d+)/', views.Study.as_view(), name='morestudy'),

    # 用户信息管理
    url(r'^user/list/$', views.UserList.as_view(), name='user_list'),
    url(r'^user/add/', views.Add_Edit_User.as_view(), name='user_add'),
    url(r'^user/edit/(\d+)/', views.Add_Edit_User.as_view(), name='user_edit'),
    url(r'^user/delete/(\d+)/', views.DeleteUser.as_view(), name='user_delete'),
    url(r'^userpwd_ret/(\d+)/', views.userpwd_ret, name='userpwd_ret'),

    # 角色信息管理
    url(r'^role/list/$', views.RoleList.as_view(), name='role_list'),
    url(r'^role/add/', views.Add_Edit_Role.as_view(), name='role_add'),
    url(r'^role/edit/(\d+)/', views.Add_Edit_Role.as_view(), name='role_edit'),
    url(r'^role/delete/(\d+)/', views.DeleteRole.as_view(), name='role_delete'),
    url(r'^user/list/role/$', views.UserList.as_view(), name='user_list_role'),

    # 权限信息管理
    url(r'^permission/list/$', views.PermissionList.as_view(), name='permission_list'),
    url(r'^permission/add/', views.Add_Edit_Permission.as_view(), name='permission_add'),
    url(r'^permission/edit/(\d+)/', views.Add_Edit_Permission.as_view(), name='permission_edit'),
    url(r'^permission/delete/(\d+)/', views.DeletePermission.as_view(), name='permission_delete'),

    # 菜单信息管理
    url(r'^menu/list/$', views.MenuList.as_view(), name='menu_list'),
    url(r'^menu/add/', views.Add_Edit_Menu.as_view(), name='menu_add'),
    url(r'^menu/edit/(\d+)/', views.Add_Edit_Menu.as_view(), name='menu_edit'),
    url(r'^menu/delete/(\d+)/', views.DeleteMenu.as_view(), name='menu_delete'),
    url(r'^permission/list/menu/$', views.PermissionList.as_view(), name='permission_list_menu'),

    # 权限分配
    url(r'^permission/distribute/$', views.PermissionDistribute.as_view(), name='permission_distribute'),


]
