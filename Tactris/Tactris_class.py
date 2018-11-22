"""
@class Tactris
Class that fully manage Tactris game
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



class Tactris(ExperimentGEO3):
    """
    @class Tactris
    Class that fully manage the tactris game
    """


    figures_type = None          # A or B
    music = None
    audio_channels = None
    language = None

    allfigures = None    # all available figures
    tot_figures = None


    total_figure = None    # tract selected to be matched with master figure
    game_area = None
    score_area = None
    delimiter = None
    level_fig = None
    score_fig = None

    next_figure = None
    next_figure_fig = None
    next_figure_code = None
    total_figure_code = None
    game_area_code = None
    code_delimiter = None
    code_level = None
    code_score = None

    COLS_GAME_AREA = 10
    COLS_SCORE_AREA = 4 # +1 of delimiter

    # current figure
    figure_id = None
    current_figure = None
    figure_start_time = None
    deleted = False

    start_time = None
    max_time = None
    level = None
    score = None
    cell_size_char = None
    cell_size_fig = None
    characters = None


    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self, params, callback=None, language = "it"):

        self.params = params

        if callback is None:
            self.connectors_callback = self.onBPevents
        else:
            self.connectors_callback = callback

        self.language = language
        self.init_audio()
        self.key_thread = KeyThread(self.onBPevents)

        # used only for debug, to skip exp data filling

    def debug_set_input(self, address, level, username, modality, user_responses):

        if self.validate_address(address) is True:
            self.params['app_address'] = address
            self.level = level - 1
            self.user_name = username
            self.modality = modality
            self.user_responses = user_responses
            self.max_time = self.params["levels_of_difficulty"][self.level]
            return True
        else:
            return None

    # init audio instance and set mp3s' full paths
    def init_audio(self):

        pygame.init()
        pygame.display.set_caption('BlindPAD')
        pygame.display.set_mode((250, 20))

        self.music = PlayMusic()
        self.tts_player = PlaySound()
        pygame.mixer.music.set_volume(0.5)
        if self.language is "it":
            self.audios = self.params["audio_files"]
        elif self.language is "en":
            self.audios = self.params["audio_files_en"]
        self.audio_channels = self.params["audio_channels"]
        path = os.path.join(self.params["project_path"], "audio")

        for audio in self.audios:
            self.audios[audio] = os.path.join(path, self.audios[audio])


    # START EXPERIMENT
    def start_experiment(self):

        self.initConnectors()

        self.figure_id = 0
        self.score = 0



        # READ FIGURES DICTIONARY
        path = os.path.join(self.params["project_path"], "input_data", "figures_tetris.json")
        with open(path) as json_file:
            file = json.load(json_file)
            self.cell_size_fig = file['cell_size']
            self.figures = file['figures']

        path = os.path.join(self.params["project_path"], "input_data", "braille_char_8dots.json")
        with open(path) as json_file:
            file = json.load(json_file)
            self.cell_size_char = file['cell_size']
            self.characters = file['characters']


        self.title_screen()



    def start_demo(self):

        self.initConnectors()

        self.figure_id = 0
        self.score = 0

        # READ FIGURES DICTIONARY
        path = os.path.join(self.params["project_path"], "input_data", "figures_tetris.json")
        with open(path) as json_file:
            file = json.load(json_file)
            self.cell_size_fig = file['cell_size']
            self.figures = file['figures']

        path = os.path.join(self.params["project_path"], "input_data", "braille_char_8dots.json")
        with open(path) as json_file:
            file = json.load(json_file)
            self.cell_size_char = file['cell_size']
            self.characters = file['characters']

        self.exp_state = self.STATE_START

        print("Fai doppio tap o premi spazio per iniziare")


    def title_screen(self):

        self.exp_state = self.STATE_START

        print("Fai doppio tap o premi spazio per iniziare")

        # add something...


    def start_playing_demo(self):

        self.pd_socket.super_clear()
        self.tot_figures = len(self.figures)
        self.exp_state = self.STATE_MOVING

        self.game_area = np.array(self.params["game_area"])
        self.game_area_code = pt.convert_map_to_horz_lines(self.game_area)

        self.delimiter = np.concatenate((np.ones((self.MAX_ROWS, 1)), np.zeros((self.MAX_ROWS, 1))), axis=1)
        self.code_delimiter = self.params["code_delimiter"]

        self.score_fig = [0, 0]
        self.score_area = np.array(self.params["score_area"])
        self.code_score = self.params["code_score"]

        self.next_figure = "L31"
        self.next_figure_code = self.params["next_figure_code"]
        self.total_figure = np.concatenate((self.game_area,self.delimiter,self.score_area),axis=1)
        self.total_figure_code = self.game_area_code + self.code_delimiter + self.next_figure_code + self.code_score


        self.pd_socket.send_cmd(self.total_figure_code)


        # START !!
        if self.params["play_music"]:
            self.music.playit(self.audios["tetris_BGM"], loop=-1)
        figure = "T31"

        self.new_figure(figure)




    def start_playing(self):

        self.pd_socket.super_clear()

        self.tot_figures = len(self.figures)

        self.exp_state = self.STATE_MOVING

        self.game_area = np.zeros((self.MAX_ROWS, self.COLS_GAME_AREA))
        self.game_area_code = ""

        self.delimiter = np.concatenate((np.ones((self.MAX_ROWS, 1)),np.zeros((self.MAX_ROWS, 1))), axis=1)
        self.code_delimiter = self.params["code_delimiter"]


        self.score_fig = [0,0]
        self.score_area = np.zeros((self.MAX_ROWS, self.COLS_SCORE_AREA))

        self.total_figure = np.concatenate((self.game_area, self.delimiter, self.score_area), axis=1)


        self.pd_socket.send_cmd(self.code_delimiter)

        self.print_score()
        for i in range(2):
            current_map = self.add_maps(self.score_fig[i].map, self.total_figure)
            self.total_figure = copy.deepcopy(current_map)

        self.score_area = self.total_figure[:, 12:]

        self.next_figure = self.figures[np.random.choice(range(1,self.tot_figures))]['name']
        self.draw_next_figure()
        current_map = self.add_maps(self.next_figure_fig.map, self.total_figure)
        self.total_figure = copy.deepcopy(current_map)

        self.total_figure_code = self.game_area_code + self.code_delimiter + self.next_figure_code + self.code_score

        # START !!
        if self.params["play_music"]:
            self.music.playit(self.audios["tetris_BGM"], loop=-1)
        figure = self.figures[np.random.choice(range(1,self.tot_figures))]['name']
        self.new_figure(figure)

    # start new figure
    def new_figure(self, figure):
        self.figure_id = self.figure_id + 1
        self.current_figure = figure
        self.create_starting_figures()
        self.start_time = time.time()
        print("figure: " + str(self.figure_id))

    def create_starting_figures(self):

        try:

            fig = self.get_figure_by_name(self.current_figure)
            tract_pos = self.params['tracts_positions']
            tag = "t" + str(self.figure_id)
            self.master_figure = Figure_Tactris(tag, fig, tract_pos[0], tract_pos[1], self.pd_socket, self.game_area, self.MAX_ROWS, self.COLS_GAME_AREA, 0)

        except ValueError:
            print("GAME OVER!!!")
            self.end_experiment()
        except Exception as e:
            print(e)

    # clean up...
    def end_experiment(self):
        self.music.playit(self.audios["game_over"])
        self.pd_socket.send_cmd(pt.clear())
        # ... and start from the beginning
        self.title_screen()

    def add_maps_on_game_area(self, map1, map2):
        new_map = np.zeros((self.MAX_ROWS, self.COLS_GAME_AREA))
        for r in range(self.MAX_ROWS):
            for c in range(self.COLS_GAME_AREA):
                new_map[r][c] = map1[r][c] + map2[r][c]
        return new_map

    def add_maps_on_score_area(self, map1, map2):
        new_map = np.zeros((self.MAX_ROWS, self.COLS_SCORE_AREA))
        for r in range(self.MAX_ROWS):
            for c in range(self.COLS_SCORE_AREA):
                new_map[r][c] = map1[r][c] + map2[r][c]
        return new_map

    # user finished moving the master figure. calc results, write them, start next figures
    def confirm_figure(self):

        self.confirm_cbk = None
        self.cancel_cbk = None

        current_map = self.add_maps_on_game_area(self.master_figure.map, self.game_area)
        self.game_area = copy.deepcopy(current_map)

        self.find_complete_lines()
        self.game_area_code = pt.convert_map_to_horz_lines(self.game_area)

        if self.deleted:
            self.speech("linea_completa")

        # start new figure
        self.pd_socket.send_cmd(pt.clear())
        self.pd_socket.send_cmd(self.code_delimiter)
        self.pd_socket.send_cmd(self.game_area_code)
        self.score_area = np.zeros((self.MAX_ROWS, self.COLS_SCORE_AREA))
        self.total_figure = np.concatenate((self.game_area, self.delimiter, self.score_area), axis=1)
        self.print_score()
        for i in range(2):
            current_map = self.add_maps(self.score_fig[i].map, self.total_figure)
            self.total_figure = copy.deepcopy(current_map)
        self.score_area = self.total_figure[:, 12:]

        self.new_figure(self.next_figure)
        self.next_figure = self.figures[np.random.choice(range(1, self.tot_figures))]['name']
        self.draw_next_figure()
        current_map = self.add_maps(self.next_figure_fig.map, self.total_figure)
        self.total_figure = copy.deepcopy(current_map)

        # self.total_figure = np.concatenate((self.game_area, self.delimiter, current_map), axis=1)
        self.total_figure_code = self.game_area_code + self.code_delimiter + self.next_figure_code + self.code_score

        self.deleted = False
        if self.params["play_audio"]:
            self.speech("muovi")



    def find_complete_lines(self):
        for i in range(0, self.game_area.shape[0]):
            if all(self.game_area[i,:]): # check if all the elements in the row are 1
                self.delete_line_and_shift(i)



    def delete_line_and_shift(self, row_index):
        self.game_area[row_index] = np.zeros(self.game_area.shape[1])
        up = self.game_area[0: row_index+1, :]
        down = self.game_area[row_index+1:,:]
        self.game_area = np.concatenate((np.roll(up,1,0),down))
        # TODO aggiungere sintesi vocale
        print("Cancellata linea " + str(row_index))
        self.deleted = True
        self.score += 1


    def get_char_by_name(self, char_name):
        for char in self.characters:
            if char['name'] == char_name:
                return copy.deepcopy(char)
        return None


    def print_level(self):
        tract_pos = self.params['level_positions']
        level = self.level+1
        fig = self.get_char_by_name(str(level))
        self.level_fig = BrailleChar("Level" + str(level), fig, tract_pos[0], tract_pos[1], self.cell_size_char[0],self.pd_socket, 0)
        self.code_level = self.level_fig.current_code_str


    def draw_next_figure(self):
        tract_pos = self.params['level_positions']
        fig = self.get_figure_by_name(self.next_figure)
        self.next_figure_fig = BrailleChar("next", fig, tract_pos[0], tract_pos[1], self.cell_size_fig[0], self.pd_socket, 0)
        # self.next_figure_fig =  Figure_Tactris("next", fig, tract_pos[0], tract_pos[1], self.pd_socket, self.score_area, self.MAX_ROWS, self.COLS_SCORE_AREA, 0)
        self.next_figure_code = self.next_figure_fig.current_code_str

    def refresh_next_figure(self):
        self.clean_space()
        self.next_figure = self.figures[np.random.choice(range(1, self.tot_figures))]['name']
        self.draw_next_figure()
        # self.add_maps_on_score_area()


    def clean_space(self):
        code = pt.convert_map_to_horz_lines_erase(self.next_figure_fig.map, "next")
        self.pd_socket.send_cmd(code)

    def print_score(self):
        string_score = "%02d" % self.score
        char_list = list(string_score)
        self.code_score = ""
        try:
            #TODO oltre il 99 farà cose strane
            for char in range(len(char_list)):
                tract_pos = self.params['score_positions'][char]
                tract_name = char_list[char]

                fig = self.get_char_by_name(tract_name)
                self.score_fig[char] = BrailleChar("score" + str(char), fig, tract_pos[0], tract_pos[1],self.cell_size_char[0], self.pd_socket, 0)
                self.code_score += self.score_fig[char].current_code_str

        except Exception as e:
            print(e)

    # report here App gestures & button presses + key presses.
    def onBPevents(self, eventtype, event):

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
                if event == 'DT':
                    self.start_playing()
            elif eventtype == 1:
                # BUTTON
                if event == '2':
                    self.start_playing()
            elif eventtype == 2:
                # KEYS
                if event == 'space':
                    self.start_playing()

        elif self.exp_state == self.STATE_MOVING:
            # =========== MOVING STATE ===========  (3directions + cw rotation + confirm + undo)

            res_move = None
            if eventtype == 0:
                # GESTURES
                if event == 'SL':
                    res_move = self.master_figure.move('left', self.game_area, 1)
                    if res_move == 1:
                        if self.params["play_audio"]:
                            self.speech('muovi_sinistra')

                elif event == 'SR':
                    res_move = self.master_figure.move('right', self.game_area, 1)
                    if res_move == 1:
                        if self.params["play_audio"]:
                            self.speech('muovi_destra')

                elif event == 'ST':
                    res_move = self.master_figure.rotate_cw(self.game_area, self.total_figure_code)
                    if res_move == 1:
                        if self.params["play_audio"]:
                            self.speech('ruota')

                elif event == 'DT':
                    res_move = self.master_figure.move_until_crash(self.game_area)
                    if res_move == 0 or res_move == -1:
                        if self.params["play_audio"]:
                            self.speech('posizionata')
                        self.confirm_figure()


            elif eventtype == 1:
                if event == '2':
                    res_move = self.master_figure.move('left', self.game_area, 1)
                    if res_move == 1:
                        self.speech('muovi_sinistra')

                elif event == '5':
                    res_move = self.master_figure.move('right', self.game_area, 1)
                    if res_move == 1:
                        self.speech('muovi_destra')

                # elif event == '4':
                #     pass
                #
                #
                # elif event == '7':
                #    pass

                elif event == '6':
                    res_move = self.master_figure.move_until_crash(self.game_area)
                    if res_move == 0 or res_move == -1:
                        if self.params["play_audio"]:
                            self.speech('posizionata')
                        self.confirm_figure()

                elif event == '3':
                    res_move = self.master_figure.rotate_cw(self.total_figure, self.game_area_code)
                    if res_move == 1:
                        self.speech('ruota')

                # elif event == '1':
                #     pass

            elif eventtype == 2:
                if event == 'left':
                    res_move = self.master_figure.move('left', self.total_figure, 1)
                    if res_move == 1:
                        if self.params["play_audio"]:
                            self.speech('muovi_sinistra')
                elif event == 'right':
                    res_move = self.master_figure.move('right', self.total_figure, 1)
                    if res_move == 1:
                        if self.params["play_audio"]:
                            self.speech('muovi_destra')
                elif event == 'up':
                    res_move = self.master_figure.rotate_cw(self.game_area, self.total_figure_code)
                    if res_move == 1:
                        if self.params["play_audio"]:
                            self.speech('ruota')
                # elif event == 'down':
                #     pass

                elif event == 'space':
                    res_move = self.master_figure.move_until_crash(self.total_figure)
                    if res_move == 0 or res_move == -1:
                        if self.params["play_audio"]:
                            self.speech('posizionata')
                        self.confirm_figure()

                # elif event == 'esc':
                #     pass


            # if res_move == 0:
            #     if self.params["play_audio"]:
            #         self.speech('posizionata')
            if res_move == -1:
                if self.params["play_audio"]:
                    self.speech('bordo')

        # always valid
        if eventtype == 2:
            # KEYS
            if event == 'r':
                self.super_refresh()
            elif event == 'c':
                self.pre_select_figure('c')

    # disable gesture/buttons while speaking. speak only in BP usage
    def speech(self, audio_string, wait=True):

        if self.modality == 0:
            current_state = self.exp_state
            self.exp_state = self.STATE_INIT
            if wait is True:
                self.tts_player.playit_wait(self.audios[audio_string], self.audio_channels[audio_string])
            else:
                self.tts_player.playit(self.audios[audio_string], self.audio_channels[audio_string])

            self.exp_state = current_state
