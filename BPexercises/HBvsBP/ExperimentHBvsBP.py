"""
@class ExperimentHBvsBP
Class that fully manage HBvsBP experiment
@author Angelo Raspagliesi, Alberto Inuggi, Luca Brayda
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
from BPexercises.Tactris.Figure_tactris import Figure_Tactris
from BPexercises.GEO3.ExperimentGEO3 import ExperimentGEO3
from BPexercises.Common.playMusic import PlayMusic
from BPexercises.Common.playSound import PlaySound
from BPexercises.Braille.BrailleChar import BrailleChar
from BPexercises.HBvsBP.Figure_HB_BP import Figure_HB_BP


class ExperimentHBvsBP(ExperimentGEO3):
    """
    @class Experiment
    Class that fully manage HBvsBP
    """

    STATE_INIT = -1
    STATE_QUEST = 0
    STATE_ANSWER = 1

    exp_type = None             # 0 (8-14y) or 1 (15-60y)
    user_name = None
    trials_type = None          # A or B
    modality = None             # 0: blindpad or hyperbraille
    is_familiarization = None   # 0 or 1
    user_responses = None       # 'g' or 'b' : gestures or buttons
    result_filename = None

    cell_size = None
    figures_file = None
    trials_file = None
    target_pos = None
    tract_figures = None
    tracts_pos = None

    current_cell = None
    start_from = None
    user_answer = None
    match = None

    avg_time = None
    perc_score = None

    def __init__(self, params, callback=None):

        ExperimentGEO3.__init__(self, params, callback)

        # ask experiment data
    def get_input(self):

        # blindpad or hyperbraille
        self.modality = None
        while self.modality is None:
            sys.stdout.write('Press 0 or 1 to specify whether is a blindpad or hyperbraille experiment: ')
            uinput = input()
            try:
                self.modality = int(uinput)
                if self.modality != 0:
                    if self.modality != 1:
                        self.modality = None
            except:
                pass

        # is familiarization ?
        self.is_familiarization = None
        while self.is_familiarization is None:
            sys.stdout.write('Is familiarization ? Press 0 if is the real experiment or 1 if is familiarization: ')
            uinput = input()
            try:
                self.is_familiarization = int(uinput)
                if self.is_familiarization != 0:
                    if self.is_familiarization != 1:
                        self.is_familiarization = None
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

        if not self.is_familiarization:
            self.start_from = None
            while self.start_from is None:
                sys.stdout.write("Insert from which trial to begin [1-16]: ")
                uinput = input()
                try:
                    self.start_from = int(uinput)
                    if self.start_from < 1 or self.start_from > 16:
                        self.start_from = None
                except:
                    pass
        else:
            self.start_from = 1

    def debug_set_input(self, username, modality, is_familiarization, start_from):
        # self.user_mode = mode
        # self.ip_address = ip_address
        self.user_name = username
        self.modality = modality

        self.is_familiarization = is_familiarization
        if not self.is_familiarization:
            self.start_from = start_from
        else:
            self.start_from = 1


    def load_files(self):
        if self.modality:
            self.target_pos = self.params["target_positions_HB"]
            self.tracts_pos = self.params["tracts_positions_HB"]
            self.figures_file = "figures_hyperbraille.json"
            if self.is_familiarization:
                self.trials_file = "trials_HB_fam.json"
            else:
                self.trials_file = "trials_HB.json"

            self.MAX_ROWS = 30
            self.MAX_COLS = 32
        else:
            self.target_pos = self.params["target_positions_BP"]
            self.tracts_pos = self.params["tracts_positions_BP"]
            self.figures_file = "figures_blindpad.json"
            if self.is_familiarization:
                self.trials_file = "trials_BP_fam.json"
            else:
                self.trials_file = "trials_BP.json"

            self.MAX_ROWS = 12
            self.MAX_COLS = 16

        self.num_figures = len(self.tracts_pos)

    # START EXPERIMENT
    def start_experiment(self):
        self.initConnectors()
        self.start_from -= 1
        self.trial_id = copy.deepcopy(self.start_from)

        self.load_files()

        # READ FIGURES DICTIONARY
        path = os.path.join(self.params["project_path"], "input_data", self.figures_file)
        with open(path) as json_file:
            file = json.load(json_file)
            self.cell_size = file['cell_size']
            self.figures = file['figures']

        # READ ALL AVAILABLE TRIALS
        path = os.path.join(self.params["project_path"], "input_data", self.trials_file)
        with open(path) as json_file:
            self.trials = json.load(json_file)['trials']

        # self.trials = np.random.permutation(self.trials)

        self.tot_trials = len(self.trials)

        # CREATE RESULT FILE
        if not self.is_familiarization:
            if self.modality:
                self.result_filename = self.user_name + "_HB"
            else:
                self.result_filename = self.user_name + "_BP"

            path = os.path.join(self.params["project_path"], "result_data")
            if not os.path.exists(path):
                os.makedirs(path)
            self.res_file = JsonResult(self.result_filename, path)


        # START !!
        self.speech("start")
        self.new_trial(self.trials[self.trial_id])


    # start new Trial
    def new_trial(self, trial):
        self.pd_socket.send_cmd(pt.clear())
        self.user_answer = None
        self.match = None
        self.current_trial = trial
        self.trial_start_time = time.time()
        self.time_2_match = 0
        self.current_cell = 0
        self.create_figures()
        print("trial: " + str(self.trial_id + 1))
        self.trial_id = self.trial_id + 1
        self.exp_state = self.STATE_QUEST


    def create_figures(self):

        try:

            self.existing_figures = []

            target_name = self.current_trial["target_figure"]
            self.target_figure = self.get_figure_by_name(target_name)
            self.existing_figures.append(Figure_HB_BP("target", self.target_figure, self.target_pos[1], self.target_pos[0], self.pd_socket, self.cell_size, self.MAX_ROWS, self.MAX_COLS))

            self.tract_figures = self.current_trial["tracts"]
            for tract in range(self.num_figures):
                tract_pos = self.tracts_pos[self.current_cell]
                tract_name = self.tract_figures[self.current_cell]

                fig = self.get_figure_by_name(tract_name)
                self.existing_figures.append(Figure_HB_BP("tract" + str(tract), fig, tract_pos[1], tract_pos[0],self.pd_socket,self.cell_size,self.MAX_ROWS,self.MAX_COLS))
                self.current_cell +=1

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

        if self.exp_state == self.STATE_QUEST:
            if event == 'space':
                self.confirm_figure()
        elif self.exp_state == self.STATE_ANSWER:
            pass

    def confirm_figure(self):
        self.exp_state = self.STATE_ANSWER
        self.time_2_match = round(time.time() - self.trial_start_time, 2)
        if not self.is_familiarization:
            print("Time to match: " + str(self.time_2_match))
            while self.user_answer is None:
                print("Insert user answer, figures are numerated from 1 to 6")
                print("1    2    3")
                print("\n")
                print("4    5    6")
                uinput = input("ANSWER: ")
                try:
                    if len(uinput) == 0:
                        pass
                    else:
                        self.user_answer = int(uinput)
                        if self.user_answer < 1 or self.user_answer > 6:
                            self.user_answer = None
                except Exception as e:
                    print(e)
                    pass

            self.record_answer()

        if self.trial_id < self.tot_trials:
            self.pd_socket.send_cmd(pt.clear())
            self.speech("fine_trial")
            # start new trial
            self.speech("start")
            self.new_trial(self.trials[self.trial_id])


        else:
            self.end_experiment()

    def record_answer(self):

        self.user_answer -= 1
        self.user_answer = self.current_trial["tracts"][self.user_answer]

        self.check_result()
        # write results to file as json
        results = {"trial_num": self.trial_id, "time_2_match": self.time_2_match,
                   "target_figure": self.target_figure["name"], "answer": self.user_answer, "match": self.match}
        self.res_file.write_data_vector(results)

    def check_result(self):
        if self.user_answer == self.target_figure["name"]:
            self.match = 1
        else:
            self.match = 0

    def end_experiment(self):
        self.speech("esperimento_finito")
        self.pd_socket.send_cmd(pt.clear())

        if not self.is_familiarization:
            file = open(self.res_file.filename, mode="r")
            results = json.load(file)['results']

            self.calculate_performance(results)

            tot_results = {"SCORE: ": self.perc_score, "AVG_TIME: ": self.avg_time}

            self.res_file.write_data_vector(tot_results)


    def calculate_performance(self, results):

        total_score = 0
        total_time = 0

        for i in range(len(results)):
            total_score += results[i]["match"]
            total_time += results[i]["time_2_match"]

        self.avg_time = round((total_time / self.tot_trials), 2)
        self.perc_score = str(round(total_score * 100 / self.tot_trials)) + " %"

    def speech(self, audio_string, wait=True):

        current_state = self.exp_state
        self.exp_state = self.STATE_INIT
        if wait is True:
            self.tts_player.playit_wait(self.audios[audio_string])
        else:
            self.tts_player.playit(self.audios[audio_string])

        self.exp_state = current_state
