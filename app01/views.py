from django.shortcuts import render, HttpResponse, redirect
from app01.form import RegisterForm, CustomerModelForm, FollowrecordModelForm, StudentModelForm ,TeachModelForm,StudyModelForm # 自定义的form组件
from app01 import models  # 自定义的models模块
from django.http import JsonResponse  # Json响应数据类型
from django.urls import reverse  # url反向解析
from django.contrib import auth  # django内置认证系统
from django.contrib.auth.decorators import login_required  # 认证装饰器
from django.views import View  # CBV模式必须继承的类
from django.utils.decorators import method_decorator  # CBV视图装饰器
from django.db.models import Q  # orm查询选择条件操作
import json  # 序列化模块
import sys  # 系统模块
import re  # 正则


# 注册
def register(request):
    if request.method == 'GET':
        register_obj = RegisterForm()
        return render(request, 'register.html', {'register_obj': register_obj})
    elif request.method == 'POST':
        data = request.POST
        # print(data)
        register_obj = RegisterForm(data)
        if register_obj.is_valid():
            user_obj = register_obj.cleaned_data
            # print(user_obj)
            username = user_obj.get('name')
            password = user_obj.get('password')
            email = user_obj.get('email')

            if not models.UserInfo.objects.filter(username=username).exists():
                new_obj = models.UserInfo.objects.create_user(username=username, password=password, email=email)
                # print(f'新用户{username}注册成功！')
                return redirect('login')
            else:
                register_obj.add_error('name', '用户名已存在！')
                return render(request, 'register.html', {'register_obj': register_obj})

        else:
            return render(request, 'register.html', {'register_obj': register_obj})


# 随机验证码
def get_cverification_code(request):
    import os
    from crm01 import settings
    import random
    def get_random_color():
        '''
        随机颜色
        :return: rgb颜色
        '''
        return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    from PIL import Image, ImageDraw, ImageFont  # 要先安装pillow模块：pip install pillow
    img_obj = Image.new('RGB', (120, 40), get_random_color())  # 实例化图片对象
    draw_obj = ImageDraw.Draw(img_obj)  # 创建图片

    font_path = os.path.join(settings.BASE_DIR, r'static_files\fonts\BRUX.otf')  # 字体路径（字体自己下载）
    # print('>>>>', font_path)
    # font_obj = ImageFont.true type(font_path, 26)#路径拼接注意不能有中文，否则报错
    font_obj = ImageFont.truetype(r'static_files/fonts/BRUX.otf', 26)  # 相对路径r'static_files/fonts/BRUX.otf'
    # font_obj = ImageFont.load_default().font#系统默认字体
    sum_str = ''
    for i in range(6):  # 生成随机的字母数字组合
        a = random.choice([str(random.randint(0, 9)), chr(random.randint(97, 122)),
                           chr(random.randint(65, 90))])  # 4  a  5  D  6  S
        sum_str += a
    print('验证码>>>', sum_str)
    draw_obj.text((12, 2), sum_str, fill=get_random_color(), font=font_obj)

    width = 120
    height = 40
    # 添加噪线
    for i in range(5):  # 循环一次就是一条线：两点确定一条
        x1 = random.randint(0, width)
        x2 = random.randint(0, width)
        y1 = random.randint(0, height)
        y2 = random.randint(0, height)
        draw_obj.line((x1, y1, x2, y2), fill=get_random_color())
    # # 添加噪点
    for i in range(10):
        # 这是添加点，50个点
        draw_obj.point([random.randint(0, width), random.randint(0, height)], fill=get_random_color())
        # 下面是添加很小的弧线，看上去类似于一个点，50个小弧线
        x = random.randint(0, width)
        y = random.randint(0, height)
        draw_obj.arc((x, y, x + 4, y + 4), 0, 90, fill=get_random_color())

    from io import BytesIO  # 生成的图片格式指定和存在位置（缓存）
    f = BytesIO()
    img_obj.save(f, 'png')
    data = f.getvalue()

    # 验证码对应的数据保存到session里面
    request.session['valid_str'] = sum_str

    return HttpResponse(data)


