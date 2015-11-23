#! /usr/bin/python
#---------------------------------------------------------------------------
# Cut&paste from misc sources, starting from: 
# 
# http://iot-projects.com/index.php?id=raspberry-pi-temperature-visualization-using-websocket" (by Ratko Grbic)
# 
#---------------------------------------------------------------------------

import tornado.httpserver
import tornado.websocket
import tornado.ioloop
import tornado.web
import os, socket
import time

Version = (1,0)

#--------------------------------------------------

def makeBigTable():
    s = "<table>"
    s += "".join(["<tr>"+
                  "".join(["<td>%s,%s</td>"%(x,y)  for x in range(30) ])
                  +"</tr>"
                  for y in range(30)])
    s += "</table>"
    return s

#--------------------------------------------------

globalList = []

OutPort = 5800

class WSHandler(tornado.websocket.WebSocketHandler):
    def setServer(self, mainServer):
        self.mainServer = mainServer

    def open(self):
        self.mainServer.openWS(self)

    def on_close(self):
        self.mainServer.closeWS(self)

#--------------------------------------------------

from time import gmtime, strftime

class ServerCanvas:
    def __init__(self):
        self.app = None
        self.sd = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.wsClientList = []

    def run(self):
        root = os.path.join(os.path.dirname(__file__), "www-graph")
        print root
        application = tornado.web.Application([
            (r'/ws', self.makeWSHandler),
            (r"/(.*)", tornado.web.StaticFileHandler, 
             {"path": root, "default_filename": "index.html"})
        ])

        interval_msec = 50

        http_server = tornado.httpserver.HTTPServer(application)
        http_server.listen(8888)

        main_loop = tornado.ioloop.IOLoop.instance()
        sched_temp = tornado.ioloop.PeriodicCallback(
          self.sendAllTime, interval_msec, io_loop = main_loop)

        sched_temp.start()
        main_loop.start()

    def makeWSHandler(self, *args):
        global globalList
        result = WSHandler(*args) #, serverGraph=self)
        result.setServer(self)
        globalList.append(result)
        return result

    def openWS(self, ws):
        if ws not in self.wsClientList:
            print 'New user is connected.\n' #, dir(ws)
            self.wsClientList.append(ws)
            ws.write_message({"type":"init", "version": Version})

    def closeWS(self, ws):
        print 'connection closed\n'
        if self in self.wsClientList:
            self.wsClientList.remove(self)

    def sendAll(self, message):
        for ws in self.wsClientList[:]:
            if ws.ws_connection == None:
                print "Web socket does not exist anymore!!!"
                self.wsClientList.remove(ws)
            else:
                ws.write_message(message)

    def sendAllTime(self):
        data = {"type":"time", 
                "time": strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())}
        self.sendAll(data)

#---------------------------------------------------------------------------

server = ServerCanvas()
server.run()

#---------------------------------------------------------------------------
