"""
@TTS
This file contains the function used to generate the texts used in GEO1_acoustic experiment
@author Angelo Raspagliesi, Alberto Inuggi, Luca Brayda
@copyright Istituto Italiano di Tecnologia (IIT) 2018
"""


import random
from gtts import gTTS
import os
from playsound import playsound


def entrate(ent, lv):

    string = "Entrate mensili. "

    if lv == 1:
        string += "Primo mese: " + str(int(ent[0])) + " euro, " + "Secondo mese: " + str(int(ent[1])) + " euro."
    elif lv == 2:
        string += "Primo mese: " + str(int(ent[0])) + " euro, " + "Secondo mese: " + str(int(ent[1])) + " euro, " \
                + "Terzo mese: " + str(int(ent[2])) + " euro, " + "Quarto mese: " + str(int(ent[3])) + " euro."
    elif lv == 3:
        string += "Primo mese: " + str(int(ent[0])) + " euro, " + "Secondo mese: " + str(int(ent[1])) + " euro, " \
                + "Terzo mese: " + str(int(ent[2])) + " euro, " + "Quarto mese: " + str(int(ent[3])) + " euro, " \
                + "Quinto mese: " + str(int(ent[4])) + " euro, " + "Sesto mese: " + str(int(ent[5])) + " euro."
    elif lv == 4:
        string += "Primo mese: " + str(int(ent[0])) + " euro, " + "Secondo mese: " + str(int(ent[1])) + " euro, " \
                + "Terzo mese: " + str(int(ent[2])) + " euro, " + "Quarto mese: " + str(int(ent[3])) + " euro, " \
                + "Quinto mese: " + str(int(ent[4])) + " euro, " + "Sesto mese: " + str(int(ent[5])) + " euro, " \
                + "Settimo mese: " + str(int(ent[6])) + " euro, " + "Ottavo mese: " + str(int(ent[7])) + " euro, " \
                + "Nono mese: " + str(int(ent[8])) + " euro, " + "Decimo mese: " + str(int(ent[9])) + " euro, " \
                + "Undicesimo mese: " + str(int(ent[10])) + " euro, " + "Dodicesimo mese: " + str(int(ent[11])) + " euro."

    return string


def uscite(usc, lv):

    string = "Uscite mensili. "

    if lv == 1:
        string += "Primo mese: " + str(int(usc[0])) + " euro, " + "Secondo mese: " + str(int(usc[1])) + " euro."
    elif lv == 2:
        string += "Primo mese: " + str(int(usc[0])) + " euro, " + "Secondo mese: " + str(int(usc[1])) + " euro, " \
                + "Terzo mese: " + str(int(usc[2])) + " euro, " + "Quarto mese: " + str(int(usc[3])) + " euro."
    elif lv == 3:
        string += "Primo mese: " + str(int(usc[0])) + " euro, " + "Secondo mese: " + str(int(usc[1])) + " euro, " \
                + "Terzo mese: " + str(int(usc[2])) + " euro, " + "Quarto mese: " + str(int(usc[3])) + " euro, " \
                + "Quinto mese: " + str(int(usc[4])) + " euro, " + "Sesto mese: " + str(int(usc[5])) + " euro."
    elif lv == 4:
        string += "Primo mese: " + str(int(usc[0])) + " euro, " + "Secondo mese: " + str(int(usc[1])) + " euro, " \
                + "Terzo mese: " + str(int(usc[2])) + " euro, " + "Quarto mese: " + str(int(usc[3])) + " euro, " \
                + "Quinto mese: " + str(int(usc[4])) + " euro, " + "Sesto mese: " + str(int(usc[5])) + " euro, " \
                + "Settimo mese: " + str(int(usc[6])) + " euro, " + "Ottavo mese: " + str(int(usc[7])) + " euro, " \
                + "Nono mese: " + str(int(usc[8])) + " euro, " + "Decimo mese: " + str(int(usc[9])) + " euro, " \
                + "Undicesimo mese: " + str(int(usc[10])) + " euro, " + "Dodicesimo mese: " + str(int(usc[11])) + " euro."

    return string


def entrate_en(ent, lv):

    string = "Monthly income. "

    if lv == 1:
        string += "First month: " + str(int(ent[0])) + " euro, " + "Second month: " + str(int(ent[1])) + " euro."
    elif lv == 2:
        string += "First month: " + str(int(ent[0])) + " euro, " + "Second month: " + str(int(ent[1])) + " euro, " \
                + "Third month: " + str(int(ent[2])) + " euro, " + "Fourth month: " + str(int(ent[3])) + " euro."
    elif lv == 3:
        string += "First month: " + str(int(ent[0])) + " euro, " + "Second month: " + str(int(ent[1])) + " euro, " \
                + "Third month: " + str(int(ent[2])) + " euro, " + "Fourth month: " + str(int(ent[3])) + " euro, " \
                + "Fifth month: " + str(int(ent[4])) + " euro, " + "Sixth month: " + str(int(ent[5])) + " euro."
    elif lv == 4:
        string += "First month: " + str(int(ent[0])) + " euro, " + "Second month: " + str(int(ent[1])) + " euro, " \
                + "Third month: " + str(int(ent[2])) + " euro, " + "Fourth month: " + str(int(ent[3])) + " euro, " \
                + "Fifth month: " + str(int(ent[4])) + " euro, " + "Sixth month: " + str(int(ent[5])) + " euro, " \
                + "Seventh month: " + str(int(ent[6])) + " euro, " + "Eighth month: " + str(int(ent[7])) + " euro, " \
                + "Ninth mese: " + str(int(ent[8])) + " euro, " + "Tenth month: " + str(int(ent[9])) + " euro, " \
                + "Eleventh month: " + str(int(ent[10])) + " euro, " + "Twelfth month: " + str(int(ent[11])) + " euro."

    return string


