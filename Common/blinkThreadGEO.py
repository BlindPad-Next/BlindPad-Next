"""
@class BlinkThreadGEO
@author Angelo Raspagliesi, Alberto Inuggi, Luca Brayda
@copyright Istituto Italiano di Tecnologia (IIT) 2018
"""

import threading
import time
from BPexercises.Common import primitives as pt



class BlinkThreadGEO(threading.Thread):
    """
    # This is a thread to be run concurrently with main process
    It blinks a figure
    """

    dict_figure = None
    let_blink = True
    figure = None
    value = True
    blinking_rate = 0.1 # seconds

    def __init__(self, figure, freq, pd_comm):
        threading.Thread.__init__(self)
        ################################
        # TO PAUSE AND RESUME THE THREAD
        self.can_run = threading.Event()
        self.thing_done = threading.Event()
        self.thing_done.set()
        self.can_run.set()
        ################################
        self.dict_figure = figure
        self.blinking_rate = freq
        self.pd_comm = pd_comm
        self.start()

    def run(self):

        try:
            while self.let_blink:
                self.can_run.wait()
                try:
                    self.value = not self.value

                    # if self.dict_figure["type"] ==  "line":
                    #     self.figure = pt.draw_line(self.dict_figure["start_col"],
                    #                                self.dict_figure["start_row"],
                    #                                self.dict_figure["end_col"],
                    #                                self.dict_figure["end_row"],
                    #                                int(self.value),
                    #                                self.dict_figure["tag"])
                    # else:
                    # it blink a point
                    if self.value:
                        self.figure = pt.pen(self.dict_figure["start_col"], self.dict_figure["start_row"])
                    else:
                        self.figure = pt.erase(self.dict_figure["start_col"], self.dict_figure["start_row"])
                    # self.figure = pt.draw_line(self.dict_figure["start_col"],
                    #                                 self.dict_figure["start_row"],
                    #                                 self.dict_figure["end_col"],
                    #                                 self.dict_figure["start_row"],
                    #                                 int(self.value),
                    #                                 self.dict_figure["tag"])
                    self.pd_comm.send_cmd(self.figure)

                    time.sleep(self.blinking_rate)
                finally:
                    self.thing_done.set()

        except Exception as e:
            print(e)
            # log.exception(str(e))

    def pause(self):
        self.can_run.clear()
        self.thing_done.wait()

    def resume(self):
        self.can_run.set()

    def change_figure_delete(self,figure):
        self.pause()
        self.value = True
        self.dict_figure = figure
        print("OK")
        self.resume()

    def change_figure(self, prev_figure, curr_figure):
        self.pause()
        if self.value:
            self.pd_comm.reset_point(prev_figure)
        else:
            self.pd_comm.send_cmd(pt.pen(prev_figure["start_col"], prev_figure["start_row"]))
        self.value = True
        # self.figure = pt.draw_line(self.dict_figure["start_col"],
        #                            self.dict_figure["start_row"],
        #                            self.dict_figure["end_col"],
        #                            self.dict_figure["start_row"],
        #                            int(self.value),
        #                            self.dict_figure["tag"])
        self.dict_figure = curr_figure
        print("OK")
        self.resume()

    def stop(self):
        self.let_blink = False