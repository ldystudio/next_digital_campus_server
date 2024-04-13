def is_request_mapped_to_view(request, view_name: str | list):
    """
    检查当前请求是否映射到指定的视图名称。

    参数:
        request: HttpRequest 对象，代表当前HTTP请求。
        view_name: str | list，要检查的视图名称。

    返回:
        bool，如果请求映射到指定视图，则为True；否则为False。
    """
    if isinstance(view_name, str):
        return view_name == request.resolver_match.func.__name__

    for name in view_name:
        if name == request.resolver_match.func.__name__:
            return True
    return False


def is_teacher(request):
    return request.user.is_authenticated and request.user.user_role == "teacher"


def is_student(request):
    return request.user.is_authenticated and request.user.user_role == "student"


def is_admin(request):
    return request.user.is_authenticated and request.user.user_role == "admin"
