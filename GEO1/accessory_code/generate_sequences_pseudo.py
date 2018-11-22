"""
@generate_sequences_pseudo
This script generates PSEUDORANDOM sequences for the GEO1 experiment
@author Angelo Raspagliesi, Alberto Inuggi, Luca Brayda
@copyright Istituto Italiano di Tecnologia (IIT) 2018
"""

import random
import numpy as np
import math
import json
from BPexercises.Common import primitives as pt
from BPexercises.Common import TTS as tts
from gtts import gTTS


# BLINDPAD PARAMETERS
N_ROWS = 12
N_COLUMNS = 16

# EXPERIMENT PARAMETERS
LV = 3  # LV1 ok non rigenerare
SEQ_LEN = [2, 4, 6, 12]

N_TRIALS = 5

for i in range(len(SEQ_LEN)):
    if i == LV - 1:
        sequence_length = SEQ_LEN[i]
        break
#
# entrate = np.zeros((N_TRIALS, sequence_length))
# uscite = np.zeros((N_TRIALS, sequence_length))

# COMBINATION PARAMETERS

MAX = N_ROWS - 2
perc = 0

# GENERATE THE SEQUENCES (LV 1 - 2) ################################################
# for n in range(N_TRIALS):
#     a = random.randrange(1, MAX + 1)
#     b = random.randrange(1, MAX + 1)
#     c = random.randrange(1, MAX + 1)
#     d = random.randrange(1, MAX + 1)
#     total = a + b
#     diff = math.ceil(total * perc/100)
#     string_to_print = "A:" + str(a) + \
#                       " B: " + str(b) + \
#                       " C: " + str(c) + \
#                       " D: " + str(d) + \
#                       " TOT: " + str(total) + " PERC: " + str(perc) + " DIFF: " + str(diff)
#     print(string_to_print)
#     perc += 20
#####################################################################

# GENERATE THE SEQUENCES (LV 3 - 4)################################################
# for n in range(N_TRIALS):
#     total = 0
#     sequence = []
#     for i in range(sequence_length):
#         num = random.randrange(1, MAX + 1)
#         total += num
#         sequence.append(num)
#     diff = math.ceil(total * perc/100)
#
#     string_to_print = "SEQUENCE:" + str(sequence) + " TOT: " + str(total) + " PERC: " + str(perc) + " DIFF: " + str(diff)
#     print(string_to_print)
#     perc += 20
#####################################################################

########################################## SEQUENCES FOR TACTILE #######################################################

### FAM ###

# couple_lv_1 = {"e1": [8, 5], "u1": [2, 3],
#                "e2": [4, 7], "u2": [5, 5],
#                "e3": [2, 5], "u3": [10, 6],
#                "e4": [2, 4], "u4": [9, 8],
#                "e5": [5, 8], "u5": [1, 2]}

### LV 1 ###
# 1) t1 - s1
# 2) t2 - s2
# 3) s3 - t3
# 4) s4 - t4
# 5) t5 - s5
couple_lv_1 = {"e1": [3, 6], "u1": [5, 4],
               "e2": [9, 5], "u2": [4, 7],
               "e3": [3, 6], "u3": [7, 9],
               "e4": [2, 4], "u4": [9, 8],
               "e5": [5, 8], "u5": [1, 2]}

### LV 2 ###
# 6) s1 - t1
# 7) s2 - t2
# 8) t3 - s3
# 9) t4 - s4
# 10) s5 - t5
couple_lv_2 = {"e1": [4, 6, 7, 6], "u1": [1, 10, 4, 5],
               "e2": [2, 4, 6, 4], "u2": [5, 2, 8, 3],
               "e3": [6, 4, 2, 1], "u3": [2, 1, 2, 4],
               "e4": [4, 7, 6, 8], "u4": [6, 5, 2, 4],
               "e5": [4, 2, 5, 8], "u5": [9, 6, 10, 8]}

### LV 3 ###
# 11) t1 - s1
# 12) t2 - s2
# 13) t3 - s3
# 14) s4 - t4
# 15) s5 - t5
couple_lv_3 = {"e1": [2, 1, 3, 4, 2, 6], "u1": [2, 3, 3, 3, 3, 4],
               "e2": [9, 6, 7, 7, 3, 2], "u2": [7, 4, 4, 3, 4, 5],
               "e3": [9, 10, 4, 6, 8, 9], "u3": [3, 4, 2, 5, 4, 7],
               "e4": [2, 4, 1, 1, 0, 3], "u4": [7, 7, 8, 4, 3, 5],
               "e5": [1, 1, 1, 1, 1, 0], "u5": [3, 1, 8, 10, 2, 3]}

