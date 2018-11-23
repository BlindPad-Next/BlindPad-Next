#! /usr/bin/python3

"""
@class KeyThread
@author Alberto Inuggi, Angelo Raspagliesi, Luca Brayda
@copyright Istituto Italiano di Tecnologia (IIT) 2018
"""


import threading
import keyboard
import time


class KeyThread(threading.Thread):

    """
    # This is a thread to be run concurrently with main process
    It waits for a key pressed and it sets the
    class variables according to received message.
    """

    callback = None
    do_poll = True
    polling_rate = 0.10  # in seconds
    MSG_TYPE = 2

    def __init__(self, clb):

        threading.Thread.__init__(self)
        self.callback = clb
        self.start()

    def run(self):

        try:
            while self.do_poll:
                msg = ""
                if keyboard.is_pressed('right'):
                    msg = "right"
                elif keyboard.is_pressed('left'):
                    msg = "left"
                elif keyboard.is_pressed('down'):
                    msg = "down"
                elif keyboard.is_pressed('up'):
                    msg = "up"
                elif keyboard.is_pressed('enter'):
                    msg = 'enter'
                elif keyboard.is_pressed('space'):
                    msg = 'space'
                elif keyboard.is_pressed('r'):
                    msg = 'r'
                elif keyboard.is_pressed('c'):
                    msg = 'c'
                elif keyboard.is_pressed('p'):
                    msg = 'p'

                if msg is not "":
                    self.callback(self.MSG_TYPE, msg)

                time.sleep(self.polling_rate)

        except Exception as e:
            print(e)
            # log.exception(str(e))

    def stop(self):
        self.do_poll = False
