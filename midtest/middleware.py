from time import time

from django.conf import settings
from django.db import connection
from django.template.loader import render_to_string


def test_middleware(get_response):
    def middleware(request):
        if not settings.DEBUG:
            return get_response(request)

        # Get beginning stats
        start_queries = len(connection.queries)
        start_time = time()

        # Process the request
        response = get_response(request)

        # Calculate stats
        total_time = time() - start_time
        queries = len(connection.queries) - start_queries
        db_time = 0
        if queries:
            for query in connection.queries[start_queries:]:
                db_time += float(query['time'])
        py_time = total_time - db_time

        # Render the result
        stats = render_to_string("stats_fragment.html", {
            'total_time': total_time,
            'py_time': py_time,
            'db_time': db_time,
            'queries': queries,
        })

        response.content = response.content.replace(b"<!-- STATS -->", response.make_bytes(stats))
        return response
    return middleware
