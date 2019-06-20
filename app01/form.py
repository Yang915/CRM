from django import forms#django的form组件
from django.core.validators import RegexValidator#form组件中的validators自带校验器
from django.core.exceptions import ValidationError#错误
import re
from app01 import models

#自定义校验函数
def name_valid(value):
    name_re = re.compile(r'^[\d]+')
    ret = name_re.match(value)
    if ret:
        raise ValidationError('用户名不能以数字开头！')

#注册form组件
class RegisterForm(forms.Form):
    name = forms.CharField(
        required=True,
        label='用户名：',
        min_length=6,
        max_length=32,
        help_text='只能有字母数字下划线组成，且不能以数字开头，长度6到32位！',
        # initial='admin123_',
        error_messages={
            'required': '用户名不能为空！',
            'min_length': '长度不能少于6位！',
            'max_length': '长度不能超过32位！',
        },
        validators=[RegexValidator(r'^[a-zA-Z0-9_]+$', '用户名只能包含字母数字下划线！'), name_valid],
    )
    password = forms.CharField(
        required=True,
        label='密码：',
        min_length=6,
        max_length=32,
        help_text='长度6到32位！',
        initial='',
        error_messages={
            'required': '密码不能为空！',
            'min_length': '长度不能少于6位！',
            'max_length': '长度不能超过32位！',
        },
        widget=forms.PasswordInput(render_value=True),
    )
    r_password = forms.CharField(
        required=True,
        label='确认密码：',
        min_length=6,
        max_length=32,
        help_text='长度6到32位！',
        initial='',
        error_messages={
            'required': '密码不能为空！',
            'min_length': '长度不能少于6位！',
            'max_length': '长度不能超过32位！',
        },
        widget=forms.PasswordInput(render_value=True),
    )
    email = forms.EmailField(
        required=True,
        label='邮箱',
        error_messages={
            'required': '邮箱不能为空！',
            'invalid':'邮箱格式不正确！'
        }
    )
    #全部字段添加样式
    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})
    #局部钩子
    def clean_name(self):
        pass
        return self.cleaned_data.get('name')

    def clean_password(self):
        pass
        return self.cleaned_data.get('password')

    def clean_r_password(self):
        pass
        return self.cleaned_data.get('r_password')

    def clean_email(self):
        pass
        return self.cleaned_data.get('email')
    #全局钩子
    def clean(self):
        password = self.cleaned_data.get('password')
        r_password = self.cleaned_data.get('r_password')
        if password != r_password:
            self.add_error('r_password', '两次密码不一致！')
            raise ValidationError('两次密码不一致！')
        else:
            return self.cleaned_data


#客户信息
class CustomerModelForm(forms.ModelForm):
    class Meta:
        model=models.Customer
        fields='__all__'
        widgets={

            'birthday':forms.DateInput(attrs={'type':'date'}),
            'next_date':forms.DateInput(attrs={'type':'date'}),
        }

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        for field in self.fields:
            self.fields[field].error_messages = {'required': '该字段不能为空！'}
            # print(field)
            if field!='course':#咨询课程字段是一个导入的第三方模块，添加样式会变形，直接不加
                self.fields[field].widget.attrs.update({'class': 'form-control'})

#跟进记录
class FollowrecordModelForm(forms.ModelForm):
    class Meta:
        model=models.ConsultRecord
        fields='__all__'
        exclude=['delete_status']

    def __init__(self, request,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['customer'].queryset=models.Customer.objects.filter(consultant=request.user)
        self.fields['consultant'].queryset = models.UserInfo.objects.filter(pk=request.user.pk)
        for field in self.fields:
            self.fields[field].error_messages = {'required': '该字段不能为空！'}
            # print(field)
            self.fields[field].widget.attrs.update({'class': 'form-control'})

#学生信息
class StudentModelForm(forms.ModelForm):
    class Meta:
        model=models.Student
        fields='__all__'
        widgets={
            'date':forms.DateInput(attrs={'type':'date'}),
        }

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class':'form-control'})
            self.fields[field].error_messages = {'required': '该字段不能为空！'}

#教学信息
class TeachModelForm(forms.ModelForm):
    class Meta:
        model=models.ClassStudyRecord
        fields='__all__'
        widgets={
            'has_homework':forms.CheckboxInput(attrs={'type':'radio'})
        }
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        for field in self.fields:
            if field=='has_homework':
                continue
            self.fields[field].widget.attrs.update({'class':'form-control'})
            self.fields[field].error_messages = {'required': '该字段不能为空！'}

#学习信息
class StudyModelForm(forms.ModelForm):
    class Meta:
        model=models.StudentStudyRecord
        fields='__all__'

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            for field in self.fields:
                if field == 'has_homework':
                    continue
                self.fields[field].widget.attrs.update({'class': 'form-control'})
                self.fields[field].error_messages = {'required': '该字段不能为空！'}