# 登录
def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    elif request.method == 'POST':
        # print(request.POST)
        username = request.POST.get('username')
        password = request.POST.get('password')
        cverification_code = request.POST.get('cverification_code')

        if cverification_code.upper() == request.session.get('valid_str').upper():

            user_obj = auth.authenticate(username=username, password=password)
            print(user_obj)
            if user_obj:
                auth.login(request, user_obj)
                # 权限显示（一级菜单不划分归属）
                """
                user_permission_objs=models.Permission.objects.filter(role__userinfo__pk=request.user.pk).distinct()
                
                request.session['permission_list'] = [i.url for i in user_permission_objs]#注册权限
                print(request.session['permission_list'])
                
                request.session['permission_menu_list'] = [{'url': i.url, 'ico': i.ico, 'label': i.name} for i user_permission_objs if i.menu]#注册显示菜单
                print(request.session['permission_menu_list'])
                """

                # 权限归属划分（二级权限菜单划分归属一级菜单，存在问题：二级菜单内的操作时权限菜单显示异常）
                """
                user_role_permission_all=models.Permission.objects.filter(role__userinfo__pk=request.user.pk).distinct().values('pk','name','url','menu_id','menu__name','menu__ico')
                permission_list = []#权限表
                menu_level1_dict1_list={}#一级菜单
                for item in user_role_permission_all:
                    permission_list.append(item['url'])

                    if item['menu_id']:
                        if item['menu_id'] in menu_level1_list:
                            menu_level1_dict[item['menu_id']]['menu_level2_list'].append({
                                'name':item['name'],
                                'url':item['url']
                            } )
                        else:
                            menu_level1_dict[item['menu_id']]={
                                'name':item['menu__name'],
                                'ico':item['menu__ico'],
                                'menu_level2_list':[{
                                    'name':item['name'],
                                    'url':item['url']
                                } ]
                            }


                request.session['permission_list']=permission_list
                request.session['menu_level1_dict']=menu_level1_dict
                print(permission_list)
                print(menu_level1_dict)
                """

                # 权限归属划分（重新修改permission表结构，进行权限归属显示菜单划分，在session中注入权限和归属菜单的pid,以便在菜单样式渲染时进行判断,注意中间件权限认证）
                user_role_permission_all = models.Permission.objects.filter(
                    role__userinfo__pk=request.user.pk).distinct().values('pk', 'name', 'url', 'pid_id', 'menu_id',
                                                                          'menu__name', 'menu__ico')
                permission_list = []
                menu_level1_dict = {}
                for item in user_role_permission_all:
                    permission_list.append(
                        {'url': item['url'], 'pid': item['pid_id'], 'name': item['name'], 'pk': item['pk']})

                    if item['menu_id']:
                        if item['menu_id'] in menu_level1_dict:
                            menu_level1_dict[item['menu_id']]['menu_level2_list'].append(
                                {'name': item['name'], 'url': item['url'], 'pk': item['pk']})
                        else:
                            menu_level1_dict[item['menu_id']] = {'name': item['menu__name'], 'ico': item['menu__ico'],
                                                                 'menu_level2_list': [
                                                                     {'name': item['name'], 'url': item['url'],
                                                                      'pk': item['pk']}]
                                                                 }

                request.session['permission_list'] = permission_list
                request.session['menu_level1_dict'] = menu_level1_dict
                # print('>>>>>>>>>>>>>>>',permission_list)
                # print('>>>>>>>>>>>>>>>>>>>>>>>>>>',menu_level1_dict)

                return JsonResponse({'status': 1, 'url': reverse('base')})
            else:
                return JsonResponse({'status': 0, 'url': '账号或密码有误！'})
        else:
            return JsonResponse({'status': 0, 'url': '验证码输入有误！'})


# 注销
def logout(request):
    auth.logout(request)
    return redirect('login')


# 修改密码
def reset_psd(request):
    if request.user.is_authenticated:
        if request.method == 'GET':
            return render(request, 'reset_psd.html')
        elif request.method == 'POST':
            old_password = request.POST.get('old_password')
            new_password = request.POST.get('new_password')
            r_new_password = request.POST.get('r_new_password')
            # ret=request.user.check_password(old_password)
            # print(ret)
            if request.user.check_password(old_password):
                if new_password == r_new_password:
                    request.user.set_password(new_password)
                    request.user.save()
                    return JsonResponse({'status': True, 'info': '操作成功！', 'url': reverse('index')})
                else:
                    return JsonResponse({'status': False, 'info': '两次新密码不一致！', 'url': ''})
            else:
                return JsonResponse({'status': False, 'info': '操作失败：原密码输入有误！', 'url': ''})
        return JsonResponse({'status': False, 'info': '操作失败！', 'url': ''})

    else:
        return redirect('login')


