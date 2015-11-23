#! /usr/bin/python

# (*) Import plotly package
import plotly, json, math, time, socket

# Check plolty version (if not latest, please upgrade)
plotly.__version__

# (*) To communicate with Plotly's server, sign in with credentials file
import plotly.plotly as py

# (*) Useful Python/Plotly tools
import plotly.tools as tls

# (*) Graph objects to piece together plots
from plotly.graph_objs import *

import numpy as np  # (*) numpy for math functions and arrays



with open('./config.json') as config_file:
    plotly_user_config = json.load(config_file)

py.sign_in(plotly_user_config["plotly_username"], plotly_user_config["plotly_api_key"])


stream_ids = tls.get_credentials_file()['stream_ids']


#print tls.get_credentials_file()
# Init. 1st scatter obj (the pendulums) with stream_ids[1]
trace1 = Scatter(
    x=[],  # init. data lists
    y=[],
    mode='lines+markers',    # markers at pendulum's nodes, lines in-bt.
    line=Line(),  # reduce opacity
    marker=Marker(size=12),  # increase marker size
    stream=Stream(token=stream_ids[0])  # (!) link stream id to token
)


# Make data object made up of the 2 scatter objs
data = Data([trace1])

# Define dictionary of axis style options
axis_style = dict(
    showgrid=False,    # remove grid
    showline=False,    # remove axes lines
    zeroline=False     # remove x=0 and y=0 lines
)

# Make layout with title and set axis ranges
L = 1700
layout = Layout(
    title='Demo Display',  # set plot's title
    xaxis=XAxis(
        axis_style,     # add style options
        range=[-L,L]    # set x-axis range
    ),
    yaxis=YAxis(
        axis_style,     # add style options
        range=[-L,L]  # set y-axis range
    ),
    showlegend=False    # remove legend
)

# Make figure object
fig = Figure(data=data, layout=layout)

# (@) Send fig to Plotly, initialize streaming plot, open tab
unique_url = py.plot(fig, filename='demo')

# (@) Make 1st instance of the stream link object, 
#     with same stream id as the 1st stream id object (in trace1)
s1 = py.Stream(stream_ids[0])

s1.open()

sd= socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sd.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sd.bind(('', 7777))

while True:
    data, address = sd.recvfrom(1024)
    try:
        data = [int(x) for x in data.split(",")]
        x,y,z = data[0:3]
    except:
        print "cannot parse:", data
    print data
    x-=500
    z+=500
    s1.write(dict(x=[0, x], y=[0, -z]))


a = 0.5
L1 = 1
for i in range(9999999):
#    print sd.recvfrom(1024)
    a = i /float (10)
    x1 = L1*math.sin(a)        # convert angles to x-y coordinates
    y1 = -L1*math.cos(a)
    s1.write(dict(x=[0, x1], y=[0, y1]))
    time.sleep(0.1)
