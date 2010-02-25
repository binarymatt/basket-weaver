from contextlib import contextmanager
from webob import Response
import functools
import inspect
import os


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


@contextmanager
def pushd(dir):
    '''
    modified from http://www.blueskyonmars.com/projects/paver .
    
    A context manager (Python 2.5+ only) for stepping into a 
    directory and automatically coming back to the previous one. 
    The original directory is returned. Usage is like this::
    
        from __future__ import with_statement
        # the above line is only needed for Python 2.5
        
        from paver.easy import *
        
        @task
        def my_task():
            with pushd('new/directory') as old_dir:
                ...do stuff...
    '''
    old_dir = os.getcwd()
    os.chdir(dir)
    try:
        yield old_dir
    finally:
        os.chdir(old_dir)


def pm(func):
    @functools.wraps(func)
    def postm(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception, e:
            import pdb, sys; pdb.post_mortem(sys.exc_info[2])
            raise e
    return postm
