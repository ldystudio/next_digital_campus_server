import django_filters

from .models import Information


class TeacherInformationFilter(django_filters.FilterSet):
    real_name = django_filters.CharFilter(
        field_name="user__real_name", lookup_expr="icontains"
    )
    phone = django_filters.CharFilter(field_name="user__phone", lookup_expr="icontains")
    identification_number = django_filters.CharFilter(
        field_name="identification_number", lookup_expr="icontains"
    )
    service_status = django_filters.CharFilter(method="filter_service_status")

    def filter_service_status(self, queryset, name, value):
        service_status = value.split(",")
        return queryset.filter(service_status__in=service_status)

    class Meta:
        model = Information
        fields = (
            "id",
            "real_name",
            "phone",
            "identification_number",
            "service_status",
            "user_id",
        )