### LV 4 ###
# 16) s1 - t1
# 17) t2 - s2
# 18) s3 - t3
# 19) t4 - s4
# 20) s5 - t5
couple_lv_4 = {"e1": [2, 3, 9, 4, 7, 3, 7, 1, 3, 5, 3, 4], "u1": [2, 3, 3, 2, 9, 3, 4, 1, 4, 5, 8, 7],
               "e2": [10, 7, 1, 5, 5, 8, 3, 8, 4, 6, 5, 2], "u2": [1, 5, 8, 2, 6, 4, 3, 4, 5, 6, 4, 3],
               "e3": [4, 6, 4, 5, 7, 4, 1, 5, 4, 2, 4, 3], "u3": [4, 9, 7, 9, 6, 6, 8, 3, 6, 8, 7, 10],
               "e4": [1, 4, 8, 7, 9, 2, 8, 2, 3, 3, 10, 9], "u4": [1, 1, 2, 4, 0, 6, 2, 3, 2, 1, 2, 2],
               "e5": [1, 1, 2, 2, 1, 1, 1, 0, 3, 1, 2, 1], "u5": [7, 6, 6, 9, 10, 8, 9, 7, 5, 3, 5, 9]}

########################################################################################################################


########################################## SEQUENCES FOR ACOUSTIC #######################################################

### LV 1 ###
# LV = 1
# entrate_tts_lv_1 = {}
# uscite_tts_lv_1 = {}
# for i in range(N_TRIALS):
#     couple = i + 1
#     key_inc = "e" + str(couple)
#     key_out = "u" + str(couple)
#     curr_inc = np.array(couple_lv_1[key_inc])
#     curr_out = np.array(couple_lv_1[key_out])
#     # complemento a 10
#     curr_inc_ac = (10 - curr_inc) * 10
#     curr_out_ac = (10 - curr_out) * 10
#     # save mp3
#     inc_tts = tts.entrate(curr_inc_ac, LV)
#     text_to_speech = gTTS(inc_tts, lang='it')
#     audio_name = "LV" + str(LV) + "_e" + str(couple) + ".mp3"
#     text_to_speech.save(audio_name)
#
#     out_tts = tts.uscite(curr_out_ac, LV)
#     text_to_speech = gTTS(out_tts, lang='it')
#     audio_name = "LV" + str(LV) + "_u" + str(couple) + ".mp3"
#     text_to_speech.save(audio_name)
#
#     entrate_tts_lv_1[key_inc] = curr_inc_ac.tolist()
#     uscite_tts_lv_1[key_out] = curr_out_ac.tolist()
#
# ### LV 2 ###
# LV = 2
# entrate_tts_lv_2 = {}
# uscite_tts_lv_2 = {}
# for i in range(N_TRIALS):
#     couple = i + 1
#     key_inc = "e" + str(couple)
#     key_out = "u" + str(couple)
#     curr_inc = np.array(couple_lv_2[key_inc])
#     curr_out = np.array(couple_lv_2[key_out])
#     # complemento a 10
#     curr_inc_ac = (10 - curr_inc) * 10
#     curr_out_ac = (10 - curr_out) * 10
#     # save mp3
#     inc_tts = tts.entrate(curr_inc_ac, LV)
#     text_to_speech = gTTS(inc_tts, lang='it')
#     audio_name = "LV" + str(LV) + "_e" + str(couple) + ".mp3"
#     text_to_speech.save(audio_name)
#
#     out_tts = tts.uscite(curr_out_ac, LV)
#     text_to_speech = gTTS(out_tts, lang='it')
#     audio_name = "LV" + str(LV) + "_u" + str(couple) + ".mp3"
#     text_to_speech.save(audio_name)
#     entrate_tts_lv_2[key_inc] = curr_inc_ac.tolist()
#     uscite_tts_lv_2[key_out] = curr_out_ac.tolist()
#
# ### LV 3 ###
LV = 3
entrate_tts_lv_3 = {}
uscite_tts_lv_3 = {}
for i in range(N_TRIALS):
    couple = i + 1
    key_inc = "e" + str(couple)
    key_out = "u" + str(couple)
    curr_inc = np.array(couple_lv_3[key_inc])
    curr_out = np.array(couple_lv_3[key_out])
    # complemento a 10
    curr_inc_ac = (10 - curr_inc) * 10
    curr_out_ac = (10 - curr_out) * 10
    # save mp3
    inc_tts = tts.entrate_en(curr_inc_ac, LV)
    text_to_speech = gTTS(inc_tts)
    audio_name = "LV" + str(LV) + "_e" + str(couple) + "_en.mp3"
    text_to_speech.save(audio_name)

    out_tts = tts.uscite_en(curr_out_ac, LV)
    text_to_speech = gTTS(out_tts)
    audio_name = "LV" + str(LV) + "_u" + str(couple) + "_en.mp3"
    text_to_speech.save(audio_name)
    entrate_tts_lv_3[key_inc] = curr_inc_ac.tolist()
    uscite_tts_lv_3[key_out] = curr_out_ac.tolist()
