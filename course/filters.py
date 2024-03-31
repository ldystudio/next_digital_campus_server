import django_filters

from .models import Setting


class CourseSettingFilter(django_filters.FilterSet):
    real_name = django_filters.CharFilter(
        field_name="teacher__user__real_name", lookup_expr="icontains"
    )
    class_name = django_filters.CharFilter(
        field_name="classes__class_name", lookup_expr="icontains"
    )
    course_name = django_filters.CharFilter(
        field_name="course_name", lookup_expr="icontains"
    )
    class_location = django_filters.CharFilter(
        field_name="class_location", lookup_expr="icontains"
    )
    course_type = django_filters.CharFilter(method="filter_course_type")

    def filter_course_type(self, queryset, name, value):
        course_type = value.split(",")
        return queryset.filter(course_type__in=course_type)

    class Meta:
        model = Setting
        fields = (
            "id",
            "real_name",
            "course_name",
            "class_name",
            "class_location",
            "course_type",
        )
