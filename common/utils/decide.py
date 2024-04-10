def is_this_view(request, view_name):
    return view_name in request.resolver_match.func.__name__


def is_teacher(request):
    return request.user.is_authenticated and request.user.user_role == "teacher"


def is_student(request):
    return request.user.is_authenticated and request.user.user_role == "student"


def is_admin(request):
    return request.user.is_authenticated and request.user.user_role == "admin"