# 进入系统页面
def base(request):
    return render(request, 'base.html')


# 批量删除操作
def batch_delete(request, model):
    '''
    对用户的ajax请求进行批量删除操作
    :param request: 请求对象
    :param model: 指定的数据表(models.类名)
    :return:返回处理状态
    '''
    id_list = json.loads(request.POST.get('id_list', ''))
    # print('>>>>>>>>>', id_list)
    ret = model.objects.filter(pk__in=id_list).delete()
    # print('>>>>', ret)
    if ret:
        return 1
    else:
        return 0


# 批量修改操作
def batch_update(request, model):
    '''
        对用户的ajax请求进行批量更新操作
        :param request: 请求对象
        :param model: 指定的数据表(models.类名)
        :return:返回处理状态
        '''
    id_list = json.loads(request.POST.get('id_list', ''))
    print('----------===========+++++++', request.POST)
    field = request.POST.get('filed')  # 获取更新字段为字符串（以下用**处理字典，或者用global()转）
    val = request.POST.get('val')  # 获取值
    print(id_list)
    print(field)
    print(val)

    ret = model.objects.filter(pk__in=id_list).update(**{field: val})  # 执行更新操作
    print('>>>>', ret)
    if ret:
        return 1
    else:
        return 0


# 获取公户/私户(查询/批量处理，一个页面public_private_customers.html)
class Public_Private_Customers(View):

    # 查询
    def get(self, request):
        # 通过请求路径判断当前是公户还是私户
        if request.path == reverse('customers'):
            flag = 0
            customer_objs = models.Customer.objects.all().filter(consultant__isnull=True)
        elif request.path == reverse('mycustomers'):
            flag = 1
            customer_objs = models.Customer.objects.all().filter(consultant=request.user)

        # print('__________++++++++++++++>>>>>>>>>>>>>', request.GET)
        field = request.GET.get('field')
        val = request.GET.get(field)
        if field and val:
            customer_objs = customer_objs.filter(**{field + '__contains': val})

        if customer_objs:
            # 导入分页模块
            from app01 import page
            per_page_counts = 8
            page_number = 5
            page_obj = page.PageNation(request.path,  # 当前路径
                                       request.GET.get('page', 1),  # 当前页
                                       customer_objs.count(),  # 信息总数量
                                       request,  # 请求对象(查询使用)
                                       per_page_counts,  # 每页显示信息数
                                       page_number)  # 显示页码个数
            customer_objs = customer_objs.order_by('-pk')[
                            page_obj.start_num:page_obj.end_num]  # 实例化分页对象之后，返回有数据的起止位置，倒序排便于新增后在第一条显示
            page = page_obj.page_html()  # 返回页码导航的具体html代码
            return render(request, 'public_private_customers.html',
                          {'customer_objs': customer_objs, 'page': page, 'flag': flag,
                           'allfields': CustomerModelForm(),
                           'batch_update_fields_list': ['sex', 'source', 'status', 'consultant'],
                           'search_fields_list': ['name', 'qq', 'sex', 'source', 'status', 'consultant']})
        else:
            page = '<h1>当前信息为空！</h1>'
            return render(request, 'public_private_customers.html',
                          {'customer_objs': customer_objs, 'page': page, 'flag': flag, })

    # 批量处理
    def post(self, request):
        # print(request.POST)
        # print(request.COOKIES)
        operation = request.POST.get('operation', '')
        id_list = request.POST.get('id_list', '')
        # id_list=json.loads(id_list)
        print(operation)
        # print('++++++++', id_list, type(id_list))

        status = False
        if operation and id_list:
            if hasattr(sys.modules[__name__], operation) and callable(getattr(sys.modules[__name__], operation)):
                status = getattr(sys.modules[__name__], operation)(request, models.Customer)
            elif hasattr(self, operation) and callable(getattr(self, operation)):
                status = getattr(self, operation)(request)

        return JsonResponse({'status': status, 'operaiton': operation})

    # 批量公户转私户
    def batch_public_private(self, request):
        id_list = json.loads(request.POST.get('id_list', ''))
        ret = models.Customer.objects.filter(pk__in=id_list).update(consultant=request.user)  # 执行更新操作
        print('>>>>', ret)
        if ret:
            return 1
        else:
            return 0

    # 批量私户转公户
    def batch_private_public(self, request):
        id_list = json.loads(request.POST.get('id_list', ''))
        ret = models.Customer.objects.filter(pk__in=id_list).update(consultant=None)  # 执行更新操作
        print('>>>>', ret)
        if ret:
            return 1
        else:
            return 0


