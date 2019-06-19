from django import template
import re

register = template.Library()


# #一级菜单（直接显示权限操作）
# @register.inclusion_tag('menu.html')
# def menu_tag(request):
#     for menu_dic in request.session['permission_menu_list']:
#         url=menu_dic['url']
#         if re.search(f"^{url}$", request.path):
#             menu_dic['class'] = 'active'
#             break
#     return {'menu_list': request.session['permission_menu_list']}

#
# # 二级菜单：对权限显示进行归属划分（存在问题，只能显示菜单，菜单内的功能点击，左边菜单不在显示）
# @register.inclusion_tag('menu.html')
# def menu_tag(request):
#     for menu_level1 in request.session['menu_list'].values():
#         menu_level1['class'] = 'treeview'#自带样式一级菜单显示，二级隐藏
#
#         for menu_level2 in menu_level1['menu_level2_list']:
#
#             url= menu_level2['url']#二级菜单（要显示的权限）url
#             if re.search(f'^{url}$',request.path):#判断当前请求路径为显示的权限菜单以及内部操作
#                 menu_level1['class']='treeview menu-open'#自带样式一级菜单显示，二级也显示
#                 menu_level1['flag'] = True#二级菜单样式display:block判断展示标志
#                 menu_level2['class']='active'
#                 break
#
#     print('>>>>>>>>>', request.session['menu_list'])
#     return {'menu_list': request.session['menu_list']}


# 二级菜单：对权限显示进行归属划分，权限内部功能操作权限菜单正常显示
# 1.将不同权限内的操作归属于相应的权限显示菜单，即在permission权限表中增加字段pid关联到当前权限显示记录（关联是否均可，如下if判断有差别）的id，;
# 2.重新在session中注入权限（url和pid）和菜单(一级菜单的名称，样式，和对应的权限子菜单列表（名称，url，id)）（可以在自定义标签渲染时每次读取数据库表判断，这种方式不建议）
# 3. 确定每次请求的路径在权限内并找到对应的pid（可以在中间件权限验证是获取并赋给request.pid）,同时与权限显示的记录id进行判断（即如下的if），如果相等，则设置菜单的激活样式
@register.inclusion_tag('menu.html')
def menu_tag(request):
    for menu_level1 in request.session['menu_level1_dict'].values():
        menu_level1['class'] = 'treeview'#自带样式一级菜单显示，二级隐藏

        for menu_level2 in menu_level1['menu_level2_list']:

            url= menu_level2['url']#二级菜单（要显示的权限）url
            pk=menu_level2['pk']

            if re.search(f'^{url}$',request.path) or request.pid==pk:#判断当前请求路径为显示的权限菜单以及内部操作
                menu_level1['class']='treeview menu-open'#自带样式一级菜单显示，二级也显示
                menu_level1['flag'] = True#二级菜单样式display:block判断展示标志
                menu_level2['class']='active'
                break

    print('>>>>>>>>>', request.session['menu_level1_dict'])
    return {'menu_list': request.session['menu_level1_dict']}