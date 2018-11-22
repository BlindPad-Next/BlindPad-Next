import socket
import sys, os
import json
import time
import pygame
from BPexercises.Common import keyThread
from BPexercises.Common import primitives as pt
from BPexercises.Common.padDrawComm import PadDrawComm


# Function to do when a key is press
def event_todo(event):
    msg = ''

    # for event in pygame.event.get():
    #     if (event.type == pygame.KEYDOWN):
    # move right
    if event.key == pygame.K_RIGHT:
        msg = pt.move(1, 0)  # "move(1, 0);"
        print("R")
    # move left
    elif event.key == pygame.K_LEFT:
        msg = pt.move(-1, 0)  # "move(-1, 0);"
        print("L")
    # move down
    elif event.key == pygame.K_DOWN:
        msg = pt.move(0, 1)  # "move(0, 1);"
        print("D")
    # move up
    elif event.key == pygame.K_UP:
        msg = pt.move(0, -1)  # "move(0, -1);"
        print("U")
    if msg is not '':
        client_socket.send(bytes(msg, 'utf-8'))
        # time.sleep(0.1)




# CHOOSE LEVEL

LV = 4
file = "newLV" + str(LV) + ".txt"


with open(file) as json_file:
    tact_imgs = json.load(json_file)
#

with open("params.json") as json_file:
            params = json.load(json_file)

client_socket = PadDrawComm(params)
client_socket.connect(('localhost', 12345))

# # thread = keyThread.KeyThread()
#
fig1 = pt.draw_rect(1,1,3,3,1,'foo')
fig2 = pt.draw_circle(7,7,2,1,'bar')
# fig3 = pt.draw_horz_line(10,2,3,1,'gin')
# client_socket.refresh(tact_imgs['e5'])
# time.sleep(2)
# client_socket.refresh(tact_imgs['u5'])
# msg = pt.move(0, 2)
client_socket.refresh(fig2)
time.sleep(1)
client_socket.send_cmd(fig1)
time.sleep(1)
client_socket.send_cmd("invert(*foo);")
client_socket.send_cmd("invert();")
# client_socket.send_cmd(pt.move(0,2,'bar'))
# time.sleep(1)
# client_socket.send_cmd(pt.invert('gin'))
# time.sleep(3)
# client_socket.send_cmd(pt.move(3,0,'gin'))


