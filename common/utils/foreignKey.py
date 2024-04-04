def foreign_key_fields_update(field: list, request_data: dict, instance: any):
    """
    This function is used to update the foreign key field of the instance.
    """
    for key in field:
        if key in request_data:
            getattr(instance, key).set(request_data[key])


def foreign_key_fields_create(field: list, request_data: dict, serializer: any):
    """
    This function is used to create the foreign key field of the instance.
    """
    for key in field:
        if key in request_data:
            serializer.validated_data[key] = request_data[key]
