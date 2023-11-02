from rest_framework.pagination import PageNumberPagination as drf_PageNumberPagination


# 页码分页
class PageNumberPagination(drf_PageNumberPagination):
    # 每页显示条数
    page_size = 20
    # 分页关键字
    page_query_param = 'page'
    # 大小关键字
    page_size_query_param = 'size'
    # 最大条数
    max_page_size = 100