# 公户/私户：添加/编辑（一个页面add_edit_customer.html）
class Add_Edit_Customer(View):

    # 获取添加/编辑页面add_edit_customer.html
    def get(self, request, id=None):
        '''
        添加和编辑的不同url请求get方式,通过id值判断操作：获取添加/编辑页面
        :param request: get请求对象
        :param id: 请求url匹配的参数，有参数为真则是编辑，默认关键字None则为添加
        :return:返回添加/编辑页面，渲染数据，flag标志判断确定页面标题
        '''
        customer_obj = models.Customer.objects.all().filter(pk=id).first()
        # 通过pk查询结果显示判断当前是添加还是编辑操作
        if customer_obj:
            flag = 1
        else:
            flag = 0
        # 判断当前请求是公户还是私户，以便确认左边栏的样式
        if re.match(reverse('mycustomers'), request.path):
            flag_aside = 1
        elif re.match(reverse('customers'), request.path):
            flag_aside = 0

        customer_obj = CustomerModelForm(instance=customer_obj)
        return render(request, 'add_edit_customer.html',
                      {'customer_obj': customer_obj, 'flag': flag, 'flag_aside': flag_aside})

    # 提交添加/编辑操作处理
    def post(self, request, id=None):
        '''
        添加和编辑的不同url请求post方式,通过id值判断操作：执行添加/编辑
        :param request: post请求对象
        :param id: 请求url匹配的参数，有参数为真则是编辑，默认关键字None则为添加
        :return: 重定向customers展示页面
        '''
        customer_obj = models.Customer.objects.filter(pk=id).first()
        if customer_obj:
            flag = 1
        else:
            flag = 0
        customer_obj = CustomerModelForm(request.POST, instance=customer_obj)
        if customer_obj.is_valid():
            print(customer_obj.cleaned_data)
            customer_obj.save()
            print("+++++>>>>>>>>>", request.path)
            # 通过路径判断当前是公户还是私户操作
            if re.match(reverse('mycustomers'), request.path):
                return redirect("mycustomers")
            elif re.match(reverse('customers'), request.path):
                return redirect("customers")
        else:
            return render(request, 'add_edit_customer.html', {'customer_obj': customer_obj, 'flag': flag})


# 单个删除客户信息
class Deletecustomer(View):

    def get(self, request, id):
        print(id)
        models.Customer.objects.filter(pk=id).delete()
        # 通过路径判断当前是公户还是私户操作
        if re.match(reverse('mycustomers'), request.path):
            return redirect("mycustomers")
        elif re.match(reverse('customers'), request.path):
            return redirect("customers")


