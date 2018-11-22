"""
@class ExperimentGEO1
Class that fully manage GEO2 experiment
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

from BPexercises.Common.result_file_GEO2 import Results_file_GEO2
from BPexercises.Common import primitives as pt
from BPexercises.Common.padDrawComm import PadDrawComm
from BPexercises.Common.AppConnector import AppConnector
from BPexercises.Common.keyThread import KeyThread
from BPexercises.Common.blinkThreadGEO import BlinkThreadGEO
from BPexercises.Common.playMusic import PlayMusic


class ExperimentGEO2:
    """
    @class Experiment
    Class that fully manage GEO2
    """

    SWITCH_COLUMN = False
    DELETE_COLUMN = False
    UNDO = False
    NEXT_TRIAL = False
    COLUMN_SELECTED = False
    PAUSED = False
    time3 = None
    time4 = None
    time_paused = None

    user_mode = None
    user_name = None
    modality = None
    is_familiarization = None
    ip_address = None
    start_from = None
    read_task = None

    tts_player = None
    audios = None
    res_file = None
    pd_socket = None
    app_connector = None
    blink = None
    connectors_callback = None
    stringa_intermezzo = None
    stringa_inizio = None
    stringa_leggi_consegna = None
    audio_path = None

    sequenza = None
    answers = None
    tact_imgs = None
    time_for_present = None
    low_bounds = None
    wait_for_quest = None
    wait_for_imgs = None
    total_index = None
    level = None

    kt = None
    key = None
    sequenza_tact = None
    sequenza_pd = None
    sequence_length = None
    abs_list = None
    history_list = None
    list_tag = None
    list_col = None
    dict_param = None
    time1 = None
    time2 = None
    current_tag = None
    previous_tag = None
    index_tag_elim = None
    list_ordered = None
    index = None
    reaction_time = None
    curr_img = None
    previous_img = None
    curr_tts = None
    data = None

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self, params):

        self.params = params


        self.init_audio()

    # ask experiment data
    def get_input(self):

        # ip address of the phone
        self.ip_address = None
        while self.ip_address is None:
            sys.stdout.write('Specify the app address of the smartphone: ')
            uinput = input()
            try:
                self.ip_address = str(uinput)
                if len(self.ip_address) == 0:
                    self.ip_address = None
            except:
                pass

        # usb or BLE
        self.user_mode = None
        while self.user_mode is None:
            sys.stdout.write('Press 0 or 1 to specify whether the blindpad is connected with USB or bluetooth ')
            uinput = input()
            try:
                self.user_mode = int(uinput)
                if self.user_mode != 0:
                    if self.user_mode != 1:
                        self.user_mode = None
            except:
                pass

        # blindpad or conventional
        self.modality = None
        while self.modality is None:
            sys.stdout.write('Press 0 or 1 to specify whether is a blindpad or conventional experiment ')
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
            sys.stdout.write('Is familiarization ? Press 0 if is the real experiment or 1 if is familiarization ')
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
                sys.stdout.write("Insert from which trial to begin [1-12]: ")
                uinput = input()
                try:
                    self.start_from = int(uinput)
                    if self.start_from < 1 or self.start_from > 20:
                        self.start_from = None
                    else:
                        self.start_from -= 1
                except:
                    pass
        else:
            self.start_from = 0

        # choose callback
        if self.modality == 0:
            if self.user_mode == 1:
                self.connectors_callback = self.onBPevents_GEO2_tact_BLE
            elif self.user_mode == 0:
                self.connectors_callback = self.onBPevents_GEO2_tact_USB
        elif self.modality == 1:
            if self.user_mode == 1:
                self.connectors_callback = self.onBPevents_GEO2_aud_BLE
            elif self.user_mode == 0:
                self.connectors_callback = self.onBPevents_GEO2_aud_USB



    def debug_set_input(self, mode, ip_address, username, modality, is_familiarization):
        self.user_mode = mode
        self.ip_address = ip_address
        self.user_name = username
        self.modality = modality

        # choose callback
        if self.modality == 0:
            if self.user_mode == 1:
                self.connectors_callback = self.onBPevents_GEO2_tact_BLE
            elif self.user_mode == 0:
                self.connectors_callback = self.onBPevents_GEO2_tact_USB
        elif self.modality == 1:
            if self.user_mode == 1:
                self.connectors_callback = self.onBPevents_GEO2_aud_BLE
            elif self.user_mode == 0:
                self.connectors_callback = self.onBPevents_GEO2_aud_USB

        self.is_familiarization = is_familiarization
        if not self.is_familiarization:
            self.start_from = None
            while self.start_from is None:
                sys.stdout.write("Insert from which trial to begin [1-12]: ")
                uinput = input()
                try:
                    self.start_from = int(uinput)
                    if self.start_from < 1 or self.start_from > 12:
                        self.start_from = None
                    else:
                        self.start_from -= 1
                except:
                    pass
        else:
            self.start_from = 0


    # init audio instance and set mp3s' full paths
    def init_audio(self):

        pygame.init()
        pygame.display.set_caption('BlindPAD')
        pygame.display.set_mode((250, 20))

        self.tts_player = PlayMusic()
        self.audios = self.params["audio_files"]
        self.audio_path = os.path.join(self.params["project_path"], "audio")

        for audio in self.audios:
            self.audios[audio] = os.path.join(self.audio_path, self.audios[audio])

    # init AppConnector and PadDraw connection
    def initConnectors(self):

        # PADDRAW APP
        if self.modality == 0:
            self.pd_socket = None
            if self.params["connect_PD"] is True:
                pd_address = 'localhost'
                pd_port = 12345
                self.pd_socket = PadDrawComm(pd_address, pd_port)


        # BLINDPAD APP
        self.app_connector = None
        if self.params["connect_APP"] is True:
            self.app_connector = AppConnector(self.ip_address, self.params["app_port"],
                                              self.connectors_callback)

        return self.pd_socket, self.app_connector

    def start_experiment(self):

        self.initConnectors()

        if self.user_mode == 0:
            self.stringa_leggi_consegna = "Premere spazio quando si è pronti per la consegna..."
            self.stringa_intermezzo = "Premere spazio per passare al trial successivo..."
            self.stringa_inizio = "Premere spazio quando si è pronti per iniziare..."
        elif self.user_mode == 1:
            self.stringa_leggi_consegna = "Fare doppio tap quando si è pronti per leggere la consegna..."
            self.stringa_intermezzo = "Fare doppio tap per passare al trial successivo..."
            self.stringa_inizio = "Fare doppio tap quando si è pronti per iniziare..."

        self.kt = KeyThread(self.connectors_callback)

        # READ TRIALS SEQUENCE
        if self.is_familiarization:
            # OPEN FILE WITH SEQUENCES
            self.tact_imgs = {}
            file = os.path.join(self.params["project_path"], "input_data", "LVFAM.txt")
            key_lv = self.params["key_lv"] + str(1)
            with open(file) as json_file:
                self.tact_imgs[key_lv] = json.load(json_file)

            self.answers = {}
            file = os.path.join(self.params["project_path"], "input_data", "LVFAMans.txt")
            key_lv = self.params["key_lv"] + str(1)
            with open(file) as json_file:
                self.answers[key_lv] = json.load(json_file)

            seq = range(0,3)
        else:
            # CREATE RESULT FILE
            path = os.path.join(self.params["project_path"], "result_data")
            if not os.path.exists(path):
                os.makedirs(path)

            # OPEN FILE
            username = self.user_name + '_' + str(self.modality)
            self.res_file = Results_file_GEO2(username, path)
            if os.path.exists(self.res_file.filename):
                self.res_file.write_heading()


            # OPEN FILE WITH SEQUENCES
            self.answers = {}
            for i in range(self.params["NUM_OF_LEVELS"]):
                key_lv = self.params["key_lv"] + str(i + 1)
                file = os.path.join(self.params["project_path"], "input_data", (str(key_lv) + "ans.txt"))
                with open(file) as json_file:
                    self.answers[key_lv] = json.load(json_file)

            self.tact_imgs = {}
            for i in range(self.params["NUM_OF_LEVELS"]):
                key_lv = self.params["key_lv"] + str(i + 1)
                file = os.path.join(self.params["project_path"], "input_data", (str(key_lv) + ".txt"))
                with open(file) as json_file:
                    self.tact_imgs[key_lv] = json.load(json_file)

            seq = range(0, 12)

        self.sequenza = seq[self.start_from:]

        self.low_bounds = self.params["low_bounds"]
        self.wait_for_imgs = self.params["wait_for_imgs"]
        self.total_index = copy.deepcopy(self.start_from)

        print(self.stringa_leggi_consegna)

        while not self.NEXT_TRIAL:
            time.sleep(self.params["delay"])
            pass

        self.NEXT_TRIAL = False

        # read task ?
        self.read_task = None
        while self.read_task is None:
            sys.stdout.write(
                'Ascoltare la consegna con la sintesi vocale? Premi 0 per NON ASCOLTARLA o 1 per ASCOLTARLA ')
            uinput = input()
            try:
                self.read_task = int(uinput)
                if self.read_task != 0:
                    if self.read_task != 1:
                        self.read_task = None
            except:
                pass

        if self.read_task:
            # READ TASK DESCRIPTION
            if self.modality == 0:
                if self.is_familiarization:
                    self.tts_player.playit_wait(self.audios["Consegna_FAM"])
                else:
                    self.tts_player.playit_wait(self.audios["Consegna_Tatto"])
            elif self.modality == 1:
                self.tts_player.playit_wait(self.audios["Consegna_Acustico"])

        print(self.stringa_inizio)

        while not self.NEXT_TRIAL:
            time.sleep(self.params["delay"])
            pass

        self.start_trials()

    def start_trials(self):

        try:
            for i in range(len(self.sequenza)):

                print("Trial n° " + str(self.total_index + 1))

                if 0 <= self.total_index <= 2:
                    self.level = 1
                elif 3 <= self.total_index <= 5:
                    self.level = 2
                elif 6 <= self.total_index <= 8:
                    self.level = 3
                elif 9 <= self.total_index <= 11:
                    self.level = 4

                if self.modality == 0:
                    self.load_images_tact()
                elif self.modality == 1:
                    self.load_images_aud()


                if self.modality == 0:
                    self.start_timer_tact()
                    self.exploration_tact()
                elif self.modality == 1:
                    self.show_images_aud()
                    self.start_timer_aud()
                    self.exploration_aud()
                self.stop_timer()

                if self.is_familiarization and self.modality == 0:
                    self.show_feedback()

                print(self.stringa_intermezzo)

                # WAIT FOR THE EXPERIMENTER THAT REGISTER THE ANSWER
                while not self.NEXT_TRIAL:
                    time.sleep(self.params["delay"])
                    pass

                self.total_index += 1

            if not self.is_familiarization:
                self.res_file.log_data(self.data)
                self.res_file.close()

            self.kt.stop()
            self.app_connector.stop()
            if self.modality == 0:
                self.blink.stop()
            pygame.quit()
            print("finished")

        except Exception as e:
            print(e)
        except KeyboardInterrupt:
            self.res_file.log_data(self.data)
            self.res_file.close()


    def load_images_aud(self):
        if self.is_familiarization:
            self.key = self.params["key_lv"] + "FAM"
            couple = self.total_index - self.low_bounds[self.key] + 1
        else:
            self.key = self.params["key_lv"] + str(self.level)
            couple = self.total_index - self.low_bounds[self.key] + 1

        key_tts = "_" + str(couple)
        self.curr_tts =  os.path.join(self.audio_path, (self.key + key_tts + ".mp3"))



    def load_images_tact(self):
        self.key = self.params["key_lv"] + str(self.level)

        couple = self.total_index - self.low_bounds[self.key] + 1
        self.sequenza_tact = self.answers[self.key][str(couple)]["tact_seq"]
        self.sequenza_pd = self.tact_imgs[self.key][str(couple)]
        self.sequence_length = len(self.sequenza_tact)

        self.list_tag = []
        self.list_col = []
        self.dict_param = {}
        self.history_list = []
        start_col = 0
        # LOAD IMAGE
        for j in range(self.sequence_length):
            tag = "L"
            n = j + 1
            tag += "{0:0=2d}".format(n)
            self.list_tag.append(tag)
            curr_num = self.params["MAX_ROWS"] - self.sequenza_tact[j]
            string_col = pt.draw_vert_line(start_col,
                                           self.params["start_row"],
                                           curr_num,
                                           self.params["value"],
                                           tag)

            self.dict_param[tag] = {
                "type": "line",
                "start_col": start_col,
                "start_row":self.params["start_row"],
                "end_col": start_col,
                "end_row": curr_num,
                "value": self.params["value"],
                "tag": tag}
            self.list_col.append(string_col)
            start_col += 1
        self.abs_list = copy.deepcopy(self.list_tag)
        self.obtain_curr_img()

    def show_images_aud(self):
        if self.total_index > 0:
            self.tts_player.playit_wait(self.audios["Annuncio_aud"])

        time.sleep(self.params["wait_for_tts"])
        # 1st sequence
        self.tts_player.playit_wait(self.curr_tts)


    def start_timer_tact(self):

        self.SWITCH_COLUMN = False
        self.COLUMN_SELECTED = False
        self.NEXT_TRIAL = False
        self.PAUSED = False
        self.current_tag = self.list_tag[0]
        self.index_tag_elim = None
        self.list_ordered = []
        self.index = 0


        self.pd_socket.refresh(self.sequenza_pd)
        self.time1 = time.time()
        self.time_paused = 0

    def start_timer_aud(self):

        self.SWITCH_COLUMN = False
        self.DELETE_COLUMN = False
        self.NEXT_TRIAL = False
        self.UNDO = False
        self.PAUSED = False
        self.time1 = time.time()
        self.time_paused = 0

    def exploration_tact(self):

        while True:

            if not self.COLUMN_SELECTED:
                if self.SWITCH_COLUMN:
                    self.blink = BlinkThreadGEO(self.dict_param[self.current_tag], self.params["delay"], self.pd_socket)
                    self.SWITCH_COLUMN = False
                    self.COLUMN_SELECTED = True
            else:
                if self.SWITCH_COLUMN:
                    self.index += 1
                    if self.index > len(self.list_tag) - 1:
                        self.index = 0

                    self.previous_tag = copy.deepcopy(self.current_tag)
                    self.current_tag = self.list_tag[self.index]

                    self.blink.change_figure(self.dict_param[self.previous_tag], self.dict_param[self.current_tag])

                    self.SWITCH_COLUMN = False

            if self.DELETE_COLUMN:
                # ritorna alla prima...
                # self.blink.change_figure(self.dict_param[self.list_tag[0]])
                # oppure passa alla successiva
                j = copy.deepcopy(self.index)
                if (j + 1) > len(self.list_tag) - 1:
                    jx = 0
                    j = 0
                else:
                    jx = j + 1

                self.blink.change_figure_delete(self.dict_param[self.list_tag[jx]])
                # last_tag_elim = copy.deepcopy(current_tag)
                self.index_tag_elim = copy.deepcopy(self.index)
                self.list_ordered.append(self.current_tag)

                self.list_tag.remove(self.current_tag)
                print("Removed: " + self.current_tag)

                self.list_col.pop(self.index_tag_elim)
                self.history_list.append((self.curr_img, self.current_tag, self.index_tag_elim))
                self.obtain_curr_img()
                self.update_sequence()

                self.current_tag = self.list_tag[j]  # se ritorna alla prima list_tag[0]
                # in order to put the index at the right position
                self.index = copy.deepcopy(j)
                print("Current: " + self.current_tag)
                print("Index: " + str(self.index))
                self.previous_tag = None
                self.DELETE_COLUMN = False
                print("Deleting...")
                print("Current list: " + str(self.list_tag))


            if self.UNDO:
                if not self.list_ordered:
                    pass
                    self.UNDO = False
                else:
                    self.curr_img = copy.deepcopy(self.history_list[-1][0])
                    self.update_sequence()
                    self.index = copy.deepcopy(self.history_list[-1][2])
                    ###############################################################
                    # self.pd_socket.reset_vert_line(self.dict_param[self.current_tag])
                    r = self.list_ordered.pop()
                    self.previous_tag = copy.deepcopy(self.current_tag)
                    self.current_tag = copy.deepcopy(r)
                    # self.pd_socket.reset_vert_line(self.dict_param[self.current_tag])
                    self.blink.change_figure(self.dict_param[self.previous_tag], self.dict_param[self.current_tag])

                    string_to_insert = pt.draw_line(self.dict_param[self.current_tag]["start_col"],
                                                   self.dict_param[self.current_tag]["start_row"],
                                                   self.dict_param[self.current_tag]["end_col"],
                                                   self.dict_param[self.current_tag]["end_row"],
                                                   self.dict_param[self.current_tag]["value"],
                                                   self.dict_param[self.current_tag]["tag"])

                    self.list_tag.insert(self.index, self.current_tag)
                    self.list_col.insert(self.index, string_to_insert)

                    print("Undo...")
                    print("Current list: " + str(self.list_tag))
                    self.UNDO = False
                    self.history_list.pop()

            if len(self.list_tag) == 1:
                self.list_ordered.extend(self.list_tag)
                print("Sequenza ordinata")
                break

            if self.NEXT_TRIAL:
                self.NEXT_TRIAL = False
                break

            if self.PAUSED:
                self.time3 = time.time()
                while self.PAUSED:
                    pass
                self.time4 = time.time()
                self.time_paused += (self.time4-self.time3)

            # time.sleep(self.params["delay"])

    def exploration_aud(self):

        while not self.NEXT_TRIAL:
            if self.SWITCH_COLUMN:
                # if self.tts_player.is_playing():
                #     self.tts_player.stopit()

                self.tts_player.playit(self.curr_tts)

                self.SWITCH_COLUMN = False

            if self.PAUSED:
                self.time3 = time.time()
                while self.PAUSED:
                    pass
                self.time4 = time.time()
                self.time_paused += (self.time4-self.time3)



    def stop_timer(self):
        self.NEXT_TRIAL = False
        self.time2 = time.time()
        if self.modality == 0:
            if self.is_familiarization:
                self.tts_player.playit(self.audios["Ordinata"])
            else:
                self.tts_player.playit_wait(self.audios["Completa"])
        self.reaction_time = self.time2 - self.time1 - self.time_paused
        result = []
        if self.modality == 0:
            for i in range(len(self.list_ordered)):
                result.append(self.params["MAX_ROWS"] - self.dict_param[self.list_ordered[i]]["end_row"])
        self.data = [self.total_index + 1, self.reaction_time, result]
        if not self.is_familiarization:
            self.res_file.log_data(self.data)
            print(self.data)
        if self.modality == 0:
            self.blink.stop()
            self.pd_socket.send_cmd(pt.clear())


    def obtain_curr_img(self):

        self.curr_img = ''.join(self.list_col)


    def show_feedback(self):

        for i in range(3):
            line = self.list_ordered[i]
            self.pd_socket.send_cmd(pt.draw_vert_line(i,
                                                 self.dict_param[line]["start_row"],
                                                 self.dict_param[line]["end_row"],
                                                 self.dict_param[line]["value"],
                                                 self.dict_param[line]["tag"]))
            time.sleep(0.3)

    def super_refresh_pause_blink(self):
        self.blink.stop()
        self.pd_socket.refresh(self.curr_img, force=True)
        # self.blink.resume()
        self.blink = BlinkThreadGEO(self.dict_param[self.current_tag], self.params["delay"], self.pd_socket)


    def update_sequence(self):
        self.pd_socket.send_cmd(pt.clear())
        self.pd_socket.send_cmd(self.curr_img)

    def onBPevents_GEO2_aud_BLE(self, type, event):

        msg = ''
        if type == 0:
            if event == 'SL':
                # msg = pt.move(-1, 0)
                pass
            elif event == 'SR':
                pass
            elif event == 'SU':
                pass
            elif event == 'SD':
                pass
                # msg = pt.move(0, 1)
            elif event == 'ST':
                pass
                # msg = pt.move(0, 1)
            elif event == 'DT':
                self.NEXT_TRIAL = True
                print("Trial successivo")
            elif event == 'LP':
                pass
        elif type == 1:
            if event == '1':
                pass
                # msg = pt.move(1, 0)
            elif event == '2':
                pass
                # msg = pt.move(0, -1)
            elif event == '3':
                pass
                # msg = pt.move(0, 1)
            elif event == '4':
                pass
            elif event == '5':
                pass
            elif event == '6':
                pass
            elif event == '7':
                self.SWITCH_COLUMN = True
                print("Riascolta sequenza")
        elif type == 2:
            if event == 'left':
                pass
                # msg = pt.move(-1, 0)
            elif event == 'right':
                pass
                # msg = pt.move(1, 0)
            elif event == 'up':
                pass
                # msg = pt.move(0, -1)
            elif event == 'down':
                pass
                # msg = pt.move(0, 1)
            elif event == 'space':
                pass
            elif event == 'enter':
                pass
            elif event == 'r':
                # self.pd_socket.refresh(self.curr_img, force=False)
                # print("Resetting taxels...")
                pass
            elif event == 'p':
                self.PAUSED = not self.PAUSED
                if self.PAUSED:
                    print("Pausa... premi p per riprendere l'esperimento")
                else:
                    print("Esperimento ripreso")
                pass
            elif event == 'c':
                # self.pd_socket.super_clear()
                # print("Super clear!")
                pass


    def onBPevents_GEO2_aud_USB(self, type, event):

        msg = ''
        if type == 0:
            if event == 'SL':
                # msg = pt.move(-1, 0)
                pass
            elif event == 'SR':
                self.SWITCH_COLUMN = True
                print("Riascolta sequenza")
                pass

            elif event == 'SU':
                pass
            elif event == 'SD':
                pass
                # msg = pt.move(0, 1)
            elif event == 'ST':
                pass
                # msg = pt.move(0, 1)
            elif event == 'DT':

                pass
            elif event == 'LP':
                pass
        elif type == 1:
            if event == '1':
                pass
                # msg = pt.move(1, 0)
            elif event == '2':
                pass
                # msg = pt.move(0, -1)
            elif event == '3':
                pass
                # msg = pt.move(0, 1)
            elif event == '4':
                pass
            elif event == '5':
                pass
            elif event == '6':
                pass
            elif event == '7':
                pass
        elif type == 2:
            if event == 'left':
                pass
                # msg = pt.move(-1, 0)
            elif event == 'right':
                pass
                # msg = pt.move(1, 0)
            elif event == 'up':
                pass
                # msg = pt.move(0, -1)
            elif event == 'down':
                pass
                # msg = pt.move(0, 1)
            elif event == 'space':
                self.NEXT_TRIAL = True
                print("Trial successivo")
            elif event == 'enter':
                pass
            elif event == 'r':
                # self.pd_socket.refresh(self.curr_img, force=False)
                # print("Resetting taxels...")
                pass
            elif event == 'p':
                self.PAUSED = not self.PAUSED
                if self.PAUSED:
                    print("Pausa... premi p per riprendere l'esperimento")
                else:
                    print("Esperimento ripreso")
                pass
            elif event == 'c':
                # self.pd_socket.super_clear()
                # print("Super clear!")
                pass

    def onBPevents_GEO2_tact_BLE(self, type, event):
        msg = ''
        if type == 0:
            # GESTURES
            if type == 0:
                if event == 'SL':
                    # msg = pt.move(-1, 0)
                    pass
                elif event == 'SR':
                    pass
                elif event == 'SU':
                    pass
                elif event == 'SD':
                    pass
                    # msg = pt.move(0, 1)
                elif event == 'ST':
                    pass
                    # msg = pt.move(0, 1)
                elif event == 'DT':
                    pass
                    self.NEXT_TRIAL = True
                    print("Trial successivo")
                elif event == 'LP':
                    pass
        elif type == 1:
            # BUTTONS
            if event == '1':
                self.UNDO = True
                if not self.list_ordered:
                    self.tts_player.playit(self.audios["Nessuna"])
                else:
                    print("Annulla scelta")
                    self.tts_player.playit(self.audios["Annulla"])
            elif event == '2':
                self.DELETE_COLUMN = True
                print("Cancella colonna")
                if len(self.list_tag) == 2:
                    pass
                else:
                    self.tts_player.playit(self.audios["Cancella"])
            elif event == '3':
                pass
                # msg = pt.move(0, 1)
            elif event == '4':
                pass
            elif event == '5':
                if not self.COLUMN_SELECTED:
                    print("Prima colonna")
                    self.tts_player.playit_wait(self.audios["Prima"])
                else:
                    print("Cambia colonna")
                    self.tts_player.playit_wait(self.audios["Cambia"])
                pass
            elif event == '6':
                pass
            elif event == '7':
                pass
        elif type == 2:
            # KEYS
            if event == 'left':
                pass
                # msg = pt.move(-1, 0)
            elif event == 'right':
                pass
                # msg = pt.move(1, 0)
            elif event == 'up':
                pass
                # msg = pt.move(0, -1)
            elif event == 'down':
                pass
                # msg = pt.move(0, 1)
            elif event == 'space':
                pass
            elif event == 'enter':
                pass
            elif event == 'r':
                self.PAUSED = True
                self.super_refresh_pause_blink()
                self.PAUSED = False
                print("Resetting taxels...")
                print("Resetting taxels...")
                pass
            elif event == 'p':
                self.PAUSED = not self.PAUSED
                if self.PAUSED:
                    print("Pausa... premi p per riprendere l'esperimento")
                else:
                    print("Esperimento ripreso")
                pass
            elif event == 'c':
                self.pd_socket.super_clear()
                print("Super clear!")
                pass


    def onBPevents_GEO2_tact_USB(self, type, event):

        msg = ''
        if type == 0:
            # GESTURES
            if event == 'SL':
                pass
            elif event == 'SR':
                if not self.COLUMN_SELECTED:
                    self.SWITCH_COLUMN = True
                    print("Prima colonna")
                    self.tts_player.playit_wait(self.audios["Prima"])
                else:
                    self.SWITCH_COLUMN = True
                    print("Cambia colonna")
                    self.tts_player.playit_wait(self.audios["Cambia"])
                pass

            elif event == 'SU':
                pass
            elif event == 'SD':
                pass
                # msg = pt.move(0, 1)
            elif event == 'ST':
                pass
                # msg = pt.move(0, 1)
            elif event == 'DT':
                self.DELETE_COLUMN = True
                print("Cancella colonna")
                if len(self.list_tag) == 2:
                    pass
                else:
                    self.tts_player.playit(self.audios["Cancella"])
            elif event == 'LP':
                self.UNDO = True
                if not self.list_ordered:
                    self.tts_player.playit(self.audios["Nessuna"])
                else:
                    print("Annulla scelta")
                    self.tts_player.playit(self.audios["Annulla"])
                pass
        elif type == 1:
            # BUTTONS
            if event == '1':
                self.UNDO = True
                print("Annulla scelta")
                self.tts_player.playit(self.audios["Annulla"])
            elif event == '2':
                self.DELETE_COLUMN = True
                print("Cancella colonna")
                self.tts_player.playit(self.audios["Cancella"])
            elif event == '3':
                pass
                # msg = pt.move(0, 1)
            elif event == '4':
                pass
            elif event == '5':
                if not self.COLUMN_SELECTED:
                    self.SWITCH_COLUMN = True
                    print("Prima colonna")
                    self.tts_player.playit_wait(self.audios["Prima"])
                else:
                    self.SWITCH_COLUMN = True
                    print("Cambia colonna")
                    self.tts_player.playit_wait(self.audios["Cambia"])
                pass
            elif event == '6':
                pass
            elif event == '7':
                pass
        elif type == 2:
            # KEYS
            if event == 'left':
                pass
                # msg = pt.move(-1, 0)
            elif event == 'right':
                pass
                # msg = pt.move(1, 0)
            elif event == 'up':
                pass
                # msg = pt.move(0, -1)
            elif event == 'down':
                pass
                # msg = pt.move(0, 1)
            elif event == 'space':
                self.NEXT_TRIAL = True
                print("Trial successivo")
            elif event == 'enter':
                pass
            elif event == 'r':
                self.PAUSED = True
                self.super_refresh_pause_blink()
                self.PAUSED = False
                print("Resetting taxels...")
                print("Resetting taxels...")
                pass
            elif event == 'p':
                self.PAUSED = not self.PAUSED
                if self.PAUSED:
                    print("Pausa... premi p per riprendere l'esperimento")
                else:
                    print("Esperimento ripreso")
                pass
            elif event == 'c':
                self.pd_socket.super_clear()
                print("Super clear!")
                pass