def uscite_en(usc, lv):

    string = "Monthly outcome. "

    if lv == 1:
        string += "First month: " + str(int(usc[0])) + " euro, " + "Second month: " + str(int(usc[1])) + " euro."
    elif lv == 2:
        string += "First month: " + str(int(usc[0])) + " euro, " + "Second month: " + str(int(usc[1])) + " euro, " \
                  + "Third month: " + str(int(usc[2])) + " euro, " + "Fourth month: " + str(int(usc[3])) + " euro."
    elif lv == 3:
        string += "First month: " + str(int(usc[0])) + " euro, " + "Second month: " + str(int(usc[1])) + " euro, " \
                  + "Third month: " + str(int(usc[2])) + " euro, " + "Fourth month: " + str(int(usc[3])) + " euro, " \
                  + "Fifth month: " + str(int(usc[4])) + " euro, " + "Sixth month: " + str(int(usc[5])) + " euro."
    elif lv == 4:
        string += "First month: " + str(int(usc[0])) + " euro, " + "Second month: " + str(int(usc[1])) + " euro, " \
                  + "Third month: " + str(int(usc[2])) + " euro, " + "Fourth month: " + str(int(usc[3])) + " euro, " \
                  + "Fifth month: " + str(int(usc[4])) + " euro, " + "Sixth month: " + str(int(usc[5])) + " euro, " \
                  + "Seventh month: " + str(int(usc[6])) + " euro, " + "Eighth month: " + str(int(usc[7])) + " euro, " \
                  + "Ninth mese: " + str(int(usc[8])) + " euro, " + "Tenth month: " + str(int(usc[9])) + " euro, " \
                  + "Eleventh month: " + str(int(usc[10])) + " euro, " + "Twelfth month: " + str(int(usc[11])) + " euro."

    return string



def rand_question():
    q = random.randrange(0, 2)
    if q == 0:
        string = "Domanda.  Globalmente, sono di più le entrate o le uscite?"
    elif q == 1:
        q = random.randrange(0, 2)
        if q == 0:
            string = "Domanda.  In quale mese hai avuto più entrate?"
            q += 1
        elif q == 1:
            string = "Domanda.  In quale mese hai avuto più uscite?"
            q += 1
    return q, string

def question(idq):

    idq = str(idq)
    if idq == '1':
        string =  "Domanda.  Globalmente, sono di più le entrate o le uscite?"
    elif idq == '2':
        string = "Domanda.  In quale mese hai avuto più entrate?"
    elif idq == '3':
        string = "Domanda.  In quale mese hai avuto più uscite?"

    return string

def question_en(idq):


    idq = str(idq)
    if idq == '1':
        string = "Question. Globally, are more the income or the outcomes?"
    elif idq == '2':
        string = "Question. In which month did you get more income?"
    elif idq == '3':
        string = "Question. In which month did you get more outcome?"

    return string


def answers(ans, q):

    months = {"1": "Primo mese",
              "2": "Secondo mese",
              "3": "Terzo mese",
              "4": "Quarto mese",
              "5": "Quinto mese",
              "6": "Sesto mese",
              "7": "Settimo mese",
              "8": "Ottavo mese",
              "9": "Nono mese",
              "10": "Decimo mese",
              "11": "Undicesiimo mese",
              "12": "Dodicesimo mese"
              }

    string = "La risposta corretta è: "

    if q == 0:
        if ans[q] == 1:
            string += "le entrate"
        elif ans[q] == 0:
            string += "le uscite"
    else:
        string += months[str(ans[q])]

    return string


def speak(string):
    """
    Converts text to speech
    :param whattosay: Text to speak
    """

    # audio_file = "response.mp3"
    # tts = gTTS(text=str(string), lang="en")
    # file1 = str("response" + str(i) + ".mp3")
    # tts.save(file1
    # tts.save(audio_file)
    # playsound(audio_file)
    # # os.remove(audio_file)

    r1 = random.randint(1, 10000000)
    r2 = random.randint(1, 10000000)

    randfile = str(r2) + "randomtext" + str(r1) + ".mp3"

    tts = gTTS(text=str(string), lang='en')
    tts.save(randfile)
    playsound(randfile)

    # print(randfile)
    os.remove(randfile)