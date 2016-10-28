from time import time

from django.db import connection


def test_middleware(get_response):
    def middleware(request):
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

        stats = b"Total Time: %(total)f, Python Time: %(py)f, DB Time: %(db)f, Queries: %(queries)d" % {
            b'total': total_time,
            b'py': py_time,
            b'db': db_time,
            b'queries': queries
        }

        response.content = response.content.replace(b"<!-- STATS -->", stats)
        return response
    return middleware
