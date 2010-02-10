from webob import Response
import functools
import inspect


def unwsgify(func, catch_exc_info=True):
    """
    We've got a webob request and need to call a normal wsgi handler
    
    borrowed from:
    http://bitbucket.org/ianb/webob/src/tip/webob/request.py#cl-882
    """
    def start_response(status, headers, exc_info=None, captured=[], output=[]):
        if exc_info is not None and not catch_exc_info:
            raise exc_info[0], exc_info[1], exc_info[2]
        captured[:] = [status, headers, exc_info]
        return output.append

    @functools.wraps(func)
    def wrapper(request):
        ret = func(request.environ, start_response)
        if isinstance(ret, Response):
            return ret
        spec = inspect.getargspec(start_response)
        status = spec[3][1][0]
        return Response(body=ret[0], status=status)
    return wrapper
