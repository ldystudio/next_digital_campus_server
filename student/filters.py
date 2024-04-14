import django_filters

from .models import Information, Enrollment, Attendance


class StudentInformationFilter(django_filters.FilterSet):
    real_name = django_filters.CharFilter(
        field_name="user__real_name", lookup_expr="icontains"
    )
    phone = django_filters.CharFilter(field_name="user__phone", lookup_expr="icontains")
    identification_number = django_filters.CharFilter(lookup_expr="icontains")
    gender = django_filters.CharFilter(method="filter_gender")

    def filter_gender(self, queryset, name, value):
        gender_statuses = value.split(",")
        return queryset.filter(gender__in=gender_statuses)

    class Meta:
        model = Information
        fields = (
            "id",
            "real_name",
            "phone",
            "identification_number",
            "gender",
            "user_id",
        )


class StudentEnrollmentFilter(django_filters.FilterSet):
    real_name = django_filters.CharFilter(
        field_name="student__user__real_name", lookup_expr="icontains"
    )
    class_name = django_filters.CharFilter(lookup_expr="icontains")
    address = django_filters.CharFilter(lookup_expr="icontains")
    enrollment_status = django_filters.CharFilter(method="filter_enrollment_status")

    def filter_enrollment_status(self, queryset, name, value):
        enrollment_statuses = value.split(",")
        return queryset.filter(enrollment_status__in=enrollment_statuses)

    class Meta:
        model = Enrollment
        fields = (
            "id",
            "real_name",
            "class_name",
            "address",
            "enrollment_status",
        )


class StudentAttendanceFilter(django_filters.FilterSet):
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
