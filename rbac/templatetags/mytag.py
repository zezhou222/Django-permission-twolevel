from django import template

register = template.Library()   # register和templatetags文件夹名是固定的名称


@register.filter
def match_permission(request, value):
    # value是模板页面传得死值
    # 从request中取出登陆出入得权限，和死值进行判断
    auth = request.session["auth"]
    for one_menu_dic in auth:
        if not one_menu_dic["is_menu"]:
            continue
        for two_menu_dic in one_menu_dic["two_menu"]:
            for dic in two_menu_dic["path"]:
                if dic["alias"] == value:
                    return True
    return False