# 获取跟进记录/:查询/批量操作
class Followrecord(View):

    def get(self, request, id=None):
        if request.method == 'GET':
            # follow_objs=models.ConsultRecord.objects.all()#所有的客户跟进记录
            if id:
                follow_objs = models.ConsultRecord.objects.all().filter(customer_id=id)
            else:
                follow_objs = models.ConsultRecord.objects.all().filter(consultant=request.user)  # 只看到自己的客户跟进
                print('<<<<<<<<<<<<<<<<<<<<<', follow_objs)
                # follow_objs = models.ConsultRecord.objects.all().filter(consultant=request.user,customer__in=models.Customer.objects.filter(consultant=request.user))
            # 当前用户的客户对象id
            allcustomer_idlist = [i.pk for i in models.Customer.objects.filter(consultant=request.user)]
            # print('>>>>>>>>>>>>>>>>>>>>>>>>>>>', allcustomer_idlist)
            # 当前用户跟进记录中对应的所有客户对象id
            allfollowrecord_idlist = [i.get('customer') for i in
                                      models.ConsultRecord.objects.filter(consultant=request.user).values(
                                          'customer').distinct()]
            # print('>>>>>>>>>>>>>>>>>>>>>>>>>>>', allfollowrecord_idlist)

            idlist = [i for i in allfollowrecord_idlist if i not in allcustomer_idlist]
            # print('>>>>>>>>>>>>>>>>>>>>>', idlist)

            # field = request.GET.get('field', '')
            # val = request.GET.get('val', '')
            # if field and val:
            #     follow_objs = follow_objs.filter(**{field + '__contains': val})

            field = request.GET.get('field')
            val = request.GET.get(field)
            if field and val:
                if field in ['customer']:
                    val = models.Customer.objects.filter(pk=val).first()
                    follow_objs = follow_objs.filter(**{field: val})
                else:
                    follow_objs = follow_objs.filter(**{field + '__contains': val})

            from app01 import page
            per_page_counts = 8
            page_number = 5
            page_obj = page.PageNation(request.path, request.GET.get('page', 1), follow_objs.count(), request,
                                       per_page_counts,
                                       page_number)
            if follow_objs:
                customer_objs = follow_objs.order_by('-pk')[page_obj.start_num:page_obj.end_num]
                page = page_obj.page_html()
                return render(request, 'follow_record.html',
                              {'follow_objs': customer_objs, 'page': page, 'allfields': FollowrecordModelForm(request),
                               'batch_update_fields_list': ['status', ],
                               'search_fields_list': ['customer', 'note', 'status', 'date', ], 'idlist': idlist})
            else:
                page = '<h1>当前信息为空！</h1>'
                return render(request, 'follow_record.html', {'follow_objs': follow_objs, 'page': page, })

    # 处理批量操作
    def post(self, request):
        operation = request.POST.get('operation', '')
        id_list = request.POST.get('id_list', '')
        # id_list=json.loads(id_list)
        # print(operation)
        # print('++++++++', id_list, type(id_list))
        status = False
        if operation and id_list:
            if hasattr(sys.modules[__name__], operation) and callable(getattr(sys.modules[__name__], operation)):
                status = getattr(sys.modules[__name__], operation)(request, models.ConsultRecord)
        return JsonResponse({'status': status, 'operaiton': operation})
# 添加/编辑跟进记录(一个页面add_edit_followrecord.html)
class Add_Edit_Followrecord(View):

    def get(self, request, id=None):
        followrecord_obj = models.ConsultRecord.objects.filter(pk=id).first()
        if followrecord_obj:
            flag = 1
            followrecord_obj = FollowrecordModelForm(request, instance=followrecord_obj)
        else:
            flag = 0
            followrecord_obj = FollowrecordModelForm(request)

        return render(request, 'add_edit_followrecord.html', {'followrecord_obj': followrecord_obj, 'flag': flag})

    def post(self, request, id=None):
        followrecord_obj = models.ConsultRecord.objects.filter(pk=id).first()
        if followrecord_obj:
            flag = 1
        else:
            flag = 0
        followrecord_obj = FollowrecordModelForm(request, request.POST, instance=followrecord_obj)
        if followrecord_obj.is_valid():
            # print(followrecord_obj.cleaned_data)
            followrecord_obj.save()
            return redirect('followrecord')
        else:
            return render(request, 'add_edit_followrecord.html', {'followrecord_obj': followrecord_obj, 'flag': flag})
# 单个删除跟进记录
class DeleteFollowrecord(View):

    def get(self, request, id):
        # print(id)
        models.ConsultRecord.objects.filter(pk=id).delete()
        return redirect('followrecord')


# 学生信息
class Student(View):
    def get(self, request):
        student_objs = models.Student.objects.all()

        print('fydgusopdghdpfs[gopsaoospjak[jofghps')

        # 查询
        field = request.GET.get('field')
        val = request.GET.get(field)
        if field and val:
            if field in ['customer', ]:

                student_objs = models.Student.objects.filter(**{field: val})

            else:

                student_objs = models.Student.objects.filter(**{field + '__contains': val})

        searchfields = ['customer', 'company', 'position', 'date']
        batch_update_fields_list = ['date','position']

        per_page_counts = 8
        page_number = 5
        from app01 import page  # 导入分页
        page_obj = page.PageNation(request.path, request.GET.get('page', 1), student_objs.count(), request,
                                   per_page_counts, page_number)
        student_objs = student_objs[page_obj.start_num:page_obj.end_num]
        page_ = page_obj.page_html()

        if  student_objs:

            return render(request, 'student.html',
                          {"student_objs": student_objs, 'page': page_, 'allfields': StudentModelForm(),
                           'search_fields_list': searchfields, 'batch_update_fields_list': batch_update_fields_list})
        else:
            page = '<h1>当前信息为空！</h1>'
            return render(request, 'student.html', {'student_objs': student_objs, 'page': page, })

    def post(self, request):
        operation = request.POST.get('operation', '')
        id_list = request.POST.get('id_list', '')

        status = False
        if operation and id_list:
            if hasattr(sys.modules[__name__], operation) and callable(getattr(sys.modules[__name__], operation)):
                status = getattr(sys.modules[__name__], operation)(request, models.Student)
        return JsonResponse({'status': status, 'operaiton': operation})
