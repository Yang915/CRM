from django.utils.deprecation import MiddlewareMixin
from django.urls import reverse
from django.shortcuts import HttpResponse, redirect, render
import re


class PermissionMiddleware(MiddlewareMixin):
    def process_request(self, request):
        url_list = [reverse('login'),reverse('logout'), reverse('register'), reverse('reset_psd'), reverse('get_cverification_code'),
                    '/admin/.*']
        for url in url_list:
            if re.search(f'^{url}$', request.path):
                return None
        else:
            if request.user.is_authenticated:
                try:#因为使用的是django内置auth，在登录admin之后，直接访问时由于auth.login并不会将权限写入session，直接读取会报错
                    # for url in request.session['permission_list']:
                    for permission_dic in request.session['permission_list']:#二级菜单内操作时菜单显示处理需要在改变了权限列表数据结构
                        url=permission_dic['url']

                        if re.search(f'^{url}$', request.path):
                            request.pid=permission_dic['pid']#获取当前权限pid，赋值给request对象，以便在菜单渲染时调用
                            return None
                    else:
                        return HttpResponse('无此权限！')
                except Exception as e:
                    return redirect('login')
            else:
                return redirect('login')
