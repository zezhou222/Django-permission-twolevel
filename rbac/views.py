import json

from django.contrib import auth
from django.http import HttpResponse
from django.shortcuts import render, redirect

from rbac.models import (
    UserInfo,
    Role,
    Path,
    Menu
)


def Register(request):
    if request.method == 'GET':
        return render(request, 'register.html')
    else:
        dic = request.POST.dict()
        # 先查看该用户名是否已经存在
        ret = UserInfo.objects.filter(username=dic.get('username')).first()
        if not ret:
            # 创建用户数据，返回的用户对象
            obj = UserInfo.objects.create_user(**dic)
            # 关联初始权限
            role_id = Role.objects.get(role_name='普通用户').id
            UserInfo.objects.get(id=obj.id).role.set((role_id,))
            return redirect('/login/')
        else:
            return HttpResponse(content='the username exists.', status=422)


def Login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    else:
        dic = request.POST.dict()
        # 认证成功，返回对象
        ret = auth.authenticate(request, **dic)
        if ret:
            # 认证成功，添加session,中间件判断是否登陆
            auth.login(request, ret)
            # 添加权限路径准备工作
            """
            [
                {
                    "one_menu": "书籍管理-1", 
                    "is_menu": 1,  # 为真表示是动态菜单要渲染得内容
                    "two_menu": [
                        {
                            "menu": "书籍管理",
                            "request_path": "/book_page/",
                            "path": [
                                {"method": "get", "auth_path": "/book/", "alias": "get_books"}, 
                                {"method": "post", "auth_path": "/book/", "alias": "add_book"}
                            ]
                        },
                        {
                            "menu": "获取数据",
                            "request_path": "/book/",
                            "path": [
                                {"method": "get", "auth_path": "/book/$", "alias": "get_books"}, 
                            ]
                        },
                    ]
                },
                {
                    "one_menu": "学生管理-1", 
                    "is_menu": 1,
                    "two_menu": [
                        {
                            "menu": "学生管理",
                            "request_path": "/student_page/",
                            "path": [
                                {"method": "get", "auth_path": "/student/", "alias": "get_students"}, 
                                {"method": "post", "auth_path": "/student/", "alias": "add_student"}
                            ]
                        },
                    ]
                },
            ]
            """
            all_path_data = []
            # 查询用户都有什么角色
            values = UserInfo.objects.filter(id=request.user.id).values(
                'role__path__menu__pid__menu_name',
                'role__path__menu__menu_name',
                'role__path__menu__request_path',
                'role__path__menu__is_menu',
                'role__path__method',
                'role__path__auth_path',
                'role__path__alias',
            )
            # print(values)
            for dic in values:
                one_menu = dic['role__path__menu__pid__menu_name']
                menu = dic['role__path__menu__menu_name']
                request_path = dic['role__path__menu__request_path']
                is_menu = dic['role__path__menu__is_menu']
                method = dic['role__path__method']
                auth_path = dic['role__path__auth_path']
                alias = dic['role__path__alias']
                for dic2 in all_path_data:
                    if dic2["one_menu"] == one_menu:
                        temp = {
                            "menu": menu,
                            "request_path": request_path,
                            "path": [{"method": method, "auth_path": auth_path, "alias": alias}]
                        }
                        for dic3 in dic2["two_menu"]:
                            if dic3["menu"] == menu:
                                temp = {"method": method, "auth_path": auth_path, "alias": alias}
                                dic3["path"].append(temp)
                                # 正常添加完跳出，否则重复执行for-else里得内容
                                break
                        else:
                            # 二级菜单没有时候执行
                            dic2["two_menu"].append(temp)
                        # 正常添加完跳出，否则重复执行for-else里得内容
                        break
                else:
                    # 一级菜单没时候才会执行
                    temp = {
                        "one_menu": one_menu,
                        "is_menu": is_menu,
                        "two_menu": [
                            {
                                "menu": menu,
                                "request_path": request_path,
                                "path": [{"method": method, "auth_path": auth_path, "alias": alias}]
                            }
                        ]
                    }
                    all_path_data.append(temp)
            # print(all_path_data)
            # 添加权限路径到session
            request.session["auth"] = all_path_data
            # 重定向到首页
            return redirect('/index/')
        else:
            return HttpResponse(content='username or password error.', status=401)


def Logout(request):
    auth.logout(request)
    return HttpResponse(content='logout success')


def Permission(request):
    return render(request, 'permission.html')


