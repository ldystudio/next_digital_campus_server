from iam.models import User


def get_user_id_from_request(request):
    """
    获取用户ID，优先级为：
    1. 从请求参数中获取user_id，如果存在，直接返回
    2. 从请求参数中获取real_name，尝试根据real_name获取user_id，如果存在，返回user_id
    3. 如果请求参数中没有user_id和real_name，则使用当前登录用户的user_id
    :param request: 请求对象
    :return: user_id
    """

    if user_id := request.data.get("user_id"):
        return user_id

    if real_name := request.data.get("real_name"):
        try:
            return User.objects.get(real_name=real_name).id
        except User.DoesNotExist:
            return request.user.id

    return request.user.id


def get_related_field_values_list(related, field="id"):
    return related.values_list(field, flat=True)
