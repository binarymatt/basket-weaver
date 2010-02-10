from basketweaver.utils import unwsgify
from gp.fileupload import Storage
from os import path
from paste.config import ConfigMiddleware, CONFIG
from paste.urlparser import StaticURLParser
from webob import Response
from basketweaver.makeindex import main as makeindex
import os
import pkg_resources
import tempfile
import wee

req = pkg_resources.Requirement.parse('basketweaver')
data = pkg_resources.resource_filename(req, 'data')
#from webob import exc
#import webob
#from webob.multidict import MultiDict

#r'^simple/$'
#r'^simple/(?P<dist_name>[\w\d_\.\-]+)/(?P<version>[\w\.\d\-_]+)/$'
#r'^simple/(?P<dist_name>[\w\d_\.\-]+)/$'
#r'^$'
#r'^(?P<dist_name>[\w\d_\.\-]+)/$'

## @wee.post(r'^$')
## def post(request):
##     pass


@wee.post(r'^/$')
def upload(request):
    #this is sort of janky
    import pdb;pdb.set_trace()
    repo_dir = CONFIG['repo_dir']
    filepath = path.join(CONFIG['upload_dest_dir'], request.environ.get('HTTP_STORED_PATHS'))
    print filepath
    print path.join(repo_dir, request.POST['content'].filename)
    try:
        os.rename(filepath, path.join(repo_dir, request.POST['content'].filename))
    except Exception, e:
        print e
        import pdb;pdb.set_trace()
        
    recreate_index(repo_dir)
    return Response(status=200)


def recreate_index(repo_dir):
    opdir = path.abspath(os.curdir)
    os.chdir(repo_dir)
    makeindex("*")
    os.chdir(opdir)


@wee.get(r'^/$')
@unwsgify
def static_dispatch(environ, start_response):
    return environ['basketweaver.static'](environ, start_response)

    
tmpdir = tempfile.mkdtemp('basketweaver.server')


def make_app(global_conf, **app_conf):
    global_conf.update(app_conf)
    conf = global_conf
    
    pm = conf.pop('postmortem', 'false')
    max_size = conf.get('upload_max_size', 150000)

    app = app_factory(max_size, pm=pm, config=conf)
    app.conf = conf.copy()
    app = ConfigMiddleware(app, conf)
    return app


def app_factory(udd=None, max_size=150000, repo_dir=data, cache_age=None, pm=True, config=None):
    app = wee.make_app()
    
    tmpdir =  os.path.join(tempfile.gettempdir(), 'basketweave')
    if udd is None:
        udd = path.join(repo_dir, 'sessions')

    if config is not None:
        config['upload_dest_dir'] = udd
        
    print "UPLOAD DIR: %s" %udd
    app = Storage(app, upload_to=udd, tempdir=tmpdir, max_size=max_size)
 
    if pm != 'false':
        from repoze.debug.pdbpm import PostMortemDebug
        app = PostMortemDebug(app)

    #app = trace(app)
    app = StaticDelegate(app, repo_dir, cache_max_age=cache_age)
    return app


class StaticDelegate(object):
    
    def __init__(self, app, directory, root_directory=None, cache_max_age=None):
        self.app = app
        self.static = StaticURLParser(directory, root_directory=None, cache_max_age=None)
        
    def __call__(self, environ, start_reponse):
        environ['basketweaver.static'] = self.static
        return self.app(environ, start_reponse)

        
class trace(object):
    
    def __init__(self, app):
        self.app = app

    def __call__(self, env, start_reponse):
        import pdb;pdb.set_trace()
        return self.app(env, start_reponse)


if __name__ == "__main__":
    print 'Test'
    from wsgiref.simple_server import make_server
    srv = make_server('localhost', 8080, app_factory)
    srv.serve_forever()
