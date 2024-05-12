import django_filters
from .models import User


class UserSimpleFilter(django_filters.FilterSet):
    real_name = django_filters.CharFilter(lookup_expr="icontains")

    class Meta:
        model = User
        fields = ("id", "user_role", "real_name")
