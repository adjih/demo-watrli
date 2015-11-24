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
import time, random

import argparse

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

xSize = 1024
xSize = 1400
ySize = 400

NodePyDat = "testbed-all.pydat"

if os.path.exists(NodePyDat):
    with open(NodePyDat) as f:
        testbedInfo = eval(f.read())

    arduinoPosList = []
    a8PosList = []
    arduinoTable = {}
    a8Table = {}

    for nodeInfo in testbedInfo:
        xyz = nodeInfo['xyz'] 
        x,y,z = xyz
        if z < 1.1: # not on top
            continue 
        if y>10: # outdoors node
            continue
        if "arduino" in nodeInfo:
            arduinoPosList.append(xyz[0:2])
            #print z
            arduinoId = nodeInfo["arduino"]["arduino-id"]
            arduinoTable[arduinoId] = xyz[0:2]
        else: 
            a8PosList.append(xyz[0:2])
            a8Table[nodeInfo["id"]] = xyz[0:2]

    print arduinoPosList
    print a8PosList
else:
    arduinoPosList = []
    a8PosList = []

def minMaxIdx(l, idx):
    ll = [u[idx] for u in l]
    return min(ll), max(ll)

x0,x1 = minMaxIdx(arduinoPosList+a8PosList, 0)
y0,y1 = minMaxIdx(arduinoPosList+a8PosList, 1)
margin = 10

if (x1-x0)* (ySize-2*margin) > (y1 -y0)*(xSize -2*margin):
    scale = (xSize -2*margin) /float (x1-x0)
    dx = margin
    dy = margin
else: 
    scale = (ySize -2*margin) /float (y1-y0)
    dx = margin
    dy = margin

def scaleXY(x,y):
    global x0,y0,scale
    return (x-x0)*scale+margin, ((y1-y)*scale+margin)

print x0,x1,y0,y1, dx,dy, margin,scale

def OLDgetNodeGraphList():
    res = []
    for u,(x,y) in a8Table.iteritems():
        xx,yy = scaleXY(x,y)
        res.append(("create", "a8-%s"%u, ("ball", xx, yy, 5, 0.5)))
    for u,(x,y) in arduinoTable.iteritems():
        xx,yy = scaleXY(x,y)
        res.append(("create", "ard-%s"%u, ("ball", xx, yy, 7, 0.8)))

    return res


#--------------------------------------------------

class GraphManager:
    def __init__(self, args):
        self.pendingList = []
        self.content = {}
        self.newContent = {}
        self.newContentNameList = []
        self.elemId = 0
        self.args = args

    def delete(self, name):
        if name in self.content:
            del self.content[name]
            self.pendingList.append(("delete", name))
        elif name in self.newContent:
            del self.newContent[name]
            self.newContentNameList.remove(name)

    def clear(self):
        for k in self.content.iterkeys():
            self.pendingList.append(("delete", k))
        self.content = {}

    def getUpdateList(self, doClearCurrent=True):
        result = self.pendingList[:]
        self.pendingList = []
        for k in self.newContentNameList:
            v = self.newContent[k]
            if (k not in self.content):
                result.append(("create", k, v))
                if self.args.verbose:
                    print ("create", k, v)
            elif self.content[k]  != v:
                result.append(("update", k, v))
                if self.args.verbose:
                    print ("update", k, v)
        self.content.update(self.newContent)
        self.newContent = {}
        self.newContentNameList = []
        return result
            
    def _ensureName(self, name):
        if name == None:
            name = "obj%s" % self.elemId
            self.elemId += 1
        return name
            
    def drawBall(self, name, x, y, r, color):
        name = self._ensureName(name)
        elem = ("ball", x, y, r, color)
        self.newContent[name] = elem
        self.newContentNameList.append(name)
        return name

    def drawLine(self, name, xyList, width, color):
        name = self._ensureName(name)
        self.newContent[name] = (name)
        def scaleXY(*u):
            return u
        data = "M%d,%d" % scaleXY(*xyList[0])
        for i in range(1, len(xyList)):
            data += "L%d,%d" % scaleXY(*xyList[i])
        elem = ("line", {"path":data, "stroke":color, "stroke-width":width})
        self.newContent[name] = elem
        self.newContentNameList.append(name)
        return name


def getRandomArduino(previousNodeId):
    global arduinoTable
    potentialParentList = [
        nodeId for nodeId in arduinoTable.keys()
        if arduinoTable[previousNodeId][0] < arduinoTable[nodeId][0] <= arduinoTable[previousNodeId][0] +10  ]
    #print potentialParentList
    if len(potentialParentList) == 0:
        return None
    return random.choice(potentialParentList)


