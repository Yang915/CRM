from django.contrib import admin

# Register your models here.

from app01 import models


# 定制admin显示的字段效果
class UserInfoAdim(admin.ModelAdmin):
    list_display = ['pk', 'username', 'telephone']  # 显示字段
    ordering = ['pk']  # 排序，默认逆序
class RoleAdim(admin.ModelAdmin):
    list_display = ['pk', 'name',]  # 显示字段
    list_editable = ['name']#是否直接可编辑
    ordering = ['pk']  # 排序，默认逆序
class PermissionAdim(admin.ModelAdmin):
    list_display = ['pk', 'name', 'url',]
    list_editable = ['name','url',]
    ordering = ['pk']
class MenuAdim(admin.ModelAdmin):
    list_display = ['pk', 'name',  ]
    list_editable = ['name',  ]
    ordering = ['pk']

admin.site.register(models.UserInfo, UserInfoAdim)
admin.site.register(models.Customer)
admin.site.register(models.Campuses)
admin.site.register(models.ClassList)
admin.site.register(models.Role,RoleAdim)
admin.site.register(models.Permission,PermissionAdim)
admin.site.register(models.Menu,MenuAdim)
admin.site.register(models.Student)
admin.site.register(models.ClassStudyRecord)
