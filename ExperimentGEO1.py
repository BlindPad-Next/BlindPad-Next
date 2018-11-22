"""
@class ExperimentGEO1
Class that fully manage GEO1 experiment
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

from BPexercises.Common.result_file_GEO1 import Results_file_GEO1
from BPexercises.Common import primitives as pt
from BPexercises.Common.padDrawComm import PadDrawComm
from BPexercises.Common.AppConnector import AppConnector
from BPexercises.Common.keyThread import KeyThread
from BPexercises.Common.playMusic import PlayMusic


class ExperimentGEO1:
    """
    @class Experiment
    Class that fully manage GEO1
    """

    SWITCH_SEQUENCE = True
    SAY_ANSWER = False
    PLAY_QUEST = False
    NEXT_TRIAL = False
    NO_SEQUENCE = False
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
    connectors_callback = None
    stringa_intermezzo = None
    stringa_inizio = None
    stringa_leggi_consegna = None
    audio_path = None

    sequenza = None
    question = None
    tact_imgs = None
    time_for_present = None
    low_bounds = None
    wait_for_quest = None
    wait_for_imgs = None
    total_index = None
    level = None

    kt = None
    key = None
    inc_tact_img = None
    out_tact_img = None
    inc_tts_seq = None
    out_tts_seq = None
    time1 = None
    time2 = None
    reaction_time = None
    curr_img = None
    previous_img = None
    curr_tts = None
    data = None


    seq_demo_tact = None
    seq_demo_aud = None

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
                sys.stdout.write("Insert from which trial to begin [1-20]: ")
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
                self.connectors_callback = self.onBPevents_GEO1_tact_BLE
            elif self.user_mode == 0:
                self.connectors_callback = self.onBPevents_GEO1_tact_USB
        elif self.modality == 1:
            if self.user_mode == 1:
                self.connectors_callback = self.onBPevents_GEO1_aud_BLE
            elif self.user_mode == 0:
                self.connectors_callback = self.onBPevents_GEO1_aud_USB


    def debug_set_input(self, mode, ip_address, username, modality, is_familiarization):
        self.user_mode = mode
        self.ip_address = ip_address
        self.user_name = username
        self.modality = modality

        # choose callback
        if self.modality == 0:
            if self.user_mode == 1:
                self.connectors_callback = self.onBPevents_GEO1_tact_BLE
            elif self.user_mode == 0:
                self.connectors_callback = self.onBPevents_GEO1_tact_USB
        elif self.modality == 1:
            if self.user_mode == 1:
                self.connectors_callback = self.onBPevents_GEO1_aud_BLE
            elif self.user_mode == 0:
                self.connectors_callback = self.onBPevents_GEO1_aud_USB

        self.is_familiarization = is_familiarization
        if not self.is_familiarization:
            self.start_from = None
            while self.start_from is None:
                sys.stdout.write("Insert from which trial to begin [1-20]: ")
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


    def debug_set_input_demo(self, ip_address, username):
        self.ip_address = ip_address
        self.user_name = username
        self.modality = 0
        self.user_mode = 0
        self.start_from = 12
        self.connectors_callback = self.onBPevents_GEO1_tact_USB_DEMO

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
                self.pd_socket = PadDrawComm(pd_address, pd_port, False)


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
            path = os.path.join(self.params["project_path"], "input_data", "SEQUENZA_FAM.txt")
            with open(path) as file:
                seq = list(file.read().split(","))

            # OPEN FILE WITH SEQUENCES
            self.tact_imgs = {}
            file = os.path.join(self.params["project_path"], "input_data", "LVFAM.txt")
            key_lv = self.params["key_lv"] + str(1)
            with open(file) as json_file:
                self.tact_imgs[key_lv] = json.load(json_file)
        else:
            if self.modality == 0:
                path = os.path.join(self.params["project_path"], "input_data", "SEQUENZA_TATTILE.txt")
                with open(path) as file:
                    seq = list(file.read().split(","))
            elif self.modality == 1:
                path = os.path.join(self.params["project_path"], "input_data", "SEQUENZA_ACUSTICO.txt")
                with open(path) as file:
                    seq = list(file.read().split(","))

            # CREATE RESULT FILE
            path = os.path.join(self.params["project_path"], "result_data")
            if not os.path.exists(path):
                os.makedirs(path)

            # OPEN FILE
            username = self.user_name + '_' + str(self.modality)
            self.res_file = Results_file_GEO1(username, path)
            if os.path.exists(self.res_file.filename):
                self.res_file.write_heading()

            # OPEN FILE WITH SEQUENCES
            self.tact_imgs = {}
            for i in range(self.params["NUM_OF_LEVELS"]):
                key_lv = self.params["key_lv"] + str(i + 1)
                file = os.path.join(self.params["project_path"], "input_data", (str(key_lv) + ".txt"))
                with open(file) as json_file:
                    self.tact_imgs[key_lv] = json.load(json_file)

        self.sequenza = seq[self.start_from:]

        self.time_for_present = self.params["time_for_present"]
        self.low_bounds = self.params["low_bounds"]
        self.wait_for_quest = self.params["wait_for_quest"]
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
            sys.stdout.write('Ascoltare la consegna con la sintesi vocale? Premi 0 per NON ASCOLTARLA o 1 per ASCOLTARLA ')
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
                self.tts_player.playit_wait(self.audios["Consegna_Tatto"])
            elif self.modality == 1:
                self.tts_player.playit_wait(self.audios["Consegna_Acustico"])

        print(self.stringa_inizio)

        while not self.NEXT_TRIAL:
            time.sleep(self.params["delay"])
            pass

        self.start_trials()


    def start_demo(self):

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

        path = os.path.join(self.params["project_path"], "input_data", "SEQUENZA_TATTILE_DEMO.txt")
        with open(path) as file:
            seq = list(file.read().split(","))

        # CREATE RESULT FILE
        path = os.path.join(self.params["project_path"], "result_data")
        if not os.path.exists(path):
            os.makedirs(path)

        # OPEN FILE
        username = self.user_name + '_' + str(self.modality)
        self.res_file = Results_file_GEO1(username, path)
        if os.path.exists(self.res_file.filename):
            self.res_file.write_heading()

        # OPEN FILE WITH SEQUENCES
        self.tact_imgs = {}
        for i in range(self.params["NUM_OF_LEVELS"]):
            key_lv = self.params["key_lv"] + str(i + 1)
            file = os.path.join(self.params["project_path"], "input_data", (str(key_lv) + ".txt"))
            with open(file) as json_file:
                self.tact_imgs[key_lv] = json.load(json_file)

        self.sequenza = seq[self.start_from:]

        self.time_for_present = self.params["time_for_present"]
        self.low_bounds = self.params["low_bounds"]
        self.wait_for_quest = self.params["wait_for_quest"]
        self.wait_for_imgs = self.params["wait_for_imgs"]
        self.total_index = copy.deepcopy(self.start_from)

        self.NEXT_TRIAL = False

        print(self.stringa_inizio)

        while not self.NEXT_TRIAL:
            time.sleep(self.params["delay"])
            pass

        self.start_trials_demo()

    def start_trials_demo(self):

        try:
            for i in range(len(self.sequenza)):

                print("Trial n° " + str(self.total_index + 1))

                if 0 <= self.total_index <= 4:
                    self.level = 1
                elif 5 <= self.total_index <= 9:
                    self.level = 2
                elif 10 <= self.total_index <= 14:
                    self.level = 3
                elif 15 <= self.total_index <= 19:
                    self.level = 4

                self.modality = 0
                self.load_images_tact()
                self.show_images_tact()
                id_q = self.sequenza[i]
                self.question = os.path.join(self.audio_path, ("Domanda" + str(id_q) + "_en.mp3"))
                print(self.question)
                self.tts_player.playit_wait(self.question)
                self.start_timer_tact()
                self.exploration_tact()
                self.stop_timer_demo()

                print(self.stringa_intermezzo)

                # WAIT FOR THE EXPERIMENTER THAT REGISTER THE ANSWER
                while not self.NEXT_TRIAL:
                    time.sleep(self.params["delay"])
                    pass


                self.modality = 1
                self.load_images_aud()
                self.show_images_aud()
                id_q = self.sequenza[i]
                self.question = os.path.join(self.audio_path, ("Domanda" + str(id_q) + "_en.mp3"))
                print(self.question)
                self.tts_player.playit_wait(self.question)
                self.start_timer_aud()
                self.exploration_aud()
                self.stop_timer_demo()

                print(self.stringa_intermezzo)

                # WAIT FOR THE EXPERIMENTER THAT REGISTER THE ANSWER
                while not self.NEXT_TRIAL:
                    time.sleep(self.params["delay"])
                    pass

                self.total_index += 1

            self.kt.stop()
            self.app_connector.stop()
            pygame.quit()
            print("finished")

        except Exception as e:
            print(e)


    def start_trials(self):

        try:
            for i in range(len(self.sequenza)):

                print("Trial n° " + str(self.total_index + 1))


                if 0 <= self.total_index <= 4:
                    self.level = 1
                elif 5 <= self.total_index <= 9:
                    self.level = 2
                elif 10 <= self.total_index <= 14:
                    self.level = 3
                elif 15 <= self.total_index <= 19:
                    self.level = 4

                if self.modality == 0:
                    self.load_images_tact()
                    self.show_images_tact()
                elif self.modality == 1:
                    self.load_images_aud()
                    self.show_images_aud()

                id_q = self.sequenza[i]
                self.question = os.path.join(self.audio_path,("Domanda" + str(id_q) + "_en.mp3"))
                print(self.question)
                self.tts_player.playit_wait(self.question)


                if self.modality == 0:
                    self.start_timer_tact()
                    self.exploration_tact()
                elif self.modality == 1:
                    self.start_timer_aud()
                    self.exploration_aud()
                self.stop_timer()

                print(self.stringa_intermezzo)

                # WAIT FOR THE EXPERIMENTER THAT REGISTER THE ANSWER
                while not self.NEXT_TRIAL:
                    time.sleep(self.params["delay"])
                    pass

                self.total_index += 1

            self.kt.stop()
            self.app_connector.stop()
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

        key_inc = "_e" + str(couple)
        key_out = "_u" + str(couple)
        self.inc_tts_seq = os.path.join(self.audio_path, (self.key + key_inc + "_en.mp3"))
        self.out_tts_seq = os.path.join(self.audio_path, (self.key + key_out + "_en.mp3"))


    def load_images_tact(self):
        self.key = self.params["key_lv"] + str(self.level)
        curr_lv_tact_imgs = self.tact_imgs[self.key]

        couple = self.total_index - self.low_bounds[self.key] + 1
        key_inc = "e" + str(couple)
        key_out = "u" + str(couple)
        self.inc_tact_img = curr_lv_tact_imgs[key_inc]
        self.out_tact_img = curr_lv_tact_imgs[key_out]



    def show_images_aud(self):

        # 1st sequence
        self.tts_player.playit_wait(self.inc_tts_seq)
        time.sleep(self.wait_for_imgs)

        # 2nd sequence
        self.tts_player.playit_wait(self.out_tts_seq)

        # wait for question
        time.sleep(self.wait_for_quest)

    def show_images_tact(self):
        # 1st image
        self.tts_player.playit_wait(self.audios["Entrate_en"])
        time.sleep(self.wait_for_imgs)

        # present 1st image
        self.pd_socket.refresh(self.inc_tact_img)
        time.sleep(self.time_for_present[self.key])

        self.tts_player.playit_wait(self.audios["Uscite_en"])
        time.sleep(self.wait_for_imgs)

        # present 2nd image
        self.pd_socket.refresh(self.out_tact_img)
        time.sleep(self.time_for_present[self.key])

        # clear and wait for question
        self.pd_socket.send_cmd(pt.clear())
        time.sleep(self.wait_for_quest)


    def start_timer_tact(self):
        self.time1 = time.time()
        self.time_paused = 0
        self.SWITCH_SEQUENCE = False
        self.NO_SEQUENCE = True
        self.SAY_ANSWER = False
        self.NEXT_TRIAL = False
        self.PAUSED = False
        self.curr_img = self.out_tact_img
        self.previous_img = copy.deepcopy(self.out_tact_img)

    def start_timer_aud(self):
        self.time1 = time.time()
        self.time_paused = 0
        self.SWITCH_SEQUENCE = False
        self.SAY_ANSWER = False
        self.NEXT_TRIAL = False
        self.PLAY_QUEST = False
        self.PAUSED = False
        self.curr_tts = self.out_tts_seq

    def exploration_tact(self):

        while not self.SAY_ANSWER:
            if self.SWITCH_SEQUENCE:
                self.NO_SEQUENCE = False
                self.curr_img = self.inc_tact_img
            else:
                self.curr_img = self.out_tact_img

            if self.curr_img == self.previous_img:
                pass
            else:
                self.pd_socket.refresh(self.curr_img)
                print('Changing taxels...')
                self.previous_img = copy.deepcopy(self.curr_img)

            if self.NEXT_TRIAL:
                self.NEXT_TRIAL = False
                break

            if self.PAUSED:
                self.time3 = time.time()
                while self.PAUSED:
                    pass
                self.time4 = time.time()
                self.time_paused += (self.time4-self.time3)

            time.sleep(self.params["delay"])

    def exploration_aud(self):

        while not self.SAY_ANSWER:
            if self.SWITCH_SEQUENCE:
                if self.tts_player.is_playing():
                    self.tts_player.stopit()
                if self.curr_tts == self.inc_tts_seq:
                    self.curr_tts = self.out_tts_seq
                    self.tts_player.playit(self.curr_tts)
                elif self.curr_tts == self.out_tts_seq:
                    self.curr_tts = self.inc_tts_seq
                    self.tts_player.playit(self.curr_tts)

                self.SWITCH_SEQUENCE = False

            elif self.PLAY_QUEST:
                if self.tts_player.is_playing():
                    self.tts_player.stopit()

                self.tts_player.playit(self.question)

                self.PLAY_QUEST = False

            if self.NEXT_TRIAL:
                self.NEXT_TRIAL = False
                break

            if self.PAUSED:
                self.time3 = time.time()
                while self.PAUSED:
                    pass
                self.time4 = time.time()
                self.time_paused += (self.time4-self.time3)

            time.sleep(self.params["delay"])


    def stop_timer(self):
        self.time2 = time.time()
        if self.SAY_ANSWER:
            # self.tts_player.playit(self.audios["Risposta"])
            # TODO JUST FOR THE DEMO
            self.tts_player.playit(self.audios["Risposta_en"])
        self.reaction_time = self.time2 - self.time1 - self.time_paused
        self.data = [self.total_index + 1, self.reaction_time]
        if not self.is_familiarization:
            self.res_file.log_data(self.data)
        print(self.data)
        self.SAY_ANSWER = False
        if self.modality == 0:
            self.pd_socket.send_cmd(pt.clear())


    def stop_timer_demo(self):
        self.time2 = time.time()
        # if self.SAY_ANSWER:
        # self.tts_player.playit_wait(self.audios["Risposta_en"])

        self.reaction_time = self.time2 - self.time1 - self.time_paused
        self.data = [self.total_index + 1, self.reaction_time]
        self.SAY_ANSWER = False
        self.pd_socket.send_cmd(pt.clear())

    def super_refresh(self):
        self.pd_socket.refresh(self.curr_img, force=True)

    def onBPevents_GEO1_aud_BLE(self, type, event):

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
                # pass
                self.PLAY_QUEST = True
                print("Riascolta la domanda")
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
                self.PLAY_QUEST = True
                print("Riascolta la domanda")
            elif event == '5':
                self.SAY_ANSWER = True
                print("Dai la risposta")
            elif event == '6':
                pass
            elif event == '7':
                self.SWITCH_SEQUENCE = True
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


    def onBPevents_GEO1_aud_USB(self, type, event):

        msg = ''
        if type == 0:
            if event == 'SL':
                # msg = pt.move(-1, 0)
                pass
            elif event == 'SR':
                pass
                self.SWITCH_SEQUENCE = True
                print("Riascolta sequenza")
            elif event == 'SU':
                pass
            elif event == 'SD':
                pass
                # msg = pt.move(0, 1)
            elif event == 'ST':
                pass
                # msg = pt.move(0, 1)
            elif event == 'DT':
                self.SAY_ANSWER = True
                print("Dai la risposta")
                pass
            elif event == 'LP':
                # pass
                self.PLAY_QUEST = True
                print("Riascolta la domanda")
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
                self.PLAY_QUEST = True
                print("Riascolta la domanda")
            elif event == '5':
                self.SAY_ANSWER = True
                print("Dai la risposta")
            elif event == '6':
                pass
            elif event == '7':
                self.SWITCH_SEQUENCE = True
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

    def onBPevents_GEO1_tact_BLE(self, type, event):
        msg = ''
        if type == 0:
            # GESTURES
            if event == 'SL':
                pass
            elif event == 'SR':
                pass
                # msg = pt.move(1, 0)
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
                pass
            elif event == 'LP':
                pass
        elif type == 1:
            # BUTTONS
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
                self.tts_player.playit_wait(self.question)
                # PLAY_QUEST = True
                print("Riascolta la domanda")
            elif event == '5':
                self.SAY_ANSWER = True
                print("Dai la risposta")
            elif event == '6':
                pass
            elif event == '7':
                self.SWITCH_SEQUENCE = not self.SWITCH_SEQUENCE
                if self.NO_SEQUENCE:
                    print("Tocca immagine")
                    # self.tts_player.playit_wait(self.audios["Percepisci"])
                    # TODO JUST FOR THE DEMO
                    self.tts_player.playit_wait(self.audios["Percepisci_en"])
                    self.NO_SEQUENCE = False
                else:
                    print("Cambia immagine")
                    # self.tts_player.playit_wait(self.audios["Cambia"])
                    # TODO JUST FOR THE DEMO
                    self.tts_player.playit_wait(self.audios["Cambia_en"])
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
                self.super_refresh()
                self.PAUSED = False
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


    def onBPevents_GEO1_tact_USB(self, type, event):

        msg = ''
        if type == 0:
            # GESTURES
            if event == 'SL':
                pass
            elif event == 'SR':
                self.SWITCH_SEQUENCE = not self.SWITCH_SEQUENCE
                if self.NO_SEQUENCE:
                    print("Tocca immagine")
                    # self.tts_player.playit_wait(self.audios["Percepisci"])
                    # TODO JUST FOR THE DEMO
                    self.tts_player.playit_wait(self.audios["Percepisci_en"])
                    self.NO_SEQUENCE = False
                else:
                    print("Cambia immagine")
                    # self.tts_player.playit_wait(self.audios["Cambia"])
                    # TODO JUST FOR THE DEMO
                    self.tts_player.playit_wait(self.audios["Cambia_en"])
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
                self.SAY_ANSWER = True
                print("Dai la risposta")
                pass
            elif event == 'LP':
                self.tts_player.playit_wait(self.question)
                print("Riascolta la domanda")
        elif type == 1:
            # BUTTONS
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
                self.tts_player.playit_wait(self.question)
                print("Riascolta la domanda")
            elif event == '5':
                self.SAY_ANSWER = True
                print("Dai la risposta")
            elif event == '6':
                pass
            elif event == '7':
                self.SWITCH_SEQUENCE = not self.SWITCH_SEQUENCE
                if self.NO_SEQUENCE:
                    print("Tocca immagine")
                    self.tts_player.playit_wait(self.audios["Percepisci"])
                    self.NO_SEQUENCE = False
                else:
                    print("Cambia immagine")
                    self.tts_player.playit_wait(self.audios["Cambia"])
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
                self.super_refresh()
                self.PAUSED = False
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


    def onBPevents_GEO1_tact_USB_DEMO(self, type, event):

        msg = ''
        if type == 0:
            # GESTURES
            if event == 'SL':
                pass
            elif event == 'SR':
                if self.modality == 0:
                    self.SWITCH_SEQUENCE = not self.SWITCH_SEQUENCE
                    if self.NO_SEQUENCE:
                        print("Tocca immagine")
                        self.tts_player.playit_wait(self.audios["Percepisci_en"])
                        self.NO_SEQUENCE = False
                    else:
                        print("Cambia immagine")
                        self.tts_player.playit_wait(self.audios["Cambia_en"])
                elif self.modality == 1:
                    self.SWITCH_SEQUENCE = True
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
                # self.SAY_ANSWER = True
                # print("Dai la risposta")
                self.NEXT_TRIAL = True
                if self.modality == 1:
                    if self.tts_player.is_playing():
                        self.tts_player.stopit()
                print("Trial successivo")
                pass
            elif event == 'LP':
                if self.modality == 0:
                    self.tts_player.playit_wait(self.question)
                    print("Riascolta la domanda")
                elif self.modality == 1:
                    self.PLAY_QUEST = True
                    print("Riascolta la domanda")
        elif type == 1:
            # BUTTONS
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
                self.tts_player.playit_wait(self.question)
                print("Riascolta la domanda")
            elif event == '5':
                self.SAY_ANSWER = True
                print("Dai la risposta")
            elif event == '6':
                pass
            elif event == '7':
                self.SWITCH_SEQUENCE = not self.SWITCH_SEQUENCE
                if self.NO_SEQUENCE:
                    print("Tocca immagine")
                    self.tts_player.playit_wait(self.audios["Percepisci"])
                    self.NO_SEQUENCE = False
                else:
                    print("Cambia immagine")
                    self.tts_player.playit_wait(self.audios["Cambia"])
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
                if self.modality == 1:
                    if self.tts_player.is_playing():
                        self.tts_player.stopit()
                print("Trial successivo")
            elif event == 'enter':
                pass
            elif event == 'r':
                if self.modality == 0:
                    self.PAUSED = True
                    self.super_refresh()
                    self.PAUSED = False
                    print("Resetting taxels...")
                else:
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