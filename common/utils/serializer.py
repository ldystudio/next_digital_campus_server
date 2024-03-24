from iam.models import User
from rest_framework import serializers


def validate_user_id_or_real_name(request):
    user_id = request.data.get("user_id")
    real_name = request.data.get("real_name")

    # 如果user_id存在，直接返回user_id，不需要进一步验证
    if user_id:
        try:
            user = User.objects.get(id=user_id)
            return user.id
        except User.DoesNotExist:
            raise serializers.ValidationError("用户不存在")

    # 如果没有user_id但有real_name，尝试根据real_name获取user_id
    if real_name:
        try:
            user = User.objects.get(real_name=real_name)
            return user.id
        except User.DoesNotExist:
            # 如果real_name对应的用户不存在，使用request.user.id
            return request.user.id

    # 如果既没有user_id也没有real_name，使用request.user.id
    return request.user.id
