import re

from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import HttpResponse, redirect

from test_qx.settings import white_list


class MyMiddleware(MiddlewareMixin):

    def process_request(self, request):
        # 当前请求路径
        now_path = request.path
        now_method = request.method

        # 白名单直接进入
        for rule in white_list:
            if re.search(rule, now_path):
                return None

        # 判断是否进行了登陆
        if not request.user.is_authenticated:
            return redirect('/login/')

        # 取出用户的路径
        auth = request.session.get('auth', None)
        # 权限路径认证
        if auth:
            # 进行循环判断
            for one_menu_dic in auth:
                for two_menu_dic in one_menu_dic["two_menu"]:
                    for dic in two_menu_dic["path"]:
                        # 如果当前请求的内容，符合权限里的，就进入
                        if re.search(dic["auth_path"], now_path) and (dic["method"] == now_method or dic["method"] == '*'):
                            return None

        # 没权，则直接返回
        return HttpResponse('not allow!')
