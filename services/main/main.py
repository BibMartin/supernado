import yaml, os
from tornado import ioloop, web, httpserver, httpclient

service_name = os.path.dirname(__file__).split('/')[-1]
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__),'../..'))
config = yaml.load(open(os.path.join(root_path,'config.yml')))

conf = config['services'].get(service_name,None)
assert conf is not None

class AsynchronousHandler(web.RequestHandler):
    @web.asynchronous
    def get(self, service, uri=''):
        client = httpclient.AsyncHTTPClient()
        conf = config['services'].get(service,None)
        if conf is None:
            raise web.HTTPError(500,reason='Service {} not known.'.format(service))
        url = conf.get('url',None)
        if url is None:
            raise web.HTTPError(500,reason='Service {} has no url.'.format(service))
        response = client.fetch(url + uri,self.on_response)
    def on_response(self, response):
        self.write(response.body)
        self.finish()

class QueryHandler(web.RequestHandler):
    def get(self, url):
        self.write("Hello from main/" + url)

app = web.Application([
    ("/", QueryHandler),
    ("/(.*?)/(.*)", AsynchronousHandler),
    ("/(.*)", AsynchronousHandler),
    ])

server = httpserver.HTTPServer(app)
server.bind(conf['port'])
server.start(conf['threads_nb'])
ioloop.IOLoop.current().start()

