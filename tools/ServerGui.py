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
import os
import time

#--------------------------------------------------

wss =[]
class WSHandler(tornado.websocket.WebSocketHandler):
  def open(self):
    print 'New user is connected.\n' 
    if self not in wss:
      wss.append(self)
  def on_close(self):
    print 'connection closed\n'
    if self in wss:
      wss.remove(self)

def wsSend(message):
    for ws in wss:
        if not ws.ws_connection.stream.socket:
            print "Web socket does not exist anymore!!!"
            wss.remove(ws)
        else:
            ws.write_message(message)

#--------------------------------------------------

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")

#def make_app():
#    return tornado.web.Application([
#        (r"/", MainHandler),
#        (r'/ws', WSHandler),
#    ])

lastInfo = [0,0,0,0]
lastCoapAddr = "-"

def read_temp():
    temp = "61;20"
    temp = "%s"%(int(time.time())%100) +";" + "%s"%(int(time.time()*100)%100)
    temp += (";"+ "%s"%(int(time.time())%100) 
             +";" + "%s"%(int(time.time()*100)%100))
    #print temp
    wsSend(temp)
    #wsSend("-;-")

def read_temp():
    global lastInfo
    data = ";".join([str(x) for x in lastInfo +[time.time(), lastCoapAddr]])
    wsSend(data)

class ServerGui:
    def __init__(self):
        self.app = None

    def run(self):
        root = os.path.dirname(__file__)+"/www"
        application = tornado.web.Application([
            (r"/", MainHandler),
            (r'/ws', WSHandler),
            #(r"/auto", AutoPageHandler),
            (r"/(.*)", tornado.web.StaticFileHandler, 
             {"path": root, "default_filename": "index.html"})
        ])

        interval_msec = 50

        http_server = tornado.httpserver.HTTPServer(application)
        http_server.listen(8888)

        main_loop = tornado.ioloop.IOLoop.instance()
        sched_temp = tornado.ioloop.PeriodicCallback(read_temp, interval_msec,   io_loop = main_loop)

        sched_temp.start()
        main_loop.start()

        #self.app = make_app()
        #self.app.listen(8888)
        #tornado.ioloop.IOLoop.current().start()

    def receiveCoap(self, srcAddr, msg):
        payload = "".join((chr(x) for x in msg["payload"]))
        payloadInfo = payload.split(",")
        print "COAP", srcAddr, payloadInfo
        try:
            payloadInfo = [int(x) for x in payloadInfo]
            if len(payloadInfo) != 4:
                return
        except:
            return
        
        global lastInfo, lastCoapAddr
        lastInfo = payloadInfo
        lastCoapAddr = srcAddr
        #print srcAddr, msg["options"], 

#---------------------------------------------------------------------------
