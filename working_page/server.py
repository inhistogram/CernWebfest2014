
import tornado.ioloop
import tornado.web
import tornado.websocket
import tornado.httpserver

import numpy as np
import json


dataset = np.load("serverdata/LHCbData.npy")
arr1 = dataset['D0_PT']
arr2 = dataset['D0_TAU']

hist1 = np.histogram(arr1, bins = 20, range = (0., 20000))
hist2 = np.histogram(arr2, bins = 20, range = (0., 0.020))
def SimpleEncode(ndarray):
    return json.dumps(ndarray.tolist())

def CenterBinEdges(hist):
    return (hist[1][:-1]+hist[1][1:])/2

def HistJson( histname, hist):
    valuejson = '"value": '+ SimpleEncode(hist[0])
    centerjson = '"key": '+ SimpleEncode(CenterBinEdges(hist))
    histjson = '{ "name": \"'+histname+'\",'+ valuejson + ',' + centerjson +' }'
    return histjson


class WSHandler(tornado.websocket.WebSocketHandler):

    def open(self):
        print "WebSocket opened"
        # Send histogram 1 to frontend
        self.write_message(HistJson("hist1", hist1))
        # Send histogram 2 to frontend
        self.write_message(HistJson("hist2", hist2))
        #self.write_message('{ "value" :[0, 0, 21223, 19141, 7204, 3339, 1626, 834, 464, 250, 121, 67, 36, 28, 8, 7, 2, 1, 0, 1], "key": [0.0, 1000.0, 2000.0, 3000.0, 4000.0, 5000.0, 6000.0, 7000.0, 8000.0, 9000.0, 10000.0, 11000.0, 12000.0, 13000.0, 14000.0, 15000.0, 16000.0, 17000.0, 18000.0, 19000.0, 20000.0]}')


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
            'template_path': 'templates',
            'autoreload' : True
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
