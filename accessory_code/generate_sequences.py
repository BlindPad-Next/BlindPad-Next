"""
@generate_sequences
This script generates RANDOM sequences for the GEO1 experiment
@author Angelo Raspagliesi, Alberto Inuggi, Luca Brayda
@copyright Istituto Italiano di Tecnologia (IIT) 2018
"""


import random
import numpy as np
import json
from BPexercises.Common import primitives as pt
from BPexercises.Common import TTS as tts
from gtts import gTTS


# BLINDPAD PARAMETERS
N_ROWS = 12
N_COLUMNS = 16

# EXPERIMENT PARAMETERS
LV = 4  # LV1 ok non rigenerare
SEQ_LEN = [2, 4, 6, 12]

N_TRIALS = 5

for i in range(len(SEQ_LEN)):
    if i == LV - 1:
        sequence_length = SEQ_LEN[i]
        break

entrate = np.zeros((N_TRIALS, sequence_length))
uscite = np.zeros((N_TRIALS, sequence_length))


# COMBINATION PARAMETERS
win = True
win2 = True
diff_min = 3
diff_max = 5
MAX = N_ROWS - 2

# GENERATE THE SEQUENCES ################################################
for n in range(N_TRIALS):

    seq_en = []
    seq_us = []

    for i in range(sequence_length):
        while True:
            if win:
                while True:
                    a = random.randrange(4, MAX)
                    b = random.randrange(2, MAX/2 + 1)  # magari fare da 2 a 6
                    if win2:
                        if diff_min <= abs(a - b) <= diff_max:
                            break
                    else:
                        break
            else:
                while True:
                    a = random.randrange(2, MAX/2 + 1)
                    b = random.randrange(3, MAX)
                    if win2:
                        if diff_min <= abs(a - b) <= diff_max:
                            break
                    else:
                        break
            if not seq_en:
                break
            elif len(seq_en) >= 1:
                max_a = max(seq_en)
                max_b = max(seq_us)
                if a != max_a and b != max_b:
                    break
        seq_en.append(a)
        seq_us.append(b)

    entrate[n] = seq_en
    uscite[n] = seq_us
    win = not win
    win2 = not win2
#####################################################################


# CREATE THE STRINGS FOR TTS ########################################

entrate_tts = entrate * 10
uscite_tts = uscite * 10

# for n in range(N_TRIALS):
#
#     str_to_tts = tts.entrate(entrate_tts[n], LV)
#     text_to_speach = gTTS(str_to_tts, lang='it')
#     audio_name = "LV" + str(LV) + "_e" + str(n + 1) + ".mp3"
#     text_to_speach.save(audio_name)
#     str_to_tts = tts.uscite(uscite_tts[n], LV)
#     text_to_speach = gTTS(str_to_tts, lang='it')
#     audio_name = "LV" + str(LV) + "_u" + str(n + 1) + ".mp3"
#     text_to_speach.save(audio_name)

############################################################################

# OBTAIN THE CORRECT ANSWERS FOR EACH TRIALS ################################
answers = []

for n in range(N_TRIALS):
    ans_temp = []
    tot_ent = np.sum(entrate_tts[n])
    tot_usc = np.sum(uscite_tts[n])
    if tot_ent > tot_usc:
        ans_temp.append(1)
    else:
        ans_temp.append(0)

    index_a = np.where(entrate_tts[n] == np.amax(entrate_tts[n]))
    index_b = np.where(uscite_tts[n] == np.amax(uscite_tts[n]))

    ans_temp.append(int(index_a[0]) + 1)
    ans_temp.append(int(index_b[0]) + 1)

    answers.append(ans_temp)
############################################################################################

# CORRECT THE VALUES FOR PADDRAW ###########################################################
entrate_pad = N_ROWS - entrate
uscite_pad = N_ROWS - uscite
###########################################################################################

# STRING PARAMETERS
start_col = 0
start_row = 11
taxels = 1

str_to_flip = pt.flip_vert()

entrate_str = []
uscite_str = []


# GENERATE THE STRINGS FOR PADDRAW ########################################################
for n in range(N_TRIALS):

    str_en = ""
    str_us = ""
    for i in range(sequence_length):
        string_en = pt.draw_vert_line(start_col, start_row, int(entrate_pad[n][i]), taxels)
        str_en += string_en
        string_us = pt.draw_vert_line(start_col, start_row, int(uscite_pad[n][i]), taxels)
        str_us += string_us
        start_col += 1

    entrate_str.append(str_en)
    str_us += str_to_flip
    uscite_str.append(str_us)
    start_col = 0
###########################################################################################

# SAVE ON FILE SEQUENCES AND ANSWERS #################

str_to_dump = {'e1': entrate_str[0],
               'e2': entrate_str[1],
               'e3': entrate_str[2],
               'e4': entrate_str[3],
               'e5': entrate_str[4],
               'u1': uscite_str[0],
               'u2': uscite_str[1],
               'u3': uscite_str[2],
               'u4': uscite_str[3],
               'u5': uscite_str[4]}

filename = "LV" + str(LV) + ".txt"

# WRITE TO FILE AS A JSON MSG
with open(filename, 'w') as json_file:
    json.dump(str_to_dump, json_file)


# convert to list
entrate_tts = entrate_tts.tolist()
uscite_tts = uscite_tts.tolist()

tts_to_dump = {'e1': entrate_tts[0],
               'e2': entrate_tts[1],
               'e3': entrate_tts[2],
               'e4': entrate_tts[3],
               'e5': entrate_tts[4],
               'u1': uscite_tts[0],
               'u2': uscite_tts[1],
               'u3': uscite_tts[2],
               'u4': uscite_tts[3],
               'u5': uscite_tts[4]}

filename = "LV" + str(LV) + "_tts.txt"

# WRITE TO FILE AS A JSON MSG
with open(filename, 'w') as json_file:
    json.dump(tts_to_dump, json_file)

ans_to_dump = {'1': answers[0],
               '2': answers[1],
               '3': answers[2],
               '4': answers[3],
               '5': answers[4]}

filename_ans = "LV" + str(LV) + "_ans.txt"

with open(filename_ans, 'w') as json_file_ans:
    json.dump(ans_to_dump, json_file_ans)

##########################################################################