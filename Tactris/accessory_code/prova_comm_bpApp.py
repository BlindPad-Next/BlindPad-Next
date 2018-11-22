import sys
import socket
import time
sys.path.append("/data/CODE/blindpad-next/BPexercises")

from BPexercises.Common.AppConnector import AppConnector
from BPexercises.Common import primitives as pt
from BPexercises.Common.keyThread import KeyThread

import pyttsx3


def onBPevents(type, event):

    msg = ''
    if type == 0:
        if event == 'SL':
            msg = pt.move(-1, 0)
        elif event == 'SR':
            msg = pt.move(1, 0)
        elif event == 'SU':
            msg = pt.move(0, -1)
        elif event == 'SD':
            msg = pt.move(0, 1)
        elif event == 'ST':
            msg = pt.move(0, 1)
        elif event == 'DT':
            msg = "rotate(90, *fig);"
        elif event == 'LP':
            msg = pt.move(0, 1)
    elif type == 1:
        if event == '1':
            msg = pt.move(1, 0)
        elif event == '2':
            msg = pt.move(0, -1)
        elif event == '3':
            msg = pt.move(0, 1)
        elif event == '4':
            pass
        elif event == '5':
            msg = pt.move(-1, 0)
        elif event == '6':
            pass
        elif event == '7':
            pass
    elif type == 2:
        if event == 'L':
            msg = pt.move(-1, 0)
        elif event == 'R':
            msg = pt.move(1, 0)
        elif event == 'U':
            msg = pt.move(0, -1)
        elif event == 'D':
            msg = pt.move(0, 1)

    if pd_socket is not None and msg is not '':
        pd_socket.send(bytes(msg, 'utf-8'))
    time.sleep(0.1)
    print(event)


if __name__ == "__main__":

    delay = 0.75
    connect_APP = True
    connect_PD = True

    # BLINDPAD APP
    bp_c = None
    if connect_APP is True:
        # bp_address = '10.245.71.73'
        bp_address = '192.168.43.251'
        bp_port = 4001
        bp_c = AppConnector(bp_address, bp_port, onBPevents)

    # PADDRAW APP
    pd_socket = None
    if connect_PD is True:
        pd_address = '10.245.72.26'
        pd_address = 'localhost'
        pd_port = 12345
        pd_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        pd_socket.connect((pd_address, pd_port))
        pd_socket.send(bytes('clear();', 'utf-8'))

        # draw figure
        msg = pt.draw_horz_line(3, 4, 7, 1, "fig")
        pd_socket.send(bytes(msg, 'utf-8'))
        time.sleep(1)

    engine = pyttsx3.init()
    engine.say('voglio andare a casa')
    engine.runAndWait()

        # kt = KeyThread(onBPevents)
    # pd_socket.send(bytes(pt.move(1, 0), 'utf-8'))
    # time.sleep(delay)
    #
    # pd_socket.send(bytes(pt.move(1, 0), 'utf-8'))
    # time.sleep(delay)
    #
    # pd_socket.send(bytes(pt.move(0, 1), 'utf-8'))
    # time.sleep(delay)
    #
    # pd_socket.send(bytes(pt.move(0, 1), 'utf-8'))
    # time.sleep(delay)
    #
    # pd_socket.send(bytes(pt.move(-1, 0), 'utf-8'))
    # time.sleep(delay)
    #
    # pd_socket.send(bytes(pt.move(-1, 0), 'utf-8'))
    # time.sleep(delay)
    #
    # pd_socket.send(bytes(pt.move(0, -1), 'utf-8'))
    # time.sleep(delay)
    #
    # pd_socket.send(bytes(pt.move(0, -1), 'utf-8'))
    # time.sleep(delay)

print('finished')