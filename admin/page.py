from rest_framework.pagination import PageNumberPagination, Response
from collections import OrderedDict


# 后台标准分页（需要指定当前页码）
class StandardPagination(PageNumberPagination):
    page_size = 10  # 表示每页的默认显示数量
    max_page_size = 100  # 表示每页最大显示数量，做限制使用
    # page_size_query_param = 'size'  # 表示url中的每页显示条数
    page_query_param = 'page'  # 表示url中的当前页码


# 前端首页文章分页(需要指定当前页码 + 每页显示条数)
class FrontPagination(PageNumberPagination):
    max_page_size = 100  # 表示每页最大显示数量，做限制使用
    page_size_query_param = 'size'  # 表示url中的每页显示条数
    page_query_param = 'page'  # 表示url中的当前页码


# 返回分页数据
def get_page_response(self, data):
    return Response(OrderedDict([
        ('count', self.page.paginator.count),  # 总记录数
        ('next', self.get_next_link()),  # 下一页URL
        ('previous', self.get_previous_link()),  # 上一页URL
        ('results', data),  # 分页数据
        ('total_pages', self.page.paginator.num_pages),  # 总页数
        ('current_page', self.page.number),  # 当前页
        ('page_size', self.page_size),  # 每页条数
    ]))