def MyUser(request):
    if request.method == 'GET':
        id = request.GET.get('id', None)
        if not id:
            page = int(request.GET.get('page'))
            limit = int(request.GET.get('limit'))
            if page-1 == 0:
                objs = UserInfo.objects.all()[0:limit]
            else:
                objs = UserInfo.objects.all()[(page-1)*limit:page*limit]
            values = list(objs.values('id', 'username'))
        else:
            id = int(id)
            result = UserInfo.objects.filter(id=id).values('id', 'username', 'role__id', 'role__path__id')
            values = {"id": '', "username": '', "role_id": [], "path_id": []}
            for dic in result:
                if values['id'] == '':
                    values['id'] = dic['id']
                    values['username'] = dic['username']
                if dic['role__id'] not in values["role_id"]:
                    values["role_id"].append(dic['role__id'])
                if dic['role__path__id'] not in values["path_id"]:
                    values["path_id"].append(dic['role__path__id'])
            # print(values)
        return HttpResponse(json.dumps(values), content_type='application/json')

    elif request.method == 'POST':
        pass
    elif request.method == 'PUT':
        pass
    elif request.method == 'DELETE':
        pass


def MyRole(request):
    if request.method == 'GET':
        id = request.GET.get('id', None)
        if not id:
            objs = Role.objects.all()
            values = list(objs.values('id', 'role_name'))
        else:
            id = int(id)
            result = Role.objects.filter(id=id).values('id', 'role_name', 'path__id')
            values = {"id": '', "role_name": '', "path_id": []}
            for dic in result:
                if values['id'] == '':
                    values['id'] = dic['id']
                    values['role_name'] = dic['role_name']
                if dic['path__id'] not in values["path_id"]:
                    values["path_id"].append(dic['path__id'])
        return HttpResponse(json.dumps(values), content_type='application/json')

    elif request.method == 'POST':
        pass
    elif request.method == 'PUT':
        opt = request.GET.get('opt', None)
        # 更新用户选择得角色
        if opt == 'save_role':
            content = json.loads(request.body)
            user_id = content.get('user_id')
            role_ids = content.get('role_ids')
            UserInfo.objects.get(id=user_id).role.set(role_ids)
        else:
            # 更新角色信息
            pass
        return HttpResponse(json.dumps(0), content_type='application/json')
    elif request.method == 'DELETE':
        pass


def MyMenu(request):
    if request.method == 'GET':
        values = Path.objects.all().values(
            'id',  # 权限路径id
            'path_name',  # 权限路径名称
            'menu_id',  # 二级菜单id
            'menu__menu_name',   # 二级菜单名
            'menu__pid__menu_name',  # 一级菜单名
            'menu__pid__is_menu',  # 一级菜单是否是前端动态菜单标识
            'menu__pid__id',  # 一级菜单id
        )
        data = []
        for dic in values:
            # 权限配置页面是否配置非菜单权限，目前不能开启，要改保存权限得代码才可
            # if not dic['menu__pid__is_menu']:
            #     continue

            # 取数据
            one_menu_id = dic['menu__pid__id']
            one_menu = dic['menu__pid__menu_name']
            two_menu_id = dic['menu_id']
            two_menu = dic['menu__menu_name']
            path_id = dic['id']
            path_name = dic['path_name']
            # 赋值
            for one_menu_dic in data:
                if dic['menu__pid__menu_name'] == one_menu_dic["one_menu"]:
                    for two_menu_dic in one_menu_dic["two_menu"]:
                        if two_menu_dic["two_menu"] == two_menu:
                            temp = {"path_id": path_id, "path_name": path_name}
                            two_menu_dic["path"].append(temp)
                            break
                    else:
                        temp = {
                                'two_menu_id': two_menu_id,
                                'two_menu': two_menu,
                                'path': [
                                    {"path_id": path_id,
                                     "path_name": path_name
                                     }
                                ]
                        }
                        one_menu_dic["two_menu"].append(temp)
                    break
            else:
                temp = {
                    "one_menu_id": one_menu_id,
                    "one_menu": one_menu,
                    "two_menu": [{
                            'two_menu_id': two_menu_id,
                            'two_menu': two_menu,
                            'path': [
                                {"path_id": path_id,
                                 "path_name": path_name
                                 }
                            ]
                    }]
                }
                data.append(temp)
        # print(data)
        return HttpResponse(json.dumps(data), content_type='application/json')

    elif request.method == 'POST':
        pass
    elif request.method == 'PUT':
        opt = request.GET.get('opt', None)
        # 更新用户选择得角色
        if opt == 'save_permission':
            content = json.loads(request.body)
            role_id = content.get('role_id')
            permission_ids = content.get('permission_ids')
            Role.objects.get(id=role_id).path.set(permission_ids)
        else:
            # 更新权限信息
            pass
        return HttpResponse(json.dumps(0), content_type='application/json')
    elif request.method == 'DELETE':
        pass
