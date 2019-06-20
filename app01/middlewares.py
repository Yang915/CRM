from django.utils.deprecation import MiddlewareMixin
from django.urls import reverse
from django.shortcuts import HttpResponse, redirect, render
import re


class PermissionMiddleware(MiddlewareMixin):
    def process_request(self, request):
        url_list = [reverse('login'), reverse('logout'), reverse('register'), reverse('reset_psd'),
                    reverse('get_cverification_code'),
                    '/admin/.*']
        for url in url_list:
            if re.search(f'^{url}$', request.path):
                return None
        else:
            if request.user.is_authenticated:
                breadcrumb_list = [{'url': reverse('base'), 'title': '首页'}]  # 面包屑（层架菜单的导航）

                try:  # 因为使用的是django内置auth，在登录admin之后，直接访问时由于auth.login并不会将权限permission_list写入session，直接读取会报错
                    # for url in request.session['permission_list']:
                    for permission_dic in request.session['permission_list']:  # 二级菜单内操作时菜单显示处理需要在改变了权限列表数据结构
                        url = permission_dic['url']

                        if re.search(f'^{url}$', request.path):
                            request.pid = permission_dic['pid']  # 获取当前权限pid，赋值给request对象，以便在菜单渲染时调用
                            # print('>>>>>+++',request.pid)

                            if permission_dic['pid']:#通过pid(权限归属父类的id,显示权限的pid为空)判断当前请求的pid如果存在则需要在面包屑列表中添加其归属的显示菜单项
                                for url_obj in request.session['permission_list']:
                                    if url_obj['pk'] == permission_dic['pid']:
                                        breadcrumb_list.append({'url': url_obj['url'], 'title': url_obj['name']})
                                        break
                            breadcrumb_list.append({'url': permission_dic['url'], 'title': permission_dic['name']})#添加当前请求到面包屑列表
                            # print('++++++',breadcrumb_list)
                            request.breadcrunmb=breadcrumb_list#将面包屑列表赋值给request对象的一个属性，在模板页面base中进行渲染

                            return None
                    else:
                        return HttpResponse('无此权限！')
                except Exception as e:
                    return redirect('login')
            else:
                return redirect('login')
