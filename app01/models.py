# Create your models here.

from django.contrib.auth.models import AbstractUser

from django.db import models
from django.contrib import auth
from django.core.exceptions import PermissionDenied
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager, User
from django.utils.translation import ugettext_lazy as _
from multiselectfield import MultiSelectField
# 安装:pip install django-multiselectfield,针对choices多选用的


from django.utils.safestring import mark_safe

# 课程选项
course_choices = (('LinuxL', 'Linux中高级'),
                  ('PythonFullStack', 'Python高级全栈开发'),)

# 学习方式选项
class_type_choices = (('fulltime', '脱产班',),
                      ('online', '网络班'),
                      ('weekend', '周末班',),)

# 客户途径
source_type = (('qq', "qq群"),
               ('referral', "内部转介绍"),
               ('website', "官方网站"),
               ('baidu_ads', "百度推广"),
               ('office_direct', "直接上门"),
               ('WoM', "口碑"),
               ('public_class', "公开课"),
               ('website_luffy', "路飞官网"),
               ('others', "其它"),)

enroll_status_choices = (('signed', "已报名"),
                         ('unregistered', "未报名"),
                         ('studying', '学习中'),
                         ('paid_in_full', "学费已交齐"))

# 跟进记录状态
seek_status_choices = (('A', '近期无报名计划'), ('B', '1个月内报名'), ('C', '2周内报名'), ('D', '1周内报名'),
                       ('E', '定金'), ('F', '到班'), ('G', '全款'), ('H', '无效'),)

pay_type_choices = (('deposit', "订金/报名费"),
                    ('tuition', "学费"),
                    ('transfer', "转班"),
                    ('dropout', "退学"),
                    ('refund', "退款"),)

# 考勤选项
attendance_choices = (('checked', "已签到"),
                      ('vacate', "请假"),
                      ('late', "迟到"),
                      ('absence', "缺勤"),
                      ('leave_early', "早退"),)

# 课程选项
score_choices = ((100, 'A+'),
                 (90, 'A'),
                 (85, 'B+'),
                 (80, 'B'),
                 (70, 'B-'),
                 (60, 'C+'),
                 (50, 'C'),
                 (40, 'C-'),
                 (0, ' D'),
                 (-1, 'N/A'),
                 (-100, 'COPY'),
                 (-1000, 'FAIL'),)


# 用户表（自定义使用auth认证）
class UserInfo(AbstractUser):
    # 销售,班主任,讲师,三哥
    telephone = models.CharField(max_length=32, null=True, blank=True, verbose_name='联系电话')
    role = models.ManyToManyField(to='Role', verbose_name='角色', default=None, null=True, blank=True)
    dep = models.ForeignKey(to='Department', null=True, blank=True)


# 角色表
class Role(models.Model):
    name = models.CharField(max_length=32, verbose_name='角色', unique=True)
    permission = models.ManyToManyField(to='Permission', verbose_name='权限', null=True, blank=True)

    def __str__(self):
        return self.name


# 权限表
class Permission(models.Model):
    name = models.CharField(verbose_name='操作权限', max_length=32)
    url = models.CharField(max_length=48, verbose_name='url路径')
    # menu=models.BooleanField(default=False,verbose_name='是否为菜单')
    # ico=models.CharField(max_length=32,verbose_name='图标',default='fa fa-link')
    menu = models.ForeignKey(to='Menu', null=True, blank=True)  # 设置权限显示菜单归属于一级菜单的id,不为空的即为要显示的二级菜单
    pid = models.ForeignKey(to='self', null=True, blank=True)  # 不同权限归属的显示菜单

    def __str__(self):
        return self.name


# 一级菜单表
ico_list = ['fa fa-mortar-board', 'fa fa-link', 'fa fa-map-o', 'fa fa-reorder', 'fa fa-sliders', 'fa fa-bandcamp',
            'fa fa-ravelry', 'fa fa-user-circle', 'fa fa-window-restore', 'fa fa-window-maximize',
            'fa fa-window-restore',
            'fa fa-book', 'fa fa-bookmark-o', 'fa fa-cubes', 'fa fa-folder-open-o', 'fa fa-laptop', 'fa fa-server',
            'fa fa fa-address-card','fa fa-sitemap','fa fa-sticky-note-o','fa fa-tasks','fa fa-bar-chart-o','fa fa-columns',
            'fa fa-list-ul','fa fa-indent']


class Menu(models.Model):
    name = models.CharField(max_length=12, verbose_name='一级菜单')
    ico = models.CharField(max_length=32, verbose_name='一级菜单图标', default='fa fa-link')

    def __str__(self):
        return self.name


# 部门表
class Department(models.Model):
    '''
    部门表
    '''
    name = models.CharField(max_length=12, verbose_name='部门名称')
    count = models.IntegerField(verbose_name='部门人数')

    def __str__(self):
        return self.name


