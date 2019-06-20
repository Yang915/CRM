# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2019-06-19 08:50
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0007_auto_20190619_1542'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClassStudyRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day_num', models.IntegerField(help_text='此处填写第几节课或第几天课程...,必须为数字', verbose_name='节次')),
                ('date', models.DateField(auto_now_add=True, verbose_name='上课日期')),
                ('course_title', models.CharField(blank=True, max_length=64, null=True, verbose_name='本节课程标题')),
                ('course_memo', models.TextField(blank=True, null=True, verbose_name='本节课程内容概要')),
                ('has_homework', models.BooleanField(default=True, verbose_name='本节有作业')),
                ('homework_title', models.CharField(blank=True, max_length=64, null=True, verbose_name='本节作业标题')),
                ('homework_memo', models.TextField(blank=True, max_length=500, null=True, verbose_name='作业描述')),
                ('exam', models.TextField(blank=True, max_length=300, null=True, verbose_name='踩分点')),
                ('class_obj', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app01.ClassList', verbose_name='班级')),
                ('teacher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='讲师')),
            ],
        ),
        migrations.CreateModel(
            name='Enrollment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('why_us', models.TextField(blank=True, default=None, max_length=1024, null=True, verbose_name='为什么报名')),
                ('your_expectation', models.TextField(blank=True, max_length=1024, null=True, verbose_name='学完想达到的具体期望')),
                ('enrolled_date', models.DateTimeField(auto_now_add=True, verbose_name='报名日期')),
                ('memo', models.TextField(blank=True, null=True, verbose_name='备注')),
                ('delete_status', models.BooleanField(default=False, verbose_name='删除状态')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app01.Customer', verbose_name='客户名称')),
                ('enrolment_class', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app01.ClassList', verbose_name='所报班级')),
                ('school', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app01.Campuses')),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('emergency_contract', models.CharField(blank=True, max_length=32, null=True, verbose_name='紧急联系人')),
                ('company', models.CharField(blank=True, max_length=128, null=True, verbose_name='公司')),
                ('location', models.CharField(blank=True, max_length=64, null=True, verbose_name='所在区域')),
                ('position', models.CharField(blank=True, max_length=64, null=True, verbose_name='岗位')),
                ('salary', models.IntegerField(blank=True, null=True, verbose_name='薪资')),
                ('welfare', models.CharField(blank=True, max_length=256, null=True, verbose_name='福利')),
                ('date', models.DateField(blank=True, help_text='格式yyyy-mm-dd', null=True, verbose_name='入职时间')),
                ('memo', models.CharField(blank=True, max_length=256, null=True, verbose_name='备注')),
                ('class_list', models.ManyToManyField(blank=True, related_name='students', to='app01.ClassList', verbose_name='已报班级')),
                ('customer', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app01.Customer', verbose_name='客户信息')),
            ],
        ),
        migrations.CreateModel(
            name='StudentStudyRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('record', models.CharField(choices=[('checked', '已签到'), ('vacate', '请假'), ('late', '迟到'), ('noshow', '缺勤'), ('leave_early', '早退')], default='checked', max_length=64, verbose_name='上课纪录')),
                ('score', models.IntegerField(choices=[(100, 'A+'), (90, 'A'), (85, 'B+'), (80, 'B'), (70, 'B-'), (60, 'C+'), (50, 'C'), (40, 'C-'), (0, ' D'), (-1, 'N/A'), (-100, 'COPY'), (-1000, 'FAIL')], default=-1, verbose_name='本节成绩')),
                ('homework_note', models.CharField(blank=True, max_length=255, null=True, verbose_name='作业评语')),
                ('note', models.CharField(blank=True, max_length=255, null=True, verbose_name='备注')),
                ('homework', models.FileField(blank=True, default=None, null=True, upload_to='', verbose_name='作业文件')),
                ('stu_memo', models.TextField(blank=True, null=True, verbose_name='学员备注')),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name='提交作业日期')),
                ('classstudyrecord', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app01.ClassStudyRecord', verbose_name='第几天课程')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app01.Student', verbose_name='学员')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='studentstudyrecord',
            unique_together=set([('student', 'classstudyrecord')]),
        ),
        migrations.AlterUniqueTogether(
            name='enrollment',
            unique_together=set([('enrolment_class', 'customer')]),
        ),
    ]