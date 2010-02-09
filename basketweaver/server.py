import wee
from gp.fileupload import Storage
#from webob import exc
#import webob
#from webob.multidict import MultiDict

#r'^simple/$'
#r'^simple/(?P<dist_name>[\w\d_\.\-]+)/(?P<version>[\w\.\d\-_]+)/$'
#r'^simple/(?P<dist_name>[\w\d_\.\-]+)/$'
#r'^$'
#r'^(?P<dist_name>[\w\d_\.\-]+)/$'

@wee.post(r'^/simple/$')
def simple(request):
    print request
    import pdb;pdb.set_trace()
    return 'test'

@wee.post(r'^$')
def post(request):
    pass

bw_app = wee.make_app()
if __name__ == "__main__":
    print 'Test'
    from wsgiref.simple_server import make_server
    srv = make_server('localhost', 8080, bw_app)
    srv.serve_forever()
    