#
# ### LV 4 ###
# LV = 4
# entrate_tts_lv_4 = {}
# uscite_tts_lv_4 = {}
# for i in range(N_TRIALS):
#     couple = i + 1
#     key_inc = "e" + str(couple)
#     key_out = "u" + str(couple)
#     curr_inc = np.array(couple_lv_4[key_inc])
#     curr_out = np.array(couple_lv_4[key_out])
#     # complemento a 10
#     curr_inc_ac = (10 - curr_inc) * 10
#     curr_out_ac = (10 - curr_out) * 10
#     # save mp3
#     inc_tts = tts.entrate(curr_inc_ac, LV)
#     text_to_speech = gTTS(inc_tts, lang='it')
#     audio_name = "LV" + str(LV) + "_e" + str(couple) + ".mp3"
#     text_to_speech.save(audio_name)
#
#     out_tts = tts.uscite(curr_out_ac, LV)
#     text_to_speech = gTTS(out_tts, lang='it')
#     audio_name = "LV" + str(LV) + "_u" + str(couple) + ".mp3"
#     text_to_speech.save(audio_name)
#     entrate_tts_lv_4[key_inc] = curr_inc_ac.tolist()
#     uscite_tts_lv_4[key_out] = curr_out_ac.tolist()

########################################################################################################################

########################################### STRINGS FOR PADDRAW ########################################################


# # STRING PARAMETERS
#
# start_row = 11
# taxels = 1
#
# str_to_flip = pt.flip_vert()
#
# ### LV 1 ###
# start_col = 0
# sequence_length = 2
# entrate_str_lv_1 = {}
# uscite_str_lv_1 = {}
#
# for i in range(N_TRIALS):
#     str_en = ""
#     str_us = ""
#     couple = i + 1
#     key_inc = "e" + str(couple)
#     key_out = "u" + str(couple)
#     curr_inc = N_ROWS - np.array(couple_lv_1[key_inc])
#     curr_out = N_ROWS - np.array(couple_lv_1[key_out])
#
#     for j in range(sequence_length):
#
#         if curr_inc[j] == 12:
#             pass
#         else:
#             string_en = pt.draw_vert_line(start_col, start_row, int(curr_inc[j]), taxels)
#             str_en += string_en
#         if curr_out[j] == 12:
#             pass
#         else:
#             string_us = pt.draw_vert_line(start_col, start_row, int(curr_out[j]), taxels)
#             str_us += string_us
#
#         start_col += 1
#
#     entrate_str_lv_1[key_inc] = str_en
#     str_us += str_to_flip
#     uscite_str_lv_1[key_out] = str_us
#     start_col = 0
#
# ### LV 2 ###
# start_col = 0
# sequence_length = 4
# entrate_str_lv_2 = {}
# uscite_str_lv_2 = {}
#
# for i in range(N_TRIALS):
#     str_en = ""
#     str_us = ""
#     couple = i + 1
#     key_inc = "e" + str(couple)
#     key_out = "u" + str(couple)
#     curr_inc = N_ROWS - np.array(couple_lv_2[key_inc])
#     curr_out = N_ROWS - np.array(couple_lv_2[key_out])
#
#
#     for j in range(sequence_length):
#         if curr_inc[j] == 12:
#             pass
#         else:
#             string_en = pt.draw_vert_line(start_col, start_row, int(curr_inc[j]), taxels)
#             str_en += string_en
#         if curr_out[j] == 12:
#             pass
#         else:
#             string_us = pt.draw_vert_line(start_col, start_row, int(curr_out[j]), taxels)
#             str_us += string_us
#         start_col += 1
#
#     entrate_str_lv_2[key_inc] = str_en
#     str_us += str_to_flip
#     uscite_str_lv_2[key_out] = str_us
#     start_col = 0
#
# ### LV 3 ###
# start_col = 0
# sequence_length = 6
# entrate_str_lv_3 = {}
# uscite_str_lv_3 = {}
#
# for i in range(N_TRIALS):
#     str_en = ""
#     str_us = ""
#     couple = i + 1
#     key_inc = "e" + str(couple)
#     key_out = "u" + str(couple)
#     curr_inc = N_ROWS - np.array(couple_lv_3[key_inc])
#     curr_out = N_ROWS - np.array(couple_lv_3[key_out])
#
#     for j in range(sequence_length):
#
#         if curr_inc[j] == 12:
#             pass
#         else:
#             string_en = pt.draw_vert_line(start_col, start_row, int(curr_inc[j]), taxels)
#             str_en += string_en
#         if curr_out[j] == 12:
#             pass
#         else:
#             string_us = pt.draw_vert_line(start_col, start_row, int(curr_out[j]), taxels)
#             str_us += string_us
#
#         start_col += 1
#
#     entrate_str_lv_3[key_inc] = str_en
#     str_us += str_to_flip
#     uscite_str_lv_3[key_out] = str_us
#     start_col = 0
#
# ### LV 4 ###
# start_col = 0
# sequence_length = 12
# entrate_str_lv_4 = {}
# uscite_str_lv_4 = {}
#
# for i in range(N_TRIALS):
#     str_en = ""
#     str_us = ""
#     couple = i + 1
#     key_inc = "e" + str(couple)
#     key_out = "u" + str(couple)
#     curr_inc = N_ROWS - np.array(couple_lv_4[key_inc])
#     curr_out = N_ROWS - np.array(couple_lv_4[key_out])
#
#     for j in range(sequence_length):
#         if curr_inc[j] == 12:
#             pass
#         else:
#             string_en = pt.draw_vert_line(start_col, start_row, int(curr_inc[j]), taxels)
#             str_en += string_en
#         if curr_out[j] == 12:
#             pass
#         else:
#             string_us = pt.draw_vert_line(start_col, start_row, int(curr_out[j]), taxels)
#             str_us += string_us
#
#         start_col += 1
#
#     entrate_str_lv_4[key_inc] = str_en
#     str_us += str_to_flip
#     uscite_str_lv_4[key_out] = str_us
#     start_col = 0

