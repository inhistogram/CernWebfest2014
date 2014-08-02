
import tornado.ioloop
import tornado.web
import tornado.websocket


class WSHandler(tornado.websocket.WebSocketHandler):

    def open(self):
        print "WebSocket opened"
        # Send message
        self.write_message("Python to JSON")

    def on_message(self, message):
        print "Received:", message

    def on_close(self):
        print "WebSocket closed"

if __name__ == "__main__":
    application = tornado.web.Application([(r"/", WSHandler), ])
    application.listen(8081)
    tornado.ioloop.IOLoop.instance().start()
