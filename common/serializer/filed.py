from rest_framework.serializers import RelatedField
from django.utils.translation import gettext_lazy as _


class MultipleSlugRelatedField(RelatedField):
    """
    A custom field to represent a model with multiple slug fields.

    This field takes a list of slug fields and returns the model instance
    with the given slug values. If the model instance does not exist,
    it raises a validation error.

    Example:

    class CourseSerializer(serializers.ModelSerializer):
        course = MultipleSlugRelatedField(read_only=True, slug_fields=["course_name"], pk="course_id", pk_field=serializers.CharField())
        class Meta:
            model = Course
            fields = ["course", ]

    Note:
        The `pk` and `pk_field` arguments are optional. If `pk_field` is not provided,
        the `pk` field will not be included in the serialized data.

    Attributes:
        slug_fields (list): A list of slug fields to search for the model instance.
        pk (str): The name of the primary key field.
        pk_field (Field): The field instance for the primary key.
    """

    default_error_messages = {
        "does_not_exist": _("Object with given slugs does not exist."),
        "invalid": _("Invalid value."),
    }

    def __init__(self, slug_fields=None, pk="id", pk_field=None, **kwargs):
        assert slug_fields is not None, "The `slug_fields` argument is required."
        self.slug_fields = slug_fields
        self.pk = pk
        self.pk_field = pk_field
        super().__init__(**kwargs)

    def to_internal_value(self, data):
        queryset = self.get_queryset()
        try:
            return queryset.get(**{field: data[field] for field in self.slug_fields})
        except queryset.model.DoesNotExist:
            self.fail("does_not_exist")
        except (TypeError, ValueError):
            self.fail("invalid")

    def to_representation(self, value):
        data = {field: getattr(value, field) for field in self.slug_fields}
        if self.pk_field is not None:
            data[self.pk] = self.pk_field.to_representation(value.pk)
        return data