class Add_Edit_Student(View):
    def get(self, request, id=None):
        obj = models.Student.objects.filter(pk=id).first()
        if id:
            flag = 0
        else:
            flag = 1
            print(obj)
        student_obj = StudentModelForm(instance=obj)
        return render(request, 'add_edit_student.html', {"student_obj": student_obj, 'flag': flag})

    def post(self, request, id=None):
        obj = models.Student.objects.filter(pk=id).first()
        # print('>>>>>>', obj)
        if id:
            flag = 0
        else:
            flag = 1
        student_obj = StudentModelForm(request.POST, instance=obj)
        if student_obj.is_valid():
            # print(student_obj.cleaned_data)
            student_obj.save()
            return redirect('student')
        else:
            return render(request, 'add_edit_student.html', {"student_obj": student_obj, 'flag': flag})
class DeleteStudent(View):
    def get(self, request, id):
        models.Student.objects.filter(pk=id).delete()
        return redirect('student')


# 教学信息
class Teach(View):
    def get(self, request):
        teach_objs = models.ClassStudyRecord.objects.all()

        # 查询
        # field = request.GET.get('field')
        # val = request.GET.get(field)
        # if field and val:
        #     if field in ['customer', ]:
        #
        #         teach_objs = models.ClassStudyRecord.objects.filter(**{field: val})
        #
        #     else:
        #
        #         teach_objs = models.ClassStudyRecord.objects.filter(**{field + '__contains': val})

        #查询字段
        searchfields = ['customer', 'company', 'position', 'date']


        per_page_counts = 8
        page_number = 5
        from app01 import page  # 导入分页
        page_obj = page.PageNation(request.path, request.GET.get('page', 1), teach_objs.count(), request,
                                   per_page_counts, page_number)
        teach_objs = teach_objs[page_obj.start_num:page_obj.end_num]
        page_ = page_obj.page_html()

        if  teach_objs:

            return render(request, 'teach.html',
                          {"teach_objs": teach_objs, 'page': page_, 'allfields': TeachModelForm(),
                           'search_fields_list': searchfields, })
        else:
            page = '<h1>当前信息为空！</h1>'
            return render(request, 'student.html', {'teach_objs': teach_objs, 'page': page, })

    def post(self, request):
        operation = request.POST.get('operation', '')
        id_list = request.POST.get('id_list', '')

        status = False
        if operation and id_list:
            if hasattr(sys.modules[__name__], operation) and callable(getattr(sys.modules[__name__], operation)):
                status = getattr(sys.modules[__name__], operation)(request, models.ClassStudyRecord)
            elif hasattr(self,operation) and callable(getattr(self,operation)):
                status=getattr(self,operation)(request)
        return JsonResponse({'status': status, 'operaiton': operation})

    def batch_create_studentstudyrecord(self,request):
        id_list=json.loads(request.POST.get('id_list', ''))
        id_list =[int(i) for i in id_list]
        teach_objs=models.ClassStudyRecord.objects.filter(pk__in=id_list)
        try:
            study_obj_list=[]
            for teach_obj in teach_objs:
                students_objs=models.Student.objects.filter(class_list=teach_obj.class_obj)
                for students_obj in students_objs:
                    study_obj=models.StudentStudyRecord(student=students_obj,classstudyrecord=teach_obj)
                    study_obj_list.append(study_obj)
                models.StudentStudyRecord.objects.bulk_create(study_obj_list)
        except Exception as e:
            print(e)
            return 0
        else:
            return 1

