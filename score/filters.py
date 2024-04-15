import django_filters

from .models import Information


class ScoreInformationFilter(django_filters.FilterSet):
    student = django_filters.CharFilter(
        field_name="student__user__real_name", lookup_expr="icontains"
    )
    course = django_filters.CharFilter(
        field_name="course__course_name", lookup_expr="icontains"
    )
    exam_date = django_filters.CharFilter(lookup_expr="icontains")
    entered_by = django_filters.CharFilter(
        field_name="entered_by__real_name", lookup_expr="icontains"
    )

    exam_type = django_filters.CharFilter(method="filter_exam_type")

    def filter_exam_type(self, queryset, name, value):
        exam_type = value.split(",")
        return queryset.filter(exam_type__in=exam_type)

    class Meta:
        model = Information
        fields = ("id", "student", "course", "exam_date", "entered_by", "exam_type")
