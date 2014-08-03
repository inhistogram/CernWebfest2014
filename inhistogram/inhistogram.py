
import tornado.ioloop
import tornado.web
import tornado.websocket
import tornado.httpserver

import numpy as np
import json




def getListVarNames(ndarray):
    return list(ndarray.dtype.names)

def getVarInfo(dataset, varNames = None ):
    varInfo = {}
    if varNames == None:
        varNames = list(dataset.dtype.names)

    for varName in varNames:
        varInfo[varName] = {}
        varInfo[varName]["nValues"] = dataset[varName].size
        varInfo[varName]["minValue"] = dataset[varName].min()
        varInfo[varName]["maxValue"] = dataset[varName].max()
        varInfo[varName]["meanValue"] = dataset[varName].mean()
    return varInfo


def SimpleEncode(ndarray):
    return json.dumps(ndarray.tolist())

def CenterBinEdges(hist):
    return (hist[1][:-1]+hist[1][1:])/2

def HistJson( histname, hist):
    valuejson = '"value": '+ SimpleEncode(hist[0])
    centerjson = '"edges": '+ SimpleEncode(hist[1])
    histjson = '{ "name": \"'+histname+'\",'+ valuejson + ',' + centerjson +' }'
    return histjson

def basicSetReducer( dataset, varName, selList ):

    boolArray =  (dataset[varName] > selList[0]) & (dataset[varName] < selList[1])

    return np.where(boolArray)


class WSHandler(tornado.websocket.WebSocketHandler):

    def open(self):
        print "WebSocket opened"
        # Send histogram 1 to frontend
        self.write_message(HistJson('D0_PT', hist1))
        # Send histogram 2 to frontend
        self.write_message(HistJson('D0_TAU', hist2))
        #self.write_message('{ "value" :[0, 0, 21223, 19141, 7204, 3339, 1626, 834, 464, 250, 121, 67, 36, 28, 8, 7, 2, 1, 0, 1], "key": [0.0, 1000.0, 2000.0, 3000.0, 4000.0, 5000.0, 6000.0, 7000.0, 8000.0, 9000.0, 10000.0, 11000.0, 12000.0, 13000.0, 14000.0, 15000.0, 16000.0, 17000.0, 18000.0, 19000.0, 20000.0]}')


    def on_message(self, message):
        print "Received:", message

    def on_close(self):
        print "WebSocket closed"


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r'/', IndexPageHandler),
            (r'/websocket', WSHandler),
            (r'/variables/name', GetListVarNamesHandler),
            (r'/variables/info', GetVarInfoHandler),
            (r'/data/(.*)', tornado.web.StaticFileHandler, dict(path = "data")),
            (r'/css/(.*)', tornado.web.StaticFileHandler, dict(path = "frontend/css")),
            (r'/js/(.*)', tornado.web.StaticFileHandler, dict(path = "frontend/js"))
            ]

        settings = {
            'template_path': 'frontend/templates',
            'autoreload' : True
        }
        tornado.web.Application.__init__(self, handlers, **settings)

class IndexPageHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")

class GetListVarNamesHandler(tornado.web.RequestHandler):
    def get(self):
        answer = {}
        answer["varNames"] = getListVarNames(dataset)
        self.write(json.dumps(answer))

class GetVarInfoHandler(tornado.web.RequestHandler):
    def get(self):
        answer = {}
        answer["varInfo"] = getVarInfo(dataset)
        self.write(json.dumps(answer))




dataset = np.load("data/LHCbData.npy")
arr1 = dataset['D0_PT']
arr2 = dataset['D0_TAU']

hist1 = np.histogram(arr1, bins = 20, range = (0., 20000))
hist2 = np.histogram(arr2, bins = 20, range = (0., 0.020))

if __name__ == "__main__":
    ws_app = Application()
    http_server = tornado.httpserver.HTTPServer(ws_app)
    ws_app.listen(8081)
    tornado.ioloop.IOLoop.instance().start()
