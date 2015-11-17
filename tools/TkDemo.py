#! /usr/bin/python
#---------------------------------------------------------------------------

import Tkinter, os
from Tkinter import *


import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--socket-id", type=int, default=0) # XXX:useless
parser.add_argument("--name", type=str, default=None)   # XXX:useless
args = parser.parse_args()

if args.name == None:
    socketId = args.socket_id
    moteSelect = "--socket-id %s" % args.socket_id
    moteId = "@%s" % args.socket_id
else:
    moteSelect = "--name %s" % args.name
    moteId = args.name


#import optparse
#
#parser = optparse.OptionParser()
#parser.add_option("--mote-id", dest="moteId", action="store", default=0,
#     type="int")
#(options, argList) = parser.parse_args()


CommandList = [
    ("ping-rpi",
      """roxterm -T PingRPi -e bash -c 'ping rpi ; echo DONE ;sleep 10'"""),
    ("ssh-rpi", """./watrli-tool ssh-rpi"""),
    ("sniffer", 
     """roxterm -T sniffer -e bash -c './watrli-tool sniffer ; echo DONE ;sleep 10'&"""),
    ("sniff 26", 
     """roxterm -T sniffer -e bash -c './watrli-tool sniffer ch26 ; echo DONE ;sleep 10'&"""),

    ("wireshark", 'sudo wireshark -k -i lo -Y "zep" &'),

    ( "RPi Process", None),

    ( "rpi-setup", "./watrli-tool rpi-setup" ),
    ( "rpi-clean-lock", "./watrli-tool rpi-clean-lock" ),
    ( "rpi-dashboard", "./watrli-tool rpi-dashboard" ),
    ( "rpi-proxy", "./watrli-tool rpi-proxy" ),
    ( "rpi-rpld", "./watrli-tool rpi-rpld" ),

    ( "Linux", None ),

    ( "border-router", "./watrli-tool border-router"),
    ( "coap-server", "./watrli-tool coap-server"),
    #( "reset-fox", "./watrli-tool reset fox"),
    #( "term-fox", "./watrli-tool term fox")

    ( "SamR21 XPro", None),

    ( "stop-r21", "./watrli-tool dbg-server"),
    ( "flash-r21", "./watrli-tool flash"),
    ( "sensorapp", "./watrli-tool flash-sensorapp"),
    ( "reset-r21", "./watrli-tool reset"),
    ( "term-r21", "./watrli-tool term"),

    ( "M3", None ),

    ( "flash-m3",  "./watrli-tool flash iot-lab_M3"),
    ( "sensorapp", "./watrli-tool flash-sensorapp iot-lab_M3"),
    ( "reset-m3",  "./watrli-tool reset iot-lab_M3"),
    ( "term-m3",   "./watrli-tool term iot-lab_M3"),

    ( "FOX", None ),

    ( "flash-fox", "./watrli-tool flash fox"),
    ( "sensorapp", "./watrli-tool flash-sensorapp fox"),
    ( "reset-fox", "./watrli-tool reset fox"),
    ( "term-fox", "./watrli-tool term fox")


    # ("reuse-port",
    #  """roxterm -T 'cmd' -e bash -c 'sudo bash -c "echo 1 > /proc/sys/net/ipv4/tcp_fin_timeout"; sudo bash -c "echo 1 > /proc/sys/net/ipv4/tcp_tw_recycle" ; sudo bash -c "echo 1 > /proc/sys/net/ipv4/tcp_tw_reuse" ; echo DONE ;sleep 10' &"""),
    # ("proxy", 
    #  """roxterm -T proxy -e bash -c 'python RealTimeParse.py --proxy --record ; echo DONE ;sleep 10'&"""),

    # ("manager", 
    #  """roxterm -T experiment -e bash -c 'make manager ; echo DONE ;sleep 10'"""),
    # ("manager-continue", 
    #  """roxterm -T experiment -e bash -c 'make manager-real-time ; echo DONE ;sleep 10'"""),

    # ("real-time-parse", 
    #  """roxterm -T "Real Time Analysis" -e bash -c 'python RealTimeParse.py --udp --data-port 2222 ; echo DONE ;sleep 1000'"""),
    # #("real-time-parse2", 
    # # """roxterm -T "Real Time Analysis" -e bash -c 'python RealTimeParse.py --udp --udp-port 2223 --data-port 2222 ; echo DONE ;sleep 10'"""),

    # ("display",
    #  """roxterm -T 'Real Time Display' -e bash -c 'cd plotDemo && python DemoManager.py --data-port 2222 ; echo DONE ;sleep 10' &"""),
    # ("last-state",
    #  """roxterm -T 'Last State Dump' -e bash -c 'watch cat /dev/shm/last-state.log ; sleep 10' &"""),

    # ("replay-fast",
    #  """roxterm -T 'Replay Reader' -e bash -c 'python RealTimeParse.py --replay manager-2014-10-27--00h31m01.log --time-scale 0.1 --data-port 3333 ; echo DONE ;sleep 100' &"""),
    # ("replay",
    #  """roxterm -T 'Replay Reader' -e bash -c 'python RealTimeParse.py --replay manager-2014-10-27--00h31m01.log --time-scale 1 --data-port 3333 ; echo DONE ;sleep 100' &"""),

    # ("replay-new-fast",
    #  """roxterm -T 'Replay Reader' -e bash -c 'python RealTimeParse.py --replay manager-2014-10-28--11h18m07.log --time-scale 0.1 --data-port 3333 ; echo DONE ;sleep 100' &"""),
    # ("replay-new",
    #  """roxterm -T 'Replay Reader' -e bash -c 'python RealTimeParse.py --replay manager-2014-10-28--11h18m07.log --time-scale 1 --data-port 3333 ; echo DONE ;sleep 100' &"""),

    # ("display-replay",
    #  """roxterm -T 'Replay Display' -e bash -c 'cd plotDemo && python DemoManager.py --data-port 3333 ; echo DONE ;sleep 10' &"""),
    # ( "", "echo ok"),
    # ("node-reset",
    #  """roxterm -T 'Replay Display' -e bash -c 'ssh iot-eur "node-cli --reset" ; echo DONE ;sleep 10' &""")

#--------------------------------------------------
    #("replay-fast",
    # """roxterm -T experiment -e bash -c 'python RealTimeParse.py --replay manager-2014-10-27--00h31m01.log --time-scale 0.1 ; echo DONE ;sleep 10' &"""),

    #("forw.ports", "./expctl ssh-forward"),
    #("tunslip6", "./expctl tunslip6"),
    #("reset BR", "./expctl reset border-router"),
    #("foren6-sniffers", "./expctl foren6-sniffers"),
    #("foren6", "./expctl foren6"),
    #("wireshark", 'sudo wireshark -k -i lo -Y "zep and icmpv6" &'),
    #("gui", "./expctl gui &"),
    #("shake", """roxterm --fork -T shake -e bash -c 'W=$(wmctrl -l | grep -i foren6 | cut "-d " -f1); echo "moving window $W (foren6) constantly" ; D=0.1 ; U=350; V=351 ; while true ; do wmctrl -i -r $W -e 0,-1,$U,-1,-1 ; wmctrl -i -r $W -e 0,-1,$V,-1,-1 ; sleep $D ; done'"""),

    #("!smartrf-sniffer", "./expctl foren6-sniffers --output wireshark+smartrf"),
    #("!wireshark-zep", 'sudo wireshark -k -i lo -Y "zep" &')
]


