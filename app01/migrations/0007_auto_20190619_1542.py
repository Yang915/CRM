# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2019-06-19 07:42
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0006_permission_pid'),
    ]

    operations = [
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=12, verbose_name='部门名称')),
                ('count', models.IntegerField(verbose_name='部门人数')),
            ],
        ),
        migrations.AddField(
            model_name='userinfo',
            name='dep',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app01.Department'),
        ),
    ]