class Add_Edit_Teach(View):
    def get(self, request, id=None):
        obj = models.ClassStudyRecord.objects.filter(pk=id).first()
        if id:
            flag = 0
        else:
            flag = 1
            print(obj)
        teach_obj = TeachModelForm(instance=obj)
        return render(request, 'add_edit_teach.html', {"teach_obj": teach_obj, 'flag': flag})

    def post(self, request, id=None):
        obj = models.ClassStudyRecord.objects.filter(pk=id).first()
        if id:
            flag = 0
        else:
            flag = 1
        teach_obj = TeachModelForm(request.POST, instance=obj)
        if teach_obj.is_valid():

            teach_obj.save()
            return redirect('teach')
        else:
            return render(request, 'add_edit_teach.html', {"teach_obj": teach_obj, 'flag': flag})
class DeleteTeach(View):
    def get(self, request, id):
        models.ClassStudyRecord.objects.filter(pk=id).delete()
        return redirect('teach')




#学习情况详情（原生版）
# class Studydetail(View):
#     def get(self,request,ClassStudyRecord_id):
#         class_obj=models.ClassStudyRecord.objects.get(pk=ClassStudyRecord_id)
#         study_objs=models.StudentStudyRecord.objects.filter(classstudyrecord=class_obj)
#         title=f'{class_obj.date}{class_obj.class_obj}第{class_obj.day_num}节次'
#         record_choices=models.StudentStudyRecord.record_choices
#         score_choices=models.StudentStudyRecord.score_choices
#         # print(record_choices)
#
#         per_page_counts = 8
#         page_number = 5
#         from app01 import page  # 导入分页
#         page_obj = page.PageNation(request.path, request.GET.get('page', 1), study_objs.count(), request,
#                                    per_page_counts, page_number)
#         study_objs = study_objs[page_obj.start_num:page_obj.end_num]
#         page_ = page_obj.page_html()
#
#         if study_objs:
#             return render(request, 'studydeatil.html', {"study_objs": study_objs, 'record_choices':record_choices,'score_choices':score_choices, 'page': page_,'title':title})
#         else:
#             page = '<h1>当前信息为空！</h1>'
#             return render(request, 'studydeatil.html', {'study_objs': study_objs, 'page': page, 'title':title})
#
#     def post(self,request,ClassStudyRecord_id):
#         print(request.POST)
#         study_objs=request.POST
#         # for field,val in study_objs.items():
#         #     if field=='csrfmiddlewaretoken':
#         #         continue
#         #     field,study_obj_id=field.rsplit('_',1)
#         #     models.StudentStudyRecord.objects.filter(pk=ClassStudyRecord_id).update(**{field:val})
#
#         study_obj_dict={}
#         for field,val in study_objs.items():
#             if field=='csrfmiddlewaretoken':
#                 continue
#             field,study_obj_id=field.rsplit('_',1)
#             if study_obj_id in study_obj_dict:
#                 study_obj_dict[study_obj_id][field]=val
#             else:
#                 study_obj_dict[study_obj_id]={field:val}
#             for id,data in study_obj_dict.items():
#                 models.StudentStudyRecord.objects.filter(pk=study_obj_id).update(**data)
#
#         return self.get(request,ClassStudyRecord_id)
#     '''
#     requset.POST接收到的数据
#     < QueryDict: {
# 	'record_choices_9': ['late'],
# 	'score_9': ['-1'],
# 	'homework_note_9': ['暂无'],
# 	'record_choices_10': ['leave_early'],
# 	'score_10': ['70'],
# 	'homework_note_10': ['暂无'],
# 	'record_choices_11': ['checked'],
# 	'score_11': ['-1'],
# 	'homework_note_11': ['暂无'],
# 	'csrfmiddlewaretoken': ['etdn9wjMtmAmM7szNTbtHd41Gcv3wZL2gCMPh1IS0z1WKXWyqGLCHYyY2JJ2dAOo']
# } >
#     '''


#学习情况详情（formset版）
from django.forms.models import modelformset_factory
from django import forms
from app01 import models

class StudyDetailsModelForm(forms.ModelForm):
    class Meta:
        model=models.StudentStudyRecord
        # fields='__all__'
        fields=['student','record','score','homework_note']

