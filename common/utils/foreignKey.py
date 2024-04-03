def foreign_key_update(field: list, request_data: dict, instance: any):
    """
    This function is used to update the foreign key field of the instance.
    """
    for key in field:
        if key in request_data:
            getattr(instance, key).set(request_data[key])