class Application(Frame):

    def create(self):
        self.controlFrame = Frame(self)
        self.controlFrame.pack({"side": "left"})
        self.buttonQuit = Button(self.controlFrame, text="QUIT", fg="red", 
                                 command=self.quit)
        self.buttonQuit.pack({"side": "top", "fill": "x"})
        self.buttonQuit = Button(self.controlFrame, text="restart", #fg="red", 
                                 command=self.restart)
        self.buttonQuit.pack({"side": "left", "fill": "x"})

        
        currentFrame = self
        self.buttonList = []
        for i,(name, command) in enumerate(CommandList):
            if command != None:
                def _runCommand(command=command):
                    self.runCommand(command)
                button = Button(currentFrame, text=name, command=_runCommand)
                #if i % 5 == 0:
                #    button.pack({"side":"left"})
                button.pack({"side":"top", "fill": "x"})
                self.buttonList.append(button)
            else:
                #currentFrame = Frame(self, bd=3, relief=RIDGE)
                #currentFrame.pack({"side":"top", "fill":"x"})
                #label = Label(currentFrame, text=name)
                #label.pack({"side":"top", "fill": "x"})
                currentFrame = LabelFrame(self, text = name)
                currentFrame.pack({"side":"top", "fill":"x"})

    def restart(self):
        argList = ["python", "python"] + sys.argv
        os.execlp(*argList)

    def runCommand(self, command):
        print "+", command
        os.system(command)

    def __init__(self, args, master=None):
        self.args = args
        Frame.__init__(self, master)
        self.pack()
        self.create()

root = Tk()
bgColor = "#d1e3f2"
activeBgColor = "#428bca"
root.wm_title("Exp. Tools")
root.tk_setPalette(background=bgColor, foreground='black',
                   activeBackground=activeBgColor, 
                   activeForeground=bgColor)
app = Application(args, master=root)
app.mainloop()
root.destroy()

#---------------------------------------------------------------------------

