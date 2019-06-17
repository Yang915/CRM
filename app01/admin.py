from django.contrib import admin

# Register your models here.

from app01 import models


# 定制admin显示的字段效果
class UserInfoAdim(admin.ModelAdmin):
    list_display = ['pk', 'username', 'telephone']  # 显示字段

    ordering = ['pk']  # 排序，默认逆序


admin.site.register(models.UserInfo, UserInfoAdim)
admin.site.register(models.Customer)
admin.site.register(models.Campuses)
admin.site.register(models.ClassList)
