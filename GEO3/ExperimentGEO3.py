"""
@class ExperimentGEO3
Class that fully manage GEO3 experiment
@author Alberto Inuggi, Angelo Raspagliesi, Luca Brayda
@copyright Istituto Italiano di Tecnologia (IIT) 2018
"""

import os
import socket
import copy
import sys
import json
import pygame

import time
import numpy as np

from BPexercises.Common.JsonResult import JsonResult
from BPexercises.Common import primitives as pt
from BPexercises.Common.padDrawComm import PadDrawComm
from BPexercises.Common.AppConnector import AppConnector
from BPexercises.Common.keyThread import KeyThread
from BPexercises.GEO3.Figure import Figure
from BPexercises.Common.playMusic import PlayMusic


class ExperimentGEO3:
    """
    @class Experiment
    Class that fully manage GEO3
    """

    STATE_INIT = -1         # events are disabled
    STATE_START = 0         # UNUSED
    STATE_SELECTING = 1     # UNUSED
    STATE_MOVING = 2
    STATE_QUESTION = 3
    MAX_ROWS = 12
    MAX_COLS = 16

    exp_type = None             # 0 (8-14y) or 1 (15-60y)
    user_name = None
    trials_type = None          # A or B
    modality = None             # 0: blindpad or conventional
    is_familiarization = None   # 0 or 1
    user_responses = None       # 'g' or 'b' : gestures or buttons
    result_filename = None

    params = None
    figures = None
    trials = None       # chosen trials
    alltrials = None    # all available trials
    tot_trials = None

    res_file = None
    pd_socket = None
    app_connector = None
    connectors_callback = None
    key_thread = None

    num_figures = None
    selected_figure = None
    selected_figure_id = 0

    master_figure = None    # figure that will be moved toward target figure
    target_figure = None    # tract selected to be matched with master figure

    exp_state = STATE_INIT   # START/SELECTING/MOVING
    is_paused = False
    existing_figures = None
    tts_player = None
    audios = None

    confirm_cbk = None
    cancel_cbk = None

    pause_time = None
    # current trial
    trial_id = None
    current_trial = None
    trial_start_time = None
    correct_maps = None     # list of correct maps for the trial
    time_2_select = None
    time_2_match = None

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self, params, callback=None):

        self.params = params

        if callback is None:
            self.connectors_callback = self.onBPevents
        else:
            self.connectors_callback = callback

        self.init_audio()
        self.key_thread = KeyThread(self.onBPevents)

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

        # EXP TYPE : 8-14y or 15-60y
        self.exp_type = None
        while self.exp_type is None:
            sys.stdout.write('Press 0 or 1 to specify whether is for 8-14y or 15-60y: ')
            uinput = input()
            try:
                self.exp_type = int(uinput)
                if self.exp_type != 0 and self.exp_type != 1:
                    self.exp_type = None
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

        # MODALITY : blindpad or conventional
        self.modality = None
        while self.modality is None:
            sys.stdout.write('Press 0 or 1 to specify whether is a blindpad or conventional experiment: ')
            uinput = input()
            try:
                self.modality = int(uinput)
                if self.modality != 0 and self.modality != 1:
                    self.modality = None
            except:
                pass

        # trial type : A or B
        self.trials_type = None
        while self.trials_type is None:
            sys.stdout.write('Specify trials family [ A or B ]: ')
            uinput = input()
            try:
                self.trials_type = str(uinput)
                if self.trials_type != 'A' and self.trials_type != 'B':
                    self.trials_type = None
            except:
                pass

        # is familiarization ?
        self.is_familiarization = None
        while self.is_familiarization is None:
            sys.stdout.write('Is familiarization ? Press 0 if is the real experiment or 1 if is familiarization: ')
            uinput = input()
            try:
                self.is_familiarization = int(uinput)
                if self.is_familiarization != 0 and self.exp_type != 1:
                    self.is_familiarization = None
            except:
                pass

        # audio must describe gestures or buttons ?
        self.user_responses = None
        while self.user_responses is None:
            sys.stdout.write('Do you want audio describing gestures [g] or buttons [b] usage? : ')
            uinput = input()
            try:
                self.user_responses = uinput
                if self.user_responses == 'g':
                    self.user_responses = 'gest'
                elif self.user_responses == 'b':
                    self.user_responses = 'but'
                else:
                    self.user_responses = None
            except:
                pass

    # used only for debug, to skip exp data filling
    def debug_set_input(self, address, exp_type, username, modality, trials_type, is_familiarization, user_responses):

        if self.validate_address(address) is True:
            self.params['app_address'] = address
            self.exp_type = exp_type
            self.user_name = username
            self.modality = modality
            self.trials_type = trials_type
            self.is_familiarization = is_familiarization
            self.user_responses = user_responses
            return True
        else:
            return None

    def validate_address(self, address):
        if len(address) == 0:
            return False

        return True

    # init audio instance and set mp3s' full paths
    def init_audio(self):

        pygame.init()
        pygame.display.set_caption('BlindPAD')
        pygame.display.set_mode((250, 20))

        self.tts_player = PlayMusic()
        self.audios = self.params["audio_files"]
        path = os.path.join(self.params["project_path"], "audio")

        for audio in self.audios:
            self.audios[audio] = os.path.join(path, self.audios[audio])

    # init AppConnector and PadDraw connection
    def initConnectors(self):

        # PADDRAW APP
        self.pd_socket = None
        if self.params["connect_PD"] is True:
            pd_address = 'localhost'
            pd_port = 12345
            self.pd_socket = PadDrawComm(pd_address, pd_port, False)

        # BLINDPAD APP
        self.app_connector = None
        if self.params["connect_APP"] is True:
            self.app_connector = AppConnector(self.params["app_address"], self.params["app_port"], self.connectors_callback)

        return self.pd_socket, self.app_connector

    # START EXPERIMENT
    def start_experiment(self):

        self.initConnectors()

        self.trial_id = 0
        self.num_figures = len(self.params["tracts_positions"][self.exp_type])

        # READ FIGURES DICTIONARY
        path = os.path.join(self.params["project_path"], "input_data", "figures_bbrot.json")
        with open(path) as json_file:
            self.figures = json.load(json_file)['figures']

        # READ ALL AVAILABLE TRIALS
        path = os.path.join(self.params["project_path"], "input_data", "trials_" + str(self.exp_type) + ".json")  # trials_0.json or trials_1.json
        with open(path) as json_file:
            self.trials = json.load(json_file)['trials']['type' + self.trials_type]

        self.trials = np.random.permutation(self.trials)

        self.tot_trials = len(self.trials)

        # CREATE RESULT FILE
        self.result_filename = self.user_name + "_" + str(self.modality) + "_" + str(self.exp_type)

        path = os.path.join(self.params["project_path"], "result_data")
        if not os.path.exists(path):
            os.makedirs(path)
        self.res_file = JsonResult(self.result_filename, path)

        # START !!
        self.new_trial(self.trials[self.trial_id])

        # self.speech("start_" + self.user_responses)

        # if self.is_familiarization == 1:
        #     self.speech("consegna_moving_" + self.user_responses + "_" + str(self.exp_type))
        # else:
        #     self.speech("muovi")

    # start new Trial
    def new_trial(self, trial):

        self.trial_id = self.trial_id + 1
        self.current_trial = trial
        self.trial_start_time = time.time()
        self.time_2_select = 0
        self.time_2_match = 0
        self.correct_maps = trial["correct_maps"]
        self.create_starting_figures()
        print("trial: " + str(self.trial_id))

    def create_starting_figures(self):

        try:
            self.existing_figures = []

            # used to reset the trial when undo is pressed
            self.pd_socket.send_cmd(pt.clear())

            fig = self.get_figure_by_name(self.current_trial['target_figure'])
            self.target_figure = Figure('target', fig, self.params['target_positions'][0], self.params['target_positions'][1], self.pd_socket, 0)

            for f in range(self.num_figures):
                tract_pos = self.params['tracts_positions'][self.exp_type][f]

                tract_name = eval("self.current_trial['tract" + str(f) + "']")
                trial_rot = eval("self.current_trial['rot" + str(f) + "']")

                fig = self.get_figure_by_name(tract_name)
                self.existing_figures.append(Figure("tract" + str(f), fig, tract_pos[0], tract_pos[1], self.pd_socket, trial_rot))

            # patch of the new version with just one tract
            # self.selected_figure_id = -1
            self.selected_figure_id = 0
            self.master_figure = self.existing_figures[self.selected_figure_id]

            self.exp_state = self.STATE_MOVING

        except Exception as e:
            print(e)

    # report here App gestures & button presses + key presses.
    def onBPevents(self, eventtype, event):

        if self.exp_state == self.STATE_INIT:
            return

        # manage PAUSE
        # if is paused and user DID NOT press 'p'...don't do anything !!! otherwise resume
        if self.is_paused is True:
            if eventtype == 2 and event == 'p':
                self.resume()
            else:
                return
        else:
            if eventtype == 2 and event == 'p':
                self.pause()

        if self.exp_state == self.STATE_START:
            # =========== START STATE =========== (left/right)
            if eventtype == 0:
                # GESTURE
                if event == 'SL':
                    self.pre_select_figure('left')
                elif event == 'SR':
                    self.pre_select_figure('right')
            elif eventtype == 1:
                # BUTTON
                if event == '2':
                    self.pre_select_figure('left')
                elif event == '5':
                    self.pre_select_figure('right')
            elif eventtype == 2:
                # KEYS
                if event == 'left':
                    self.pre_select_figure('left')
                elif event == 'right':
                    self.pre_select_figure('right')

        elif self.exp_state == self.STATE_SELECTING:
            # =========== SELECTING STATE ===========  (left/right +  select + undo)
            if eventtype == 0:
                # GESTURES
                if event == 'SL':
                    self.pre_select_figure('left')
                elif event == 'SR':
                    self.pre_select_figure('right')
                elif event == 'ST':
                    self.select_figure()
                elif event == 'LP':
                    self.create_starting_figures()
                    self.speech('ricomincia', False)
            elif eventtype == 1:
                # BUTTONS
                if event == '2':
                    self.pre_select_figure('left')
                elif event == '5':
                    self.pre_select_figure('right')
                elif event == '6':
                    self.select_figure()
                elif event == '1':
                    self.create_starting_figures()
                    self.speech('ricomincia')
            elif eventtype == 2:
                # KEYS
                if event == 'left':
                    self.pre_select_figure('left')
                elif event == 'right':
                    self.pre_select_figure('right')
                elif event == 'space':
                    self.select_figure()
                elif event == 'esc':
                    self.create_starting_figures()
                    self.speech('ricomincia')

        elif self.exp_state == self.STATE_MOVING:
            # =========== MOVING STATE ===========  (4directions + cw rotation + confirm + undo)
            res_move = None
            if eventtype == 0:
                # GESTURES
                if event == 'SL':
                    res_move = self.master_figure.move('left', self.target_figure, 1)
                    if res_move == 1:
                        self.speech('muovi_sinistra')

                elif event == 'SR':
                    res_move = self.master_figure.move('right', self.target_figure, 1)
                    if res_move == 1:
                        self.speech('muovi_destra')

                elif event == 'SU':
                    res_move = self.master_figure.move('up', self.target_figure, 1)
                    if res_move == 1:
                        self.speech('muovi_alto')

                elif event == 'SD':
                    res_move = self.master_figure.move('down', self.target_figure, 1)
                    if res_move == 1:
                        self.speech('muovi_basso')

                elif event == 'ST':
                    res_move = self.master_figure.rotate_cw(self.target_figure)
                    if res_move == 1:
                        self.speech('ruota')

                elif event == 'DT':
                    self.ask_confirm_figure()

                elif event == 'LP':
                    self.create_starting_figures()
                    self.speech('ricomincia')
            elif eventtype == 1:
                if event == '2':
                    res_move = self.master_figure.move('left', self.target_figure, 1)
                    if res_move == 1:
                        self.speech('muovi_sinistra')

                elif event == '5':
                    res_move = self.master_figure.move('right', self.target_figure, 1)
                    if res_move == 1:
                        self.speech('muovi_destra')

                elif event == '4':
                    res_move = self.master_figure.move('up', self.target_figure, 1)
                    if res_move == 1:
                        self.speech('muovi_alto')

                elif event == '7':
                    res_move = self.master_figure.move('down', self.target_figure, 1)
                    if res_move == 1:
                        self.speech('muovi_basso')

                elif event == '6':
                    self.ask_confirm_figure()

                elif event == '3':
                    res_move = self.master_figure.rotate_cw(self.target_figure)
                    if res_move == 1:
                        self.speech('ruota')

                elif event == '1':
                    self.create_starting_figures()
                    self.speech('ricomincia')
            elif eventtype == 2:
                if event == 'left':
                    res_move = self.master_figure.move('left', self.target_figure, 1)
                    if res_move == 1:
                        self.speech('muovi_sinistra')
                elif event == 'right':
                    res_move = self.master_figure.move('right', self.target_figure, 1)
                    if res_move == 1:
                        self.speech('muovi_destra')
                elif event == 'up':
                    res_move = self.master_figure.move('up', self.target_figure, 1)
                    if res_move == 1:
                        self.speech('muovi_alto')
                elif event == 'down':
                    res_move = self.master_figure.move('down', self.target_figure, 1)
                    if res_move == 1:
                        self.speech('muovi_basso')
                elif event == 'space':
                    self.ask_confirm_figure()
                elif event == 'esc':
                    self.create_starting_figures()
                    self.speech('ricomincia')

            if res_move == 0:
                self.speech('contatto_figura')
            elif res_move == -1:
                self.speech('bordo')

        elif self.exp_state == self.STATE_QUESTION:
            # =========== QUESTION STATE ===========  (confirm + undo)
            if eventtype == 0:
                # GESTURES
                if event == 'DT':
                    self.confirm_cbk()
                elif event == 'LP':
                    self.cancel_cbk()

            elif eventtype == 1:
                if event == '6':
                    self.confirm_cbk()
                elif event == '1':
                    self.cancel_cbk()

            elif eventtype == 2:
                if event == 'y':
                    self.confirm_cbk()
                elif event == 'n':
                    self.cancel_cbk()

        # always valid
        if eventtype == 2:
            # KEYS
            if event == 'r':
                self.super_refresh()
            elif event == 'c':
                self.pre_select_figure('c')

    # user pressed the first confirm. ask him/her whether confirms or not
    def ask_confirm_figure(self):
        # if self.is_familiarization == 1:
        #     self.tts_player.playit_wait(self.audios["consegna_conferma_scelta_" + self.user_responses])
        # else:
        #     self.tts_player.playit_wait(self.audios["conferma_scelta_" + self.user_responses])

        self.exp_state = self.STATE_QUESTION
        self.confirm_cbk = self.confirm_figure
        self.cancel_cbk = self.undo_confirm_figure

    # send user to move again the figure
    def undo_confirm_figure(self):
        self.exp_state = self.STATE_MOVING
        self.speech("muovi")
        self.confirm_cbk = None
        self.cancel_cbk = None

    # user finished moving the master figure. calc results, write them, start next trials
    def confirm_figure(self):

        self.confirm_cbk = None
        self.cancel_cbk = None

        # calculate results & time 2 match
        res = self.check_result()
        self.time_2_match = time.time() - self.trial_start_time
        print("result is " + str(res))

        # write results to file as json
        results = {"trial_num": self.trial_id, "iscorrect": res, "time_2_match": self.time_2_match, "trial": self.current_trial,
                   "target_map": self.target_figure.map.tolist(), "master_map": self.master_figure.map.tolist()}
        self.res_file.write_data_vector(results)

        if self.trial_id < self.tot_trials:

            if self.is_familiarization is True:
                self.tts_player.playit_wait(self.audios["fine_trial"])
            else:
                self.tts_player.playit_wait(self.audios["fine_trial"])

            # start new trial
            self.new_trial(self.trials[self.trial_id])
            self.speech("muovi")

        else:
            self.end_experiment()

    # clean up
    def end_experiment(self):
        self.speech("esperimento_finito")
        self.pd_socket.send_cmd(pt.clear())

    # calculate the sum map between master and target and compares it to each correct map
    # return True if at least one coincides.
    # return False is they all are different in at least one taxel
    def check_result(self):
        current_map = self.add_maps(self.master_figure.map, self.target_figure.map)
        for m in self.correct_maps:
            if self.are_maps_identical(current_map, m) is True:
                return True
        return False

    # return the figure associated to the given fig_name
    def get_figure_by_name(self, fig_name):
        for figure in self.figures:
            if figure['name'] == fig_name:
                return copy.deepcopy(figure)
        return None

    # determine whether two maps are identical
    def are_maps_identical(self, map1, map2):
        for r in range(self.params['MAX_ROWS']):
            for c in range(self.params['MAX_COLS']):
                if map1[r][c] != map2[r][c]:
                    return False
        return True

    # add two maps
    # since two maps cannot be overlapped. the sum can be 0 or 1
    def add_maps(self, map1, map2):
        new_map = np.zeros((self.params['MAX_ROWS'], self.params['MAX_COLS']))
        for r in range(self.params['MAX_ROWS']):
            for c in range(self.params['MAX_COLS']):
                new_map[r][c] = map1[r][c] + map2[r][c]
        return new_map

    # get all the figures' code
    def get_scenario_code(self):
        total_code = self.target_figure.current_code_str

        for f in self.existing_figures:
            total_code = total_code + f.current_code_str
        print(total_code)
        return total_code

    # recreates all the scenario. used after a disconnection. last 10 seconds. put exp in pause, then resume
    def super_refresh(self):

        self.pause()
        self.pd_socket.refresh(self.get_scenario_code(), True)
        self.resume()

    def pause(self):
        self.is_paused = not self.is_paused
        self.pause_time = time.time()

    def resume(self):
        self.is_paused = not self.is_paused
        time_in_pause = time.time() - self.pause_time
        self.trial_start_time = self.trial_start_time + time_in_pause

    # disable gesture/buttons while speaking. speak only in BP usage
    def speech(self, audio_string, wait=True):

        if self.modality == 0:
            current_state = self.exp_state
            self.exp_state = self.STATE_INIT
            if wait is True:
                self.tts_player.playit_wait(self.audios[audio_string])
            else:
                self.tts_player.playit(self.audios[audio_string])

            self.exp_state = current_state

    # =====================================================================================
    # UNUSED
    # =====================================================================================

    # select tract to move by setting : self.selected_figure_id & exp_state = SELECTING STATE
    # 8-14:  right selection define figure_1, left: figure_0
    # 15-60: right increment id, left decrement id
    def pre_select_figure(self, direction):

        print('pre_select_figure : function DISABLED ...should never be called...check who does it !!!')
        return

        self.exp_state = self.STATE_SELECTING

        if self.exp_type == 0:  # 8-14
            if direction == 'right':
                self.selected_figure_id = 1
            else:
                self.selected_figure_id = 0
        else:
            if direction == 'right':
                self.selected_figure_id = self.selected_figure_id + 1
                if self.selected_figure_id > self.num_figures-1:
                    self.selected_figure_id = 0
            elif direction == 'left':
                self.selected_figure_id = self.selected_figure_id - 1
                if self.selected_figure_id < 0:
                    self.selected_figure_id = self.num_figures-1

        self.speech("figura" + str(self.selected_figure_id))

        self.pd_socket.send_cmd(pt.clear())
        self.target_figure.show_figure(self.target_figure.tag, self.target_figure.current_code, 1)

        self.master_figure = self.existing_figures[self.selected_figure_id]
        self.master_figure.show_figure(self.master_figure.tag, self.master_figure.current_code, 1)

    # select a figure. start MOVING STATE
    def select_figure(self):

        print('select_figure : function DISABLED...should never be called...check who does it !!!')
        return

        self.tts_player.playit_wait(self.audios["scelta_" + str(self.selected_figure_id)])
        if self.is_familiarization == 1:
            self.tts_player.playit_wait(self.audios["consegna_moving_" + str(self.exp_type)])
        else:
            self.tts_player.playit_wait(self.audios["muovi"])

        self.exp_state = self.STATE_MOVING
        self.time_2_select = time.time() - self.trial_start_time


