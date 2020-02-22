from django.db import models
from django.contrib.auth.models import AbstractUser


class UserInfo(AbstractUser):

    role = models.ManyToManyField(to="Role")

    class Meta:
        db_table = 'userInfo'


class Role(models.Model):

    role_name = models.CharField(max_length=20, blank=False)

    path = models.ManyToManyField(to='Path')

    class Meta:
        db_table = 'role'


# 动态菜单用
class Menu(models.Model):

    menu_name = models.CharField(max_length=30, blank=False)

    request_path = models.CharField(max_length=100)

    is_menu = models.BooleanField(default=1)

    # 二级菜单用
    pid = models.ForeignKey(to='self', on_delete=False, null=True)

    class Meta:
        db_table = 'menu'


class Path(models.Model):

    auth_path = models.CharField(max_length=100, blank=False)

    method = models.CharField(max_length=10, blank=False, default='GET')

    alias = models.CharField(max_length=20)

    path_name = models.CharField(max_length=30)

    menu = models.ForeignKey(to='Menu', on_delete=False)

    class Meta:
        db_table = 'path'