# 客户表
class Customer(models.Model):
    """
    客户表（最开始的时候大家都是客户，销售就不停的撩你，你还没交钱就是个客户）
    """
    qq = models.CharField(verbose_name='QQ', max_length=64, unique=True, help_text='QQ号必须唯一')
    qq_name = models.CharField('QQ昵称', max_length=64, blank=True, null=True)
    name = models.CharField('姓名', max_length=32, help_text='学员报名后，请改为真实姓名')
    sex_type = (('male', '男'), ('female', '女'))
    sex = models.CharField("性别", choices=sex_type, max_length=16, default='male', blank=True,
                           null=True)  # 存的是male或者female，字符串
    birthday = models.DateField('出生日期', default=None, help_text="格式yyyy-mm-dd", blank=True, null=True)

    phone = models.CharField('手机号', blank=True, null=True, max_length=32)
    # phone = models.CharField('手机号', blank=True, null=True)
    source = models.CharField('客户来源', max_length=64, choices=source_type, default='qq')

    introduce_from = models.ForeignKey('self', verbose_name="转介绍自学员", blank=True,
                                       null=True)  # self指的就是自己这个表，和下面写法是一样的效果

    # introduce_from = models.ForeignKey('Customer', verbose_name="转介绍自学员", blank=True, null=True,on_delete=models.CASCADE)
    course = MultiSelectField("咨询课程", choices=course_choices)  # 多选，并且存成一个列表的格式
    # course = models.CharField("咨询课程", choices=course_choices) #如果你不想用上面的多选功能，可以使用Charfield来存
    class_type = models.CharField("班级类型", max_length=64, choices=class_type_choices, default='fulltime')
    customer_note = models.TextField("客户备注", blank=True, null=True, )
    status = models.CharField("状态", choices=enroll_status_choices, max_length=64, default="unregistered",
                              help_text="选择客户此时的状态")  # help_text这种参数基本都是针对admin应用里面用的

    date = models.DateTimeField("咨询日期", auto_now_add=True)

    last_consult_date = models.DateField("最后跟进日期", auto_now_add=True)  # 考核销售的跟进情况，如果多天没有跟进，会影响销售的绩效等
    next_date = models.DateField("预计再次跟进时间", blank=True, null=True)  # 销售自己大概记录一下自己下一次会什么时候跟进，也没啥用

    # 用户表中存放的是自己公司的所有员工。
    consultant = models.ForeignKey('UserInfo', verbose_name="销售", blank=True, null=True)

    # 一个客户可以报多个班，报个脱产班，再报个周末班等，所以是多对多。
    class_list = models.ManyToManyField('ClassList', verbose_name="已报班级", null=True,
                                        blank=True)  # blank在ModelForm校验是或否允许为空，null是数据库判断

    def __str__(self):
        return self.name + ":" + self.qq  # 主要__str__最好是个字符串昂，不然你会遇到很多的坑，还有我们返回的这两个字段填写数据的时候必须写上数据，必然相加会报错，null类型和str类型不能相加等错误信息。

    def get_classlist(self):  # 当我们通过self.get_classlist的时候，就拿到了所有的班级信息，前端显示的时候用

        l = []
        for cls in self.class_list.all():
            l.append(str(cls))
        # return mark_safe(",".join(l)) #纯文本，不用mark_safe也可以昂
        return ",".join(l)  # 纯文本，不用mark_safe也可以昂


# 校区表
class Campuses(models.Model):
    """
    校区表
    """
    name = models.CharField(verbose_name='校区', max_length=64)
    address = models.CharField(verbose_name='详细地址', max_length=512, blank=True, null=True)

    def __str__(self):
        return self.name


# 班级表
class ClassList(models.Model):
    """
    班级表
    """
    course = models.CharField("课程名称", max_length=64, choices=course_choices)
    semester = models.IntegerField("学期")  # python20期等
    campuses = models.ForeignKey('Campuses', verbose_name="校区", on_delete=models.CASCADE)
    price = models.IntegerField("学费", default=10000)
    memo = models.CharField('说明', blank=True, null=True, max_length=100)
    start_date = models.DateField("开班日期")
    graduate_date = models.DateField("结业日期", blank=True, null=True)  # 不一定什么时候结业，哈哈，所以可为空

    # contract = models.ForeignKey('ContractTemplate', verbose_name="选择合同模版", blank=True, null=True,on_delete=models.CASCADE)
    teachers = models.ManyToManyField('UserInfo',
                                      verbose_name="老师")  # 对了，还有一点，如果你用的django2版本的，那么外键字段都需要自行写上on_delete=models.CASCADE

    class_type = models.CharField(choices=class_type_choices, max_length=64, verbose_name='班额及类型', blank=True,
                                  null=True)

    class Meta:
        unique_together = ("course", "semester", 'campuses')

    def __str__(self):
        return "{}{}({})".format(self.get_course_display(), self.semester, self.campuses)


# 跟进记录表
class ConsultRecord(models.Model):
    """
    跟进记录表
    """
    customer = models.ForeignKey('Customer', verbose_name="所咨询客户")

    note = models.TextField(verbose_name="跟进内容...")

    status = models.CharField("跟进状态", max_length=8, choices=seek_status_choices, help_text="选择客户此时的状态")

    consultant = models.ForeignKey("UserInfo", verbose_name="跟进人", related_name='records')

    date = models.DateTimeField("跟进日期", auto_now_add=True)

    delete_status = models.BooleanField(verbose_name='删除状态', default=False)


