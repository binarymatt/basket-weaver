from paste.deploy.loadwsgi import loadapp
from pkg_resources import Requirement, resource_filename
try:
    from wsgi_intercept.httplib2_intercept import install
    install()
    import wsgi_intercept
    import httplib2
    
except ImportError, e:
    raise ImportError("httplib2 and wsgi_intercept needed for tests: %s" %e)

req = Requirement.parse('basketweaver')

_app = None
def test_app():
    global _app
    _app = loadapp('config:sample.ini',
                   **dict(global_conf={},
                          relative_to=resource_filename(req, 'docs')
                          )
                   )
    return _app

wsgi_intercept.add_wsgi_intercept('basket', 80, test_app)

