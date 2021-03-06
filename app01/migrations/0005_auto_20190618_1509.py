# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2019-06-18 07:09
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0004_auto_20190617_1723'),
    ]

    operations = [
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=12, verbose_name='一级菜单')),
                ('ico', models.CharField(default='fa fa-link', max_length=32, verbose_name='一级菜单图标')),
            ],
        ),
        migrations.RemoveField(
            model_name='permission',
            name='ico',
        ),
        migrations.AlterField(
            model_name='permission',
            name='menu',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app01.Menu'),
        ),
    ]