class PathDisplay:
    def __init__(self, graphManager):
        self.sourceArduino = 41
        self.currentPath = [self.sourceArduino]
        random.seed(0)
        self.graphManager = graphManager
        self.pathNameSet = set()

    def increasePath(self):
        newNode = getRandomArduino(self.currentPath[-1])
        if newNode == None:
            self.destroyCurrentPath()
        else:
            self.currentPath.append(newNode)
        xyList = [arduinoTable[nodeId] for nodeId in self.currentPath]
        xyList = [scaleXY(*xy) for xy in xyList ]
        n = self.graphManager.drawLine("packet-path", xyList, 3,
                                       "#ff0000")
        

        (x,y) = arduinoTable[nodeId]
        xx,yy = scaleXY(x,y)
        n = self.graphManager.drawBall("tmp%d"%nodeId, xx, yy, 10, 0.0)
        self.pathNameSet.add(n)

    def destroyCurrentPath(self):
        self.currentPath = [self.sourceArduino]
        for n in self.pathNameSet:
            self.graphManager.delete(n)

    def getContent(self):
        if len(self.xList) == 0:
            return res

        data = "M%d,%d" % scaleXY(self.xList[0], self.yList[0])
        for i in range(1, len(self.xList)):
            data += "L%d,%d" % scaleXY(self.xList[i], self.yList[i])
        res += [("path", "line", data, "#ff0000", 3)]

        return res


def plotAllNode(graphManager):
    for u,(x,y) in a8Table.iteritems():
        xx,yy = scaleXY(x,y)
        graphManager.drawBall("a8-%s"%u, xx, yy, 5, 0.5)
    for u,(x,y) in arduinoTable.iteritems():
        xx,yy = scaleXY(x,y)
        graphManager.drawBall("ard-%s"%u, xx, yy, 7, 0.8)

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

RaphaelJsUrl = "http://raphaeljs.com/raphael.js"
SmoothieJsUrl = "http://smoothiecharts.org/smoothie.js"
JQueryJsUrl = "http://code.jquery.com/jquery-2.0.0.js"

class ServerCanvas:
    def __init__(self, args):
        self.args = args
        self.app = None
        self.sd = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.wsClientList = []

    def run(self):
        root = os.path.join(os.path.dirname(__file__), "www-graph")
        print root

        raphaelJs = os.path.join(root, "raphael.js")
        if not os.path.exists(raphaelJs):
            os.system("cd "+root+" && wget "+RaphaelJsUrl)
        smoothieJs = os.path.join(root, "smoothie.js")
        if not os.path.exists(smoothieJs):
            os.system("cd "+root+" && wget "+SmoothieJsUrl)
        jQueryJs = os.path.join(root, "jquery-2.0.0.js")
        if not os.path.exists(jQueryJs):
            os.system("cd "+root+" && wget "+JQueryJsUrl)

        application = tornado.web.Application([
            (r'/ws', self.makeWSHandler),
            (r"/(.*)", tornado.web.StaticFileHandler, 
             {"path": root, "default_filename": "index.html"})
        ])

        self.lastTime = time.time()
        interval_msec = 50

        http_server = tornado.httpserver.HTTPServer(application)
        http_server.listen(8008)

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
            self.graphManager = GraphManager(self.args)
            self.pathDisplay = PathDisplay(self.graphManager)

            self.wsClientList.append(ws)
            msg = { "type": "init", 
                    "version": Version,
                    "xSize": xSize, 
                    "ySize": ySize }
            ws.write_message(msg)
            #[ ("b%s-%s"%(x,y), "ball", x*20,y*20, 10, ((x+y)%11)/float(10))
            #    for x in range(10) for y in range(10) ]
            plotAllNode(self.graphManager)
            contentList = self.graphManager.getUpdateList()
            #print contentList
            #d = {"fill": "#f00"}
            #contentList = [("create", "c1", ("circle", 100,100,20,d))]

            msg = { "type": "draw", "content": contentList }
            ws.write_message(msg)



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
        if len(self.wsClientList[:]) == 0:
            return
        t = time.time()

        data = {"type":"time", 
                "time": strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime()),
                "x": t, "y": t - int(t) }
        self.sendAll(data)

        PathIncreaseInterval = 0.2
        while t > self.lastTime + PathIncreaseInterval:
            self.pathDisplay.increasePath()
            self.lastTime += PathIncreaseInterval

        data = { "type": "draw",
                 "content": self.graphManager.getUpdateList() }
        self.sendAll(data)

#---------------------------------------------------------------------------

parser = argparse.ArgumentParser()
parser.add_argument("-v", dest="verbose", action="store_true", default=False)
args = parser.parse_args()

print args

server = ServerCanvas(args)
server.run()

#---------------------------------------------------------------------------