class Studydetail(View):


    def get(self,request,ClassStudyRecord_id):
        formset_obj=modelformset_factory(model=models.StudentStudyRecord,form=StudyDetailsModelForm,extra=0)
        class_obj=models.ClassStudyRecord.objects.filter(pk=ClassStudyRecord_id).first()
        title = f'{class_obj.date}{class_obj.class_obj}第{class_obj.day_num}节次'
        study_objs=models.StudentStudyRecord.objects.filter(classstudyrecord=class_obj)
        formset_objs=formset_obj(queryset=study_objs)

        per_page_counts = 8
        page_number = 5
        from app01 import page  # 导入分页
        page_obj = page.PageNation(request.path, request.GET.get('page', 1), len(formset_objs) , request,
                                   per_page_counts, page_number)
        formset_objs = formset_objs[page_obj.start_num:page_obj.end_num]
        page_ = page_obj.page_html()
        if formset_objs:
            return render(request, 'studydeatil.html', { 'formset_objs':formset_objs, 'page': page_,'title':title})
        else:
            page = '<h1>当前信息为空！</h1>'
            return render(request, 'studydeatil.html', {'formset_objs': formset_objs, 'page': page, 'title':title})

        # return render(request,'studydeatil.html',{'formset_objs':formset_objs})#不分页直接返回


    def post(self,request,ClassStudyRecord_id):
        print(request.POST)
        formset_obj=modelformset_factory(model=models.StudentStudyRecord,form=StudyDetailsModelForm,extra=0)
        formset_objs=formset_obj(request.POST)
        if formset_objs.is_valid():
            formset_objs.save()
        else:
            print(formset_objs.errors)

        # return self.get(request,ClassStudyRecord_id)#避免一次重定向
        return redirect(reverse('studydetail',args=(ClassStudyRecord_id,)))#reverse反向解析传参数






# 学习信息
class Study(View):
    def get(self, request,id=None):
        if id:
            study_objs=models.StudentStudyRecord.objects.filter(classstudyrecord_id=id)
        else:
            study_objs = models.StudentStudyRecord.objects.all()

        # 查询
        field = request.GET.get('field')
        val = request.GET.get(field)
        # if field and val:
        #     if field in ['customer', ]:
        #
        #         study_objs = models.Student.objects.filter(**{field: val})
        #
        #     else:
        #
        #         study_objs = models.Student.objects.filter(**{field + '__contains': val})
        #
        searchfields = ['customer', 'company', 'position', 'date']
        batch_update_fields_list = ['date','position']

        per_page_counts = 8
        page_number = 5
        from app01 import page  # 导入分页
        page_obj = page.PageNation(request.path, request.GET.get('page', 1), study_objs.count(), request,
                                   per_page_counts, page_number)
        study_objs = study_objs[page_obj.start_num:page_obj.end_num]
        page_ = page_obj.page_html()

        if  study_objs:

            return render(request, 'study.html',
                          {"study_objs": study_objs, 'page': page_, 'allfields': StudyModelForm(),
                           'search_fields_list': searchfields, 'batch_update_fields_list': batch_update_fields_list})
        else:
            page = '<h1>当前信息为空！</h1>'
            return render(request, 'study.html', {'study_objs': study_objs, 'page': page, })

    def post(self, request):
        operation = request.POST.get('operation', '')
        id_list = request.POST.get('id_list', '')

        status = False
        if operation and id_list:
            if hasattr(sys.modules[__name__], operation) and callable(getattr(sys.modules[__name__], operation)):
                status = getattr(sys.modules[__name__], operation)(request, models.StudentStudyRecord)
        return JsonResponse({'status': status, 'operaiton': operation})
class Add_Edit_Study(View):
    def get(self, request, id=None):
        obj = models.StudentStudyRecord.objects.filter(pk=id).first()
        if id:
            flag = 0
        else:
            flag = 1
            print(obj)
        study_obj =StudyModelForm(instance=obj)
        return render(request, 'add_edit_study.html', {"study_obj": study_obj, 'flag': flag})

    def post(self, request, id=None):
        obj = models.StudentStudyRecord.objects.filter(pk=id).first()
        # print('>>>>>>', obj)
        if id:
            flag = 0
        else:
            flag = 1
        study_obj = StudyModelForm(request.POST, instance=obj)
        if study_obj.is_valid():
            # print(student_obj.cleaned_data)
            study_obj.save()
            return redirect('study')
        else:
            return render(request, 'add_edit_study.html', {"study_obj": study_obj, 'flag': flag})
class DeleteStudy(View):
    def get(self, request, id):
        models.StudentStudyRecord.objects.filter(pk=id).delete()
        return redirect('study')

