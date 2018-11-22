import json
import time
import copy
import os
import numpy as np

from BPexercises.Common.AppConnector import AppConnector
from BPexercises.Common.padDrawComm import PadDrawComm
from BPexercises.Common import primitives as pt


def show_random_matrix(waitf=2):

    pd_socket.send_cmd(pt.clear())
    time.sleep(waitf/3)

    matrix = np.zeros((12, 16))
    values = np.random.random((5, 5))

    for i in range(5):
        for j in range(5):
            if values[i][j] > 0.5:
                matrix[i][j] = 1
            else:
                matrix[i][j] = 0

    pd_socket.send_cmd(pt.convert_map_to_pens(matrix))
    time.sleep(waitf)



def on_bpapp(type, code):

    print("BP event: type = " + str(type) + ", code: " + str(code))



if __name__ == "__main__":

    app_address = "10.245.71.47"
    app_port = 4001

    pd_address = 'localhost'
    pd_port = 12345

    waitfor = 5.0
    number_of_loops = 0 # 100000000
    loops = 0
    connect_APP = True
    connect_PD = False

    # BLINDPAD APP
    bp_c = None
    if connect_APP is True:
        bp_c = AppConnector(app_address, app_port, on_bpapp)

    # PADDRAW APP
    pd_socket = None
    if connect_PD is True:
        pd_address = 'localhost'
        pd_socket = PadDrawComm(pd_address, pd_port)

    while loops < number_of_loops:
        show_random_matrix(waitfor)
        loops = loops + 1