# 报名表
class Enrollment(models.Model):
    """
    报名表
    """

    customer = models.ForeignKey('Customer', verbose_name='客户名称')

    why_us = models.TextField("为什么报名", max_length=1024, default=None, blank=True, null=True)

    your_expectation = models.TextField("学完想达到的具体期望", max_length=1024, blank=True, null=True)

    enrolled_date = models.DateTimeField(auto_now_add=True, verbose_name="报名日期")

    memo = models.TextField('备注', blank=True, null=True)

    delete_status = models.BooleanField(verbose_name='删除状态', default=False)

    school = models.ForeignKey('Campuses')  # 校区表

    enrolment_class = models.ForeignKey("ClassList", verbose_name="所报班级")

    class Meta:
        unique_together = ('enrolment_class', 'customer')


# 学生表
class Student(models.Model):
    """
    学生表（已报名）
    """
    customer = models.OneToOneField(verbose_name='客户信息', to='Customer', on_delete=models.CASCADE, null=True, blank=True)
    class_list = models.ManyToManyField(verbose_name="已报班级", to='ClassList', blank=True, related_name="students")

    emergency_contract = models.CharField(max_length=32, blank=True, null=True, verbose_name='紧急联系人')
    company = models.CharField(verbose_name='公司', max_length=128, blank=True, null=True)
    location = models.CharField(max_length=64, verbose_name='所在区域', blank=True, null=True)
    position = models.CharField(verbose_name='岗位', max_length=64, blank=True, null=True)
    salary = models.IntegerField(verbose_name='薪资', blank=True, null=True)
    welfare = models.CharField(verbose_name='福利', max_length=256, blank=True, null=True)
    date = models.DateField(verbose_name='入职时间', help_text='格式yyyy-mm-dd', blank=True, null=True)
    memo = models.CharField(verbose_name='备注', max_length=256, blank=True, null=True)

    def __str__(self):
        return self.customer.name

    def class_dispaly(self):
        l = []
        for i in self.class_list.all():
            l.append(str(i))
        return '.'.join(l)


# 班级教学记录表
class ClassStudyRecord(models.Model):
    """
    上课记录表 （班级记录）
    """
    class_obj = models.ForeignKey(verbose_name="班级", to="ClassList", on_delete=models.CASCADE)
    day_num = models.IntegerField(verbose_name="节次", help_text=u"此处填写第几节课或第几天课程...,必须为数字")

    teacher = models.ForeignKey(verbose_name="讲师", to='UserInfo', on_delete=models.CASCADE)
    date = models.DateField(verbose_name="上课日期", auto_now_add=True)
    course_title = models.CharField(verbose_name='本节课程标题', max_length=64, blank=True, null=True)
    course_memo = models.TextField(verbose_name='本节课程内容概要', blank=True, null=True)
    has_homework = models.BooleanField(default=True, verbose_name="本节有作业", )
    homework_title = models.CharField(verbose_name='本节作业标题', max_length=64, blank=True, null=True)
    homework_memo = models.TextField(verbose_name='作业描述', max_length=500, blank=True, null=True)
    exam = models.TextField(verbose_name='踩分点', max_length=300, blank=True, null=True)

    def __str__(self):
        return "{0} day{1}".format(self.class_obj, self.day_num)


# 学生学习记录表
class StudentStudyRecord(models.Model):
    '''
    学生学习记录
    '''
    student = models.ForeignKey(verbose_name="学员", to='Student', on_delete=models.CASCADE)
    classstudyrecord = models.ForeignKey(verbose_name="第几天课程", to="ClassStudyRecord", on_delete=models.CASCADE)
    record_choices = (('checked', "已签到"),
                      ('vacate', "请假"),
                      ('late', "迟到"),
                      ('noshow', "缺勤"),
                      ('leave_early', "早退"),
                      )
    record = models.CharField("上课纪录", choices=record_choices, default="checked", max_length=64)
    score_choices = ((100, 'A+'),
                     (90, 'A'),
                     (85, 'B+'),
                     (80, 'B'),
                     (70, 'B-'),
                     (60, 'C+'),
                     (50, 'C'),
                     (40, 'C-'),
                     (0, ' D'),
                     (-1, 'N/A'),
                     (-100, 'COPY'),
                     (-1000, 'FAIL'),
                     )
    score = models.IntegerField("本节成绩", choices=score_choices, default=-1)
    homework_note = models.CharField(verbose_name='作业评语', max_length=255, blank=True, null=True)
    note = models.CharField(verbose_name="备注", max_length=255, blank=True, null=True)

    homework = models.FileField(verbose_name='作业文件', blank=True, null=True, default=None)
    stu_memo = models.TextField(verbose_name='学员备注', blank=True, null=True)
    date = models.DateTimeField(verbose_name='提交作业日期', auto_now_add=True)

    def __str__(self):
        return "{0}-{1}".format(self.classstudyrecord, self.student)

    class Meta:
        unique_together = ["student", "classstudyrecord"]
