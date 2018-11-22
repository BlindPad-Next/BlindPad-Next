#!/usr/bin/env python
#!/usr/bin/python3

"""
@class AppConnector
Class that manage the connection with the BlindPadApp
@author Alberto Inuggi, Angelo Raspagliesi, Luca Brayda
@copyright Istituto Italiano di Tecnologia (IIT) 2018
"""


import threading
import sys
import socket
import time


class AppConnector(threading.Thread):
    """
    This is a thread to be run concurrently with main process
    It repeatedly send an update message to the BP tcpServer and obtain user gestures and BP buttons' presses
    then call the callback during given instanciation .
    """

    ip_address = ''
    server_port = 0
    callback = None

    gesture_label = ''
    button_label = ''

    is_connected = False

    do_poll = True

    polling_rate = 0.15  # in seconds

    successful_response_string = 'BP_EM_16_12_OK'
    update_string = 'BP_UPDATE'
    conn_string = 'BP_STAT'
    close_string = 'BP_STOP'

    def __init__(self, address, port, clb):
        """
        @constructor
        """

        self.ip_address = address
        self.server_port = port
        self.callback = clb

        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        threading.Thread.__init__(self)
        self.start()

    def run(self):
        """
        @function run
        It connect to BPBridgeApp
        if successful, periodically (0.1 Hz) send it a BP_UPDATE message to obtain gestures and button presses
        """
        data = None
        try:
            self.client_socket.connect((self.ip_address, self.server_port))

            self.client_socket.send(bytes(self.conn_string, 'utf-8'))
            data = self.client_socket.recv(1024)

            str_data = data.decode("utf-8")

            if self.successful_response_string not in str_data:
                self.is_connected = False
            else:
                self.is_connected = True

                time.sleep(self.polling_rate)

                while self.do_poll:
                    self.gesture_label = ""
                    self.button_label = ""

                    self.client_socket.send(bytes(self.update_string, 'utf-8'))
                    data = self.client_socket.recv(1024)
                    str_data = data.decode("utf-8")
                    str_data = str_data[0:len(str_data)-1]  # remove \r

                    if "BP_GESTURE" in str_data:
                        id_eq = str_data.find('=')
                        self.gesture_label = str_data[id_eq+1:]
                        self.callback(0, self.gesture_label)
                    elif "BP_BUTTON" in str_data:
                        id_eq = str_data.find('=')
                        self.button_label = str_data[id_eq+1:]
                        self.callback(1, self.button_label)

                    time.sleep(self.polling_rate)

        except Exception as e:
            print(e)
            #client_socket.send(bytes(self.close_string, 'utf-8'))


    def stop(self):
        self.do_poll = False
