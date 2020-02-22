import os
import django

project_name = 'test_qx'  # 不同项目需要修改

os.environ.setdefault("DJANGO_SETTINGS_MODULE", project_name + ".settings")
django.setup()

from rbac.models import *

menu_data = [
    {"id": 1, "menu_name": '非菜单-1', "is_menu": False},
    {"id": 2, "menu_name": '学生管理-1'},
    {"id": 3, "menu_name": '书籍管理-1'},
    {"id": 4, "menu_name": '学生管理', "request_path": "/student_page/", "pid_id": 2},
    {"id": 5, "menu_name": '获取学生信息', "request_path": "/student/", "pid_id": 2},
    {"id": 6, "menu_name": '书籍管理', "request_path": "/book_page/", "pid_id": 3},
    {"id": 7, "menu_name": '非菜单', "is_menu": False, "pid_id": 1},
]
path_data = [
    {"id": 1, "auth_path": '/student/$', "method": 'GET', "alias": 'get_students', "path_name": '获取学生', "menu_id": 4},
    {"id": 2, "auth_path": '/student/$', "method": 'POST', "alias": 'add_student', "path_name": '添加学生', "menu_id": 4},
    {"id": 3, "auth_path": '/student/$', "method": 'PUT', "alias": 'edit_student', "path_name": '编辑学生', "menu_id": 4},
    {"id": 4, "auth_path": '/student/$', "method": 'DELETE', "alias": 'delete_student', "path_name": '删除学生', "menu_id": 4},
    {"id": 5, "auth_path": '/book/$', "method": 'GET', "alias": 'get_books', "path_name": '获取书籍', "menu_id": 6},
    {"id": 6, "auth_path": '/book/$', "method": 'POST', "alias": 'add_book', "path_name": '添加书籍', "menu_id": 6},
    {"id": 7, "auth_path": '/book/$', "method": 'PUT', "alias": 'edit_book', "path_name": '编辑书籍', "menu_id": 6},
    {"id": 8, "auth_path": '/book/$', "method": 'DELETE', "alias": 'delete_book', "path_name": '删除书籍', "menu_id": 6},
    {"id": 9, "auth_path": '/index/$', "path_name": '访问首页', "menu_id": 7},
    {"id": 10, "auth_path": '/student_page/$', "path_name": '访问学生页面', "menu_id": 7},
    {"id": 11, "auth_path": '/book_page/$', "path_name": '访问书籍页面', "menu_id": 7},
    {"id": 12, "auth_path": '/logout/$', "path_name": '注销账户', "menu_id": 7},
    # 修改权限得权限
    {"id": 13, "auth_path": '/rbac/', "method": '*', "path_name": '修改权限', "menu_id": 7},
    # 测试一级菜单下面俩个二级菜单
    {"id": 14, "auth_path": '/student/$', "method": 'GET', "alias": 'get_students', "path_name": '获取学生', "menu_id": 5},
]
role_data = [
    {"id": 1, "role_name": "管理员", "path_id": (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14)},
    {"id": 2, "role_name": "普通用户", "path_id": (1, 2, 3, 5, 6, 7, 9, 10, 11, 12, 14)},
]
admin_user_data = [
    {"id": 1, "username": "admin", "password": "123456", "email": "test@qq.com"}
]
# 添加菜单数据
for dic in menu_data:
    # 添加菜单
    obj = Menu.objects.create(**dic)
# 添加权限路径数据
for dic in path_data:
    Path.objects.create(**dic)
# 添加角色数据
for dic in role_data:
    temp = dic
    path_ids = temp.pop("path_id")
    # 添加角色
    obj = Role.objects.create(**temp)
    # 添加角色和权限路径的关系
    Role.objects.get(id=obj.id).path.set(path_ids)
# 添加管理员用户
for dic in admin_user_data:
    obj = UserInfo.objects.create_superuser(**dic)
    obj.role.set((1,))  # 用户关联管理员角色

print("执行完毕.")
