
import yaml, os
from tornado import ioloop, web, httpserver, httpclient

service_name = os.path.dirname(__file__).split('/')[-1]
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__),'../..'))
config = yaml.load(open(os.path.join(root_path,'config.yml')))

conf = config['services'].get(service_name,None)
assert conf is not None

class QueryHandler(web.RequestHandler):
    def get(self, param=''):
        self.write("service1: {}\n".format(param))

app = web.Application([
    ("/(.*)", QueryHandler),
    ])

server = httpserver.HTTPServer(app)
server.bind(conf['port'])
server.start(conf['threads_nb'])
ioloop.IOLoop.current().start()

