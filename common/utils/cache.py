from django.core.cache import cache


class CacheFnMixin:
    def delete_cache_by_path_prefix(self, path: str | list = None):
        if path is None:
            path = self.request.path
            if self.request.method != "POST":
                path = "/".join(path.split("/")[:-2])
        elif isinstance(path, list):
            for p in path:
                self.delete_cache_by_path_prefix(p)
        keys = cache.keys(f"{path}*")
        cache.delete_many(keys)

    @staticmethod
    def list_cache_key_func(request, *args, **kwargs):
        query_params = "&".join([f"{k}={v}" for k, v in request.query_params.items()])
        return f"{request.path}?{query_params}&request_user={request.user}"

    @staticmethod
    def object_cache_key_func(request, *args, **kwargs):
        return f"{request.path}?request_user={request.user}"

    def perform_create(self, serializer):
        self.delete_cache_by_path_prefix()
        serializer.save()

    def perform_update(self, serializer):
        self.delete_cache_by_path_prefix()
        serializer.save()

    def perform_destroy(self, instance):
        self.delete_cache_by_path_prefix()
        instance.delete()
