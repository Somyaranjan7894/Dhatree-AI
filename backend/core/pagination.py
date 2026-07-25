"""
Standardized API pagination classes for Dhatree AI.
Ensures uniform metadata (total_count, total_pages, current_page) across all list endpoints.
"""
from typing import Any, Dict
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class DhatreePageNumberPagination(PageNumberPagination):
    """
    PageNumberPagination with standardized response metadata wrapper.
    Response shape:
    {
        "status": "success",
        "meta": {
            "count": 100,
            "next": "http://...",
            "previous": "http://...",
            "page_size": 20
        },
        "data": [ ... items ... ]
    }
    """

    page_size = 20
    page_size_query_param = "page_size"
    max_page_size = 100

    def get_paginated_response(self, data: Any) -> Response:
        return Response(
            {
                "status": "success",
                "meta": {
                    "count": self.page.paginator.count,
                    "next": self.get_next_link(),
                    "previous": self.get_previous_link(),
                    "page_size": self.get_page_size(self.request),
                },
                "data": data,
            }
        )
