"""
@class DemoBraille
Class that fully manage the braille demo
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
from BPexercises.Braille.BrailleChar import BrailleChar
from BPexercises.Common.playMusic import PlayMusic
from BPexercises.GEO3.ExperimentGEO3 import ExperimentGEO3
from BPexercises.Common.TTS import speak
from gtts import gTTS


class DemoBraille(ExperimentGEO3):
    """
    @class Experiment
    Class that fully manage DemoBraille
    """

    # string = None
    MAX_NUM_CHAR = None
    MAX_NUM_CHAR_6dot = 28
    MAX_NUM_CHAR_8dot = 12

    characters = None
    cell_size = None
    current_cell = None
    string_length = None

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self, params, callback=None):

        self.params = params

        if callback is None:
            self.connectors_callback = self.onBPevents
        else:
            self.connectors_callback = callback

        self.init_audio()

    # START EXPERIMENT
    def start_demo(self):

        self.initConnectors()

        if self.modality == 0:
            self.MAX_NUM_CHAR = len(self.params["tracts_positions"][self.modality])
            # READ FIGURES DICTIONARY
            path = os.path.join(self.params["project_path"], "input_data", "braille_char_6dots.json")
            with open(path) as json_file:
                file = json.load(json_file)
                self.cell_size = file['cell_size']
                self.characters = file['characters']
        elif self.modality == 1:
            self.MAX_NUM_CHAR = len(self.params["tracts_positions"][self.modality])# READ FIGURES DICTIONARY
            path = os.path.join(self.params["project_path"], "input_data", "braille_char_8dots.json")
            with open(path) as json_file:
                file = json.load(json_file)
                self.cell_size = file['cell_size']
                self.characters = file['characters']

        # START !!
        self.read_and_print()


    # read and print a string from input
    def read_and_print(self):
        self.string_length = None
        self.current_cell = 0

        sys.stdout.write("Inserire la stringa da mostrare con BlindPad (massimo " + str(self.MAX_NUM_CHAR) + " caratteri compresi gli spazi): ")
        while self.string_length is None:
            string = input()
            self.string_length = len(string)
            if self.string_length > self.MAX_NUM_CHAR:
                print("La stringa è lunga " + str(self.string_length) + " caratteri. Inserire una stringa più corta (max " + str(self.MAX_NUM_CHAR) + " caratteri compresi gli spazi): ")
                self.string_length = None
            else:
                if self.modality == 0:

                    words_list = string.split()
                    self.check_string_length_for_6_dot(words_list)
                elif self.modality == 1:
                   pass

        speak(string)
        self.string_to_braille(string)



    def string_to_braille(self, string):
        self.pd_socket.send_cmd(pt.clear())
        self.existing_figures = []
        # First, separate the words inside the string
        words_list = string.split()
        if self.modality == 0:
            self.check_and_print_word_for_6_dot(words_list)
        elif self.modality == 1:
            for word in range(len(words_list)):
                char_list = list(words_list[word])
                self.print_braille_word(char_list)

                # lascio lo spazio solo se non è finita la riga
                # if self.current_cell != 5 and self.current_cell != 10:
                #     self.current_cell += 1 # once the word is ended put a empty cell

        self.read_and_print()

    def print_braille_word(self, char_list):

        try:

            for char in range(len(char_list)):
                tract_pos = self.params['tracts_positions'][self.modality][self.current_cell]
                tract_name = char_list[char]

                if self.modality == 0:
                    trial_rot = 0
                elif self.modality == 1:
                    trial_rot = 1

                fig = self.get_char_by_name(tract_name)
                self.existing_figures.append(BrailleChar("tract" + str(char), fig, tract_pos[1], tract_pos[0], self.cell_size[trial_rot], self.pd_socket, trial_rot))
                self.current_cell +=1

            self.current_cell +=1 # put an empty cell once the word is ended

        except Exception as e:
            print(e)

    def onBPevents(self, eventtype, event):
        pass
        if event == 'esc':
            sys.exit(0)

        # return the figure associated to the given fig_name

    def get_char_by_name(self, char_name):
        for char in self.characters:
            if char['name'] == char_name:
                return copy.deepcopy(char)
        return None


    def check_string_length_for_6_dot(self, words_list):
        # - aggiungere 1 carattere per ogni numero
        # - aggiungere 1 carattere per ogni parola che inizia con una lettera maiuscola
        # - aggiungere 2 caratteri per ogni parola scritta interamente in maiuscolo
        for word in range(len(words_list)):
            if words_list[word].isupper():
                self.string_length += 2
            elif words_list[word].istitle():
                self.string_length += 1
            elif words_list[word].isdigit():
                self.string_length += 1
        if self.string_length > self.MAX_NUM_CHAR:
            print("La stringa è lunga " + str(self.string_length) + " caratteri. I numeri e le lettere maiuscole richiedono 1 carattere in più, mentre le parole interamente maiuscole ne richiedono 2")
            print("Inserire la stringa da mostrare con BlindPad (massimo " + str(self.MAX_NUM_CHAR) + " caratteri compresi gli spazi): ")
            self.string_length = None

    def check_and_print_word_for_6_dot(self, words_list):
        for word in range(len(words_list)):
            if words_list[word].isupper():  # check if all the letters are capitalized
                for i in range(2):  # add 2 braille char for capital letter
                    tract_pos = self.params['tracts_positions'][self.modality][self.current_cell]
                    fig = self.get_char_by_name("shift")
                    self.existing_figures.append(BrailleChar("tract" + str(word), fig, tract_pos[1], tract_pos[0], self.cell_size[0],self.pd_socket, 0))
                    self.current_cell += 1
                char_list = list(words_list[word])
                self.print_braille_word(char_list)
            elif words_list[word].istitle():  # check if only the first letter is uppercase
                # add one braille char for capital letter
                tract_pos = self.params['tracts_positions'][self.modality][self.current_cell]
                fig = self.get_char_by_name("shift")
                self.existing_figures.append(BrailleChar("tract" + str(word), fig, tract_pos[1], tract_pos[0], self.cell_size[0], self.pd_socket, 0))
                self.current_cell += 1
                char_list = list(words_list[word])
                self.print_braille_word(char_list)
            elif words_list[word].isdigit():  # check if all the characters are digits
                tract_pos = self.params['tracts_positions'][self.modality][self.current_cell]
                fig = self.get_char_by_name("Num")
                self.existing_figures.append(BrailleChar("tract" + str(word), fig, tract_pos[1], tract_pos[0], self.cell_size[0], self.pd_socket, 0))
                self.current_cell += 1
                char_list = list(words_list[word])
                self.print_braille_word(char_list)
            else:
                char_list = list(words_list[word])
                self.print_braille_word(char_list)