########################################################################################################################

######################################## SAVE SEQUENCES ON FILE ########################################################

# NUM_OF_LEVELS = 4
#
# ###### TACTILE
# for i in range(NUM_OF_LEVELS):
#     lv = i + 1
#     filename = "newLV" + str(lv) + ".txt"
#
#     # WRITE TO FILE AS A JSON MSG
#     with open(filename, 'w') as json_file:
#         if lv == 1:
#             json.dump(entrate_str_lv_1, json_file)
#         elif lv == 2:
#             json.dump(entrate_str_lv_2, json_file)
#         elif lv == 3:
#             json.dump(entrate_str_lv_3, json_file)
#         elif lv == 4:
#             json.dump(entrate_str_lv_4, json_file)
#
#     with open(filename, 'a') as json_file:
#         if lv == 1:
#             json.dump(uscite_str_lv_1, json_file)
#         elif lv == 2:
#             json.dump(uscite_str_lv_2, json_file)
#         elif lv == 3:
#             json.dump(uscite_str_lv_3, json_file)
#         elif lv == 4:
#             json.dump(uscite_str_lv_4, json_file)
#
# ###### ACOUSTIC
# for i in range(NUM_OF_LEVELS):
#     lv = i + 1
#     filename = "newLV" + str(lv) + "_tts.txt"
#
#     # WRITE TO FILE AS A JSON MSG
#     with open(filename, 'w') as json_file:
#         if lv == 1:
#             json.dump(entrate_tts_lv_1, json_file)
#         elif lv == 2:
#             json.dump(entrate_tts_lv_2, json_file)
#         elif lv == 3:
#             json.dump(entrate_tts_lv_3, json_file)
#         elif lv == 4:
#             json.dump(entrate_tts_lv_4, json_file)
#
#     with open(filename, 'a') as json_file:
#         if lv == 1:
#             json.dump(uscite_tts_lv_1, json_file)
#         elif lv == 2:
#             json.dump(uscite_tts_lv_2, json_file)
#         elif lv == 3:
#             json.dump(uscite_tts_lv_3, json_file)
#         elif lv == 4:
#             json.dump(uscite_tts_lv_4, json_file)


