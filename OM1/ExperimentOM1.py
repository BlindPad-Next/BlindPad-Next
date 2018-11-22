"""
@class ExperimentOM1
Class that fully manage OM1 experiment
@author Alberto Inuggi, Angelo Raspagliesi, Luca Brayda
@copyright Istituto Italiano di Tecnologia (IIT) 2018
"""

import os
import sys
import json
import math

from BPexercises.Common.JsonResult import JsonResult
from BPexercises.Common.blinkThreadOM import blinkThreadOM
from BPexercises.Common import primitives as pt
from BPexercises.Common.padDrawComm import PadDrawComm
from BPexercises.Common.AppConnector import AppConnector


class ExperimentOM1:
    """
    @class Experiment
    Class that fully manage MO2
    """

    params = None
    maps = None

    # STATES
    STATE_WAITING = 0
    STATE_RUNNING = 1
    STATE_INSERTING = 2

    exp_state = None

    # input values
    user_name = None
    exp_group = None
    target_id = None

    # map info
    map_name = None
    current_map = None
    targets = None                  # array of points in ROW,COLUMN MODE : PS: mind that paddraw primitives works with col,row schema...thus invert when dealing with them
    participant_code_on = None      # string representing the pen code to represent participant position
    participant_code_off = None     # string representing the erase code to delete participant position
    n_targets = None
    border_code = None  # array of lines' codes
    blinker = None

    res_file = None
    pd_socket = None
    app_connector = None
    connectors_callback = None

    confirm_cbk = None
    cancel_cbk = None

    n_trials = None
    # current trial
    trial_id = None
    trial_results = None

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self, params, callback=None):

        self.params = params

        if callback is None:
            self.connectors_callback = self.onBPevents
        else:
            self.connectors_callback = callback

        self.init_maps()

    def init_maps(self):
        # READ MAPS
        path = os.path.join(self.params["project_path"], "input_data", "maps.json")
        with open(path) as json_file:
            self.maps = json.load(json_file)['maps']

    # ask experiment data
    def get_input(self):

        # App address
        self.params['app_address'] = None
        while self.params['app_address'] is None:
            sys.stdout.write('Specify App address: ')
            uinput = input()
            try:
                self.params['app_address'] = str(uinput)
                if self.validate_address() is False:
                    self.params['app_address'] = None
            except:
                pass

        # participant's name
        self.user_name = None
        while self.user_name is None:
            sys.stdout.write('Specify participant name: ')
            uinput = input()
            try:
                self.user_name = str(uinput)
                if len(self.user_name) == 0:
                    self.user_name = None
            except:
                pass

        # map name
        self.map_name = None
        while self.current_map is None:
            sys.stdout.write('Insert map name: ')
            mapname = input()
            try:
                self.current_map = self.get_map_by_name(mapname)
            except:
                pass

        # exp group ?
        self.exp_group = None
        while self.exp_group is None:
            sys.stdout.write('Specify group:  0:control, 1:experimental: ')
            uinput = input()
            try:
                self.exp_group = int(uinput)
                if self.exp_group != 0 and self.exp_group != 1:
                    self.exp_group = None
            except:
                pass

        # target id ?
        self.target_id = None
        while self.target_id is None:
            sys.stdout.write('Insert TARGET ID. Can only be 0,1,2: ')
            uinput = input()
            try:
                self.target_id = int(uinput)
                if self.target_id < 0 and self.target_id > 2:
                    self.target_id = None
            except:
                pass

    def validate_address(self, address):
        if len(address) == 0:
            return False

        return True

    def get_map_by_name(self, map_name):

        for m in self.maps:
            if m['name'] == map_name:
                return m
        return None

    # used only for debug, to skip exp data filling
    def debug_set_input(self, address, username, map_name, exp_group, target_id):

        if self.validate_address(address) is True:
            self.params['app_address'] = address
            self.user_name = username
            self.map_name = map_name
            self.exp_group = exp_group
            self.target_id = target_id

            self.current_map = self.get_map_by_name(map_name)
            return self.current_map
        else:
            return None

    # init AppConnector and PadDraw connection. must wait for input data filling
    def initConnectors(self):

        # PADDRAW APP
        self.pd_socket = None
        if self.params["connect_PD"] is True:
            pd_address = 'localhost'
            pd_port = 12345
            self.pd_socket = PadDrawComm(pd_address, pd_port)

        # BLINDPAD APP
        self.app_connector = None
        if self.params["connect_APP"] is True:
            self.app_connector = AppConnector(self.params["app_address"], self.params["app_port"], self.connectors_callback)

        return self.pd_socket, self.app_connector

    # START EXPERIMENT
    def start_experiment(self):

        self.initConnectors()
        self.n_trials = self.params['N_TRIALS']
        self.trial_id = 0

        # CREATE RESULT FILE
        path = os.path.join(self.params["project_path"], "result_data")
        if not os.path.exists(path):
            os.makedirs(path)
        self.res_file = JsonResult(self.user_name, path)

        self.trials_results = []
        # START !!
        self.new_trial()

    # start new Trial (first trial have trial_id=1)
    def new_trial(self):

        if self.trial_id >= self.n_trials:
            print('ESPERIMENTO FINITO !!!')
            print('mostro la sua posizione finale')
            self.trial_id = self.trial_id + 1
            self.create_map()
            self.exp_state = self.STATE_INSERTING
        else:
            self.trial_id = self.trial_id + 1
            self.create_map()

    def create_map(self):

        try:
            self.targets = [self.current_map['targets'][self.target_id]]
            self.n_targets = len(self.targets)
            self.border_code = self.current_map['code']

            # used to reset the trial when undo is pressed
            self.pd_socket.send_cmd(pt.clear())

            self.show_border('border', self.border_code)

            targets_code_on = ''
            targets_code_off = ''
            for f in range(self.n_targets):
                targets_code_on = targets_code_on + "pen(" + str(self.targets[f][1]) + ', ' + str(self.targets[f][0]) + ");"
                targets_code_off = targets_code_off + "erase(" + str(self.targets[f][1]) + ', ' + str(self.targets[f][0]) + ");"

            # start blinking targets
            self.blinker = blinkThreadOM(targets_code_on, targets_code_off, 0.75, self.pd_socket)

            # show feedback only to experimental group
            if self.exp_group == 1:
                # check whether there are previous results to display
                if self.trial_id > 1 and len(self.trials_results):
                    self.participant_code_on = ''
                    self.participant_code_off = ''
                    # create participant positions of the previous walk
                    for trg_id in range(self.n_targets):

                        row = math.floor(self.trials_results[self.trial_id - 2][0][0] / self.current_map['taxel_length']) + self.current_map['offset_row']
                        col = math.floor(self.trials_results[self.trial_id - 2][0][1] / self.current_map['taxel_length']) + self.current_map['offset_col']

                        self.participant_code_on = self.participant_code_on + pt.pen(col, row)
                        self.participant_code_off = self.participant_code_off + pt.erase(col, row)

                    self.pd_socket.send_cmd(self.participant_code_on)

                elif (self.trial_id > 1 and len(self.trials_results) == 0) or (self.trial_id == 1 and len(self.trials_results) != 0):
                    print('ERROR....should never happen')

            self.exp_state = self.STATE_RUNNING

        except Exception as e:
            print(e)

    # draw or delete a figure
    def show_border(self, tag, code, visibility=1):

        code_str = ''
        nlines = len(code)
        for l in range(nlines):
            # line(startx, starty, endx, endy, value, tag)
            code_str = code_str + "line(" + str(int(code[l][0])) + "," + str(int(code[l][1])) + "," + str(int(code[l][2])) + "," + str(int(code[l][3])) + ", " + str(visibility) + "," + "*" + tag + ");"

        print("creating figure with tag: " + tag + " and code: " + code_str)
        self.pd_socket.send_cmd(code_str)

    def insert_results(self):

        self.exp_state = self.STATE_INSERTING
        trial_result = []
        for trg in range(self.n_targets):
            trial_result.append(self.wait_for_input(trg))

        self.trials_results.append(trial_result)

        print('trial finito...')
        # write results to file as json
        results = {"trial_num": self.trial_id,  "row0": trial_result[0][0],
                                                "col0": trial_result[0][1],
                                                "time0": trial_result[0][2]}
        self.res_file.write_data_vector(results)

        self.new_trial()

    # report here App gestures & button presses + key presses.
    def onBPevents(self, eventtype, event):

        if self.exp_state is not None:
            if self.exp_state == self.STATE_RUNNING:
                if eventtype == 0:
                    # GESTURE
                    if event == 'DT':
                        self.freeze()
                elif eventtype == 1:
                    # BUTTON
                    if event == '6':
                        self.freeze()
                elif eventtype == 2:
                    # KEYS
                    if event == 'space':
                        self.freeze()

            elif self.exp_state == self.STATE_WAITING:
                if eventtype == 0:
                    # GESTURE
                    if event == 'DT':
                        self.insert_results()
                elif eventtype == 1:
                    # BUTTON
                    if event == '6':
                        self.insert_results()
                elif eventtype == 2:
                    # KEYS
                    if event == 'space':
                        self.insert_results()

            elif self.exp_state == self.STATE_INSERTING:
                return

    def validate_target(self, res):
        results = res.split(",")
        if len(results) != 3:
            return None

        if len(results[0]) > 0:
            results[0] = int(results[0])
        else:
            return None

        if len(results[1]) > 0:
            results[1] = int(results[1])
        else:
            return None

        if len(results[2]) > 0:
            pass  # time is inserted as a string
        else:
            return None
        return results

    def wait_for_input(self, id_trg):
        result = None
        while result is None:
            sys.stdout.write("Inserisci i risultati del target " + str(id_trg + 1) + " come una tripletta di numeri (partendo dall angolo in alto a sinistra : distanza alto-basso [in cm], distanza sinistra-destra[in cm], tempo [xx:yy]) ==> ")
            res = input()
            try:
                result = self.validate_target(res)
                if result is None:
                    print("ERRORE DI INSERIMENTO......RIPROVA !!")

            except Exception as e:
                print(e)
        return result

    # participant finished exploring the map, starts walking new trial. remove blinking targets, remove previous position
    def freeze(self):
        self.exp_state = self.STATE_WAITING

        # get blinking targets code
        figure_code_off = self.blinker.figure_code_off

        # stop blinking
        self.blinker.stop(True)     # stop blinking, but keep it

        # set to off the targets
        # self.pd_socket.send_cmd(figure_code_off)

        # if U want to remove the participant's previous positions....uncomment this
        # self.pd_socket.send_cmd(self.participant_code_off)
        print('PAUSED...double click on the App to enter trial results')

