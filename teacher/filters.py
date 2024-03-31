import django_filters

from .models import Information, Attendance, Work


class TeacherInformationFilter(django_filters.FilterSet):
    real_name = django_filters.CharFilter(
        field_name="user__real_name", lookup_expr="icontains"
    )
    class_name = django_filters.CharFilter(
        field_name="classes__class_name", lookup_expr="icontains"
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
            "class_name",
            "user_id",
        )


class TeacherWorkFilter(django_filters.FilterSet):
    real_name = django_filters.CharFilter(
        field_name="user__real_name", lookup_expr="icontains"
    )
    work_date = django_filters.CharFilter(
        field_name="work_date", lookup_expr="icontains"
    )
    course_name = django_filters.CharFilter(
        field_name="course_name", lookup_expr="icontains"
    )
    course_class = django_filters.CharFilter(
        field_name="course_class", lookup_expr="icontains"
    )

    class Meta:
        model = Work
        fields = (
            "id",
            "real_name",
            "work_date",
            "course_name",
            "course_class",
            "user_id",
        )


class TeacherAttendanceFilter(django_filters.FilterSet):
    real_name = django_filters.CharFilter(
        field_name="user__real_name", lookup_expr="icontains"
    )
    date = django_filters.CharFilter(field_name="date", lookup_expr="icontains")
    check_in_time = django_filters.CharFilter(
        field_name="check_in_time", lookup_expr="icontains"
    )
    leave_start_time = django_filters.CharFilter(
        field_name="leave_start_time", lookup_expr="icontains"
    )
    attendance_status = django_filters.CharFilter(method="filter_attendance_status")

    def filter_attendance_status(self, queryset, name, value):
        attendance_status = value.split(",")
        return queryset.filter(attendance_status__in=attendance_status)

    class Meta:
        model = Attendance
        fields = (
            "id",
            "real_name",
            "date",
            "check_in_time",
            "attendance_status",
            "leave_start_time",
            "user_id",
        )
