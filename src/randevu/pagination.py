from collections import OrderedDict

from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class AppPagination(PageNumberPagination):
    page_query_param= 'page'
    page_size_query_param = 'count'
    max_page_size = 100

    def get_paginated_response(self, data):
        return Response(data)
