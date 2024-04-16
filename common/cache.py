from functools import wraps, WRAPPER_ASSIGNMENTS

from django.core.cache import cache
from rest_framework_extensions.cache.decorators import CacheResponse

from common.utils.decide import is_admin
from django.conf import settings
from pydash import map_


class CacheFnMixin:
    cache_paths_to_delete = [None]

    def delete_cache_by_path_prefix(self, path: str | set | None):
        request = self.request
        if path is None:
            path = request.path
            if request.method != "POST":
                path = "/".join(path.split("/")[:-2])
        elif isinstance(path, (set, list)):
            for p in path:
                self.delete_cache_by_path_prefix(p)
        keys = (
            cache.keys(f"{path}*request_user={request.user}")
            if not is_admin(request)
            else cache.keys(f"{path}*")
        )
        cache.delete_many(keys)

    @staticmethod
    def list_cache_key_func(request, *args, **kwargs):
        query_params = "&".join([f"{k}={v}" for k, v in request.query_params.items()])
        return f"{request.path}?{query_params}&request_user={request.user}"

    @staticmethod
    def object_cache_key_func(request, *args, **kwargs):
        return f"{request.path}?request_user={request.user}"

    def get_cache_paths_to_delete(self):
        return map_(
            filter(lambda path: isinstance(path, str), self.cache_paths_to_delete),
            lambda path: f"/{settings.API_VERSION}{path}",
        )

    def perform_create(self, serializer):
        self.delete_cache_by_path_prefix({*self.get_cache_paths_to_delete(), None})
        serializer.save()

    def perform_update(self, serializer):
        self.delete_cache_by_path_prefix({*self.get_cache_paths_to_delete(), None})
        serializer.save()

    def perform_destroy(self, instance):
        self.delete_cache_by_path_prefix({*self.get_cache_paths_to_delete(), None})
        instance.delete()


class CacheAdminUserResponse(CacheResponse):
    def __call__(self, func):
        this = self

        @wraps(func, assigned=WRAPPER_ASSIGNMENTS)
        def inner(self, request, *args, **kwargs):
            if not is_admin(request):
                # 如果用户角色不是 "admin"，需要重定向到详情则直接调用视图函数，不进行缓存
                return func(self, request, *args, **kwargs)

            return this.process_cache_response(
                view_instance=self,
                view_method=func,
                request=request,
                args=args,
                kwargs=kwargs,
            )

        return inner


class CacheOtherUserResponse(CacheResponse):
    def __call__(self, func):
        this = self

        @wraps(func, assigned=WRAPPER_ASSIGNMENTS)
        def inner(self, request, *args, **kwargs):
            if is_admin(request):
                # 如果用户角色是 "admin"，需要重定向到详情则直接调用视图函数，不进行缓存
                return func(self, request, *args, **kwargs)

            return this.process_cache_response(
                view_instance=self,
                view_method=func,
                request=request,
                args=args,
                kwargs=kwargs,
            )

        return inner


cache_admin_user_response = CacheAdminUserResponse
cache_other_user_response = CacheOtherUserResponse
