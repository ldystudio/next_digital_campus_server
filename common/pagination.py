from rest_framework.pagination import (
    LimitOffsetPagination,
    PageNumberPagination as drf_PageNumberPagination,
)


# 页码分页
class PageNumberPagination(drf_PageNumberPagination):
    # 每页显示条数
    page_size = 10
    # 分页关键字
    page_query_param = "page"
    # 大小关键字
    page_size_query_param = "size"
    # 最大条数
    max_page_size = 100


class UnlimitedPagination(LimitOffsetPagination):
    # 设置每页数量为无限大
    default_limit = 1000000
    max_limit = None
