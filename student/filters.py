import django_filters

from .models import Information


class StudentInformationFilter(django_filters.FilterSet):
    real_name = django_filters.CharFilter(
        field_name="user__real_name", lookup_expr="icontains"
    )
    phone = django_filters.CharFilter(field_name="user__phone", lookup_expr="icontains")
    identification_number = django_filters.CharFilter(
        field_name="identification_number", lookup_expr="icontains"
    )
    enrollment_status = django_filters.CharFilter(method="filter_enrollment_status")

    def filter_enrollment_status(self, queryset, name, value):
        enrollment_statuses = value.split(",")
        return queryset.filter(enrollment_status__in=enrollment_statuses)

    class Meta:
        model = Information
        fields = (
            "id",
            "real_name",
            "phone",
            "identification_number",
            "enrollment_status",
            "user_id",
        )
