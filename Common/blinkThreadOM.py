"""
@class BlinkThreadOM
@author Alberto Inuggi, Angelo Raspagliesi, Luca Brayda
@copyright Istituto Italiano di Tecnologia (IIT) 2018
"""

import threading
import time
from BPexercises.Common import primitives as pt


class blinkThreadOM(threading.Thread):
    """
    # This is a thread to be run concurrently with main process
    It blinks a figure

    """

    dict_figure = None
    let_blink = True
    figure = None
    value = False
    blinking_rate = 0.1  # seconds

    figure_code_on = None
    figure_code_off = None

    final_state = False # determined whether the figure must ON or OFF when it stops blinking


    def __init__(self, code_on, code_off, freq, pd_comm):
        threading.Thread.__init__(self)

        ################################
        # TO PAUSE AND RESUME THE THREAD
        self.can_run = threading.Event()
        self.thing_done = threading.Event()
        self.thing_done.set()
        self.can_run.set()
        ################################
        self.figure_code_on = code_on
        self.figure_code_off = code_off
        self.blinking_rate = freq
        self.pd_comm = pd_comm
        self.start()

    def run(self):

        self.value = False
        self.let_blink = True
        try:
            while self.let_blink:
                self.can_run.wait()
                try:
                    self.value = not self.value
                    if self.value is True:
                        self.pd_comm.send_cmd(self.figure_code_on)
                    else:
                        self.pd_comm.send_cmd(self.figure_code_off)

                    time.sleep(self.blinking_rate)
                finally:
                    self.thing_done.set()

            if self.final_state is True:
                self.pd_comm.send_cmd(self.figure_code_on)
            else:
                self.pd_comm.send_cmd(self.figure_code_off)

        except Exception as e:
            print(e)
            # log.exception(str(e))

    def pause(self):
        self.can_run.clear()
        self.thing_done.wait()

    def resume(self):
        self.can_run.set()

    def change_figure(self, figure):
        self.pause()
        self.dict_figure = figure
        self.value = True
        print("OK")
        self.resume()

    def stop(self, final_state=False):
        self.let_blink = False
        self.final_state = final_state
