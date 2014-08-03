
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

def genHistogram(varName, filterArray = None, bins = 20, binRange = None):
    filter
    if binRange is None:
        binRange = (dataset[varName].min() , dataset[varName].max())
    if filterArray is None:
        hist = np.histogram(dataset[varName], bins, range = binRange )
    else:
        hist = np.histogram(dataset[varName][filterArray], bins, range = binRange )
    return hist


def basicSetReducer( dataset, varName, selList ):

    if selList == "":
        selList = [float("-inf"), float("inf")]

    boolArray =  (dataset[varName] > selList[0] ) & (dataset[varName] < selList[1])

    return boolArray


class WSHandler(tornado.websocket.WebSocketHandler):

    def open(self):
        print "WebSocket opened"
        # Send histogram 1 to frontend
        #self.write_message(HistJson('D0_PT',genHistogram('D0_PT', bins = 20)))
        # Send histogram 2 to frontend
        #self.write_message(HistJson('D0_TAU',genHistogram('D0_TAU', bins = 20)))


    def on_message(self, message):
        print "Received:", message
        message = json.loads(message)
        varName = message["var"]
        print varName
        bin_edges = message["bin_edges"]
        print bin_edges
        selection = message["selection"]
        print selection
        filterArray = basicSetReducer( dataset, varName, selection ) 
        self.write_message(HistJson(varName,genHistogram(varName, filterArray = filterArray, bins = 20)))

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

if __name__ == "__main__":
    ws_app = Application()
    http_server = tornado.httpserver.HTTPServer(ws_app)
    ws_app.listen(8081)
    tornado.ioloop.IOLoop.instance().start()
