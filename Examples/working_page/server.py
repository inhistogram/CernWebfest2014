
import tornado.ioloop
import tornado.web
import tornado.websocket
import tornado.httpserver

import os.path
import mimetypes


class WSHandler(tornado.websocket.WebSocketHandler):

    def open(self):
        print "WebSocket opened"
        # Send message
        self.write_message("Python to JSON")

    def on_message(self, message):
        print "Received:", message
        self.write_message(u"Your message was: " + message)

    def on_close(self):
        print "WebSocket closed"


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r'/', IndexPageHandler),
            (r'/websocket', WSHandler),
            (r'/data/(.*)', tornado.web.StaticFileHandler, dict(path = "data"),)
            ]

        settings = {
            'template_path': 'templates'
        }
        tornado.web.Application.__init__(self, handlers, **settings)

class IndexPageHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")

if __name__ == "__main__":
    ws_app = Application()
    http_server = tornado.httpserver.HTTPServer(ws_app)
    ws_app.listen(8081)
    tornado.ioloop.IOLoop.instance().start()