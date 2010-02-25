from __future__ import with_statement
from basketweaver.makeindex import main as makeindex
from basketweaver.path import path
from gp.fileupload import Storage
from paste.config import ConfigMiddleware, CONFIG
from paste.urlparser import StaticURLParser
from webob import Response
from basketweaver import utils
import os
import pkg_resources
import tempfile
import wee

try:
    import simplejson as json
except ImportError:
    import json
    
req = pkg_resources.Requirement.parse('basketweaver')
data = pkg_resources.resource_filename(req, 'data')


@wee.post(r'^/$')
def upload(request):
    repo_dir = CONFIG['repo_dir']
    fp = request.POST['content'].file.getvalue().strip()
    filepath = path(CONFIG['upload_dest_dir']) / fp
    user = request.headers['Authorization'].split(' ')[1].decode('base64').split(":")[0]
    filename = request.POST['content'].filename
    filepath.copy(path(repo_dir) / filename)
    upload_md = dict(request.POST)
    upload_md['user'] = user
    upload_md['pkg_filename'] = filename
    recreate_index(repo_dir)
    request.environ['gp.fileupload.purge'](filepath)
    return Response(status=200)


@wee.post(r'^/regenerate-index$')
def regenerate_index(request):
    repo_dir = CONFIG['repo_dir']
    recreate_index(repo_dir)
    return Response(status=200)


def recreate_index(repo_dir):
    repo_dir = path(repo_dir)
    with utils.pushd(repo_dir):
        pkgs = [x.relpath() for x in repo_dir.files() if x.endswith('gz') or x.endswith('egg')]
        makeindex(pkgs)


@wee.get(r'^/$')
@utils.unwsgify
def static_dispatch(environ, start_response):
    return environ['basketweaver.static'](environ, start_response)

    
tmpdir = tempfile.mkdtemp('basketweaver.server')


def make_app(global_conf, **app_conf):
    global_conf.update(app_conf)
    conf = global_conf
    
    pm = conf.pop('postmortem', 'false')
    max_size = conf.get('upload_max_size', 150000)
    udd = conf.get('upload_dest_dir', None)
    app = app_factory(udd, max_size, pm=pm, config=conf)
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
