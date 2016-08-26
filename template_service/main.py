import yaml
import os
from tornado import ioloop, web, httpserver

service_name = os.path.dirname(__file__).split('/')[-1]
service_path = os.path.abspath(os.path.dirname(__file__))
conf = yaml.load(open(os.path.join(service_path, 'config.yml')))

assert conf is not None


class SomeHandler(web.RequestHandler):
    def get(self, param=''):
        self.write(
            "Hello form service {}. "
            "You've asked for uri {}\n".format(service_name, param))

app = web.Application([
    ("/(.*)", QueryHandler),
    ])

server = httpserver.HTTPServer(app)
server.bind(conf['port'])
server.start(conf['threads_nb'])
ioloop.IOLoop.current().start()
