#! /usr/bin/python3

"""
@class padDrawComm
Class that manage the connection with PadDraw
@author Angelo Raspagliesi, Alberto Inuggi, Luca Brayda
@copyright Istituto Italiano di Tecnologia (IIT) 2018
"""



import socket
import time
from .primitives import *


class PadDrawComm(socket.socket):

    address = None
    port = None

    def __init__(self, address, port, do_super_clear=True):

        self.address = address
        self.port = port

        super().__init__(socket.AF_INET, socket.SOCK_STREAM)

        self.connect((address, port))
        if do_super_clear is True:
            self.super_clear()
        else:
            self.send_cmd(clear())

    def send_cmd(self, msg):
        try:
            self.send(bytes(msg, 'utf-8'))
        except Exception as e:
            print(e)

    def refresh(self, msg, force=False):
        if force:
            self.super_clear()
        else:
            self.send_cmd(clear())
        self.send_cmd(msg)

    def super_clear(self):
        # for i in range(16):
        #     self.send_cmd(draw_vert_line(i, 0, 15, 1))
        for i in range(12):
            self.send_cmd(draw_horz_line(0, i, 15, 1))
        time.sleep(5)
        self.send_cmd(clear())
        time.sleep(5)

    def reset_vert_line(self, figure):
       self.send_cmd(erase_vert_line(figure))
       self.send_cmd(draw_vert_line(figure["start_col"],
                                    figure["start_row"],
                                    figure["end_row"],
                                    figure["value"],
                                    figure["tag"]))

    def reset_point(self, figure):
        # self.send_cmd(erase_point(figure))
        self.send_cmd(erase(figure["start_col"],
                            figure["start_row"]))
                            # figure["tag"]))
        self.send_cmd(draw_vert_line(figure["start_col"],
                                     figure["start_row"],
                                     figure["start_row"],
                                     figure["value"]))#,
                                     # figure["tag"]))