#! /usr/bin/python
#---------------------------------------------------------------------------

import Tkinter, os
from Tkinter import *

import optparse


parser = optparse.OptionParser()
parser.add_option("--mote-id", dest="moteId", action="store", default=0,
     type="int")
(options, argList) = parser.parse_args()

CommandList = [
    ("ping-rpi",
      """roxterm -T PingRPi -e bash -c 'ping rpi ; echo DONE ;sleep 10'"""),
    ("ssh-rpi", """./watrli-tool ssh-rpi"""),
    ("sniffer", 
     """roxterm -T sniffer -e bash -c './watrli-tool sniffer ; echo DONE ;sleep 10'&"""),
    ("wireshark", 'sudo wireshark -k -i lo -Y "zep" &'),

    ( "", "echo ok"),

    ( "rpi-setup", "./watrli-tool rpi-setup"),
    ( "rpi-dashboard", "./watrli-tool rpi-dashboard"),
    ( "rpi-proxy", "./watrli-tool rpi-proxy"),
    ( "rpi-rpld", "./watrli-tool rpi-rpld"),

    ( "", "echo ok"),

    ( "stop-r21", "./watrli-tool dbg-server"),
    ( "flash-r21", "./watrli-tool flash"),
    ( "reset-r21", "./watrli-tool reset"),
    ( "term-r21", "./watrli-tool term"),

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
    ("!wireshark-zep", 'sudo wireshark -k -i lo -Y "zep" &')
]

if "only-control" in argList:
    CommandList += ExtraCommandList

class Application(Frame):

    def create(self):
        self.buttonQuit = Button(self, text="QUIT", fg="red", command=self.quit)
        self.buttonQuit.pack({"side": "left"})
        
        self.buttonList = []
        for i,(name, command) in enumerate(CommandList):
            def _runCommand(command=command):
                self.runCommand(command)
            button = Button(self, text=name, command=_runCommand)
            #if i % 5 == 0:
            #    button.pack({"side":"left"})
            button.pack({"side":"top"})
            self.buttonList.append(button)

    def runCommand(self, command):
        command = command.replace("./hctl", "./hctl --mote-id %s" 
                                  % options.moteId)
        print "+", command
        os.system(command)

    def __init__(self, options, master=None):
        self.options = options
        Frame.__init__(self, master)
        self.pack()
        self.create()

root = Tk()
app = Application(options, master=root)
app.mainloop()
root.destroy()

#---------------------------------------------------------------------------

