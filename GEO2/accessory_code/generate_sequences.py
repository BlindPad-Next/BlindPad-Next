import random
import numpy as np
import math
import json
from BPexercises.Common import primitives as pt
from BPexercises.Common import TTS as tts
from gtts import gTTS
from collections import Counter


# This script generates pseudorandom sequences for the GEO1 experiment

# BLINDPAD PARAMETERS
N_ROWS = 12
N_COLUMNS = 16

# EXPERIMENT PARAMETERS
LV = "FAM"
SEQ_LEN = [3, 6, 9, 12]
# PERC = [30, 30, 55, 55]


N_TRIALS = 3

for i in range(len(SEQ_LEN)):
    if i == LV - 1:
        sequence_length = SEQ_LEN[i]
        break
#
# entrate = np.zeros((N_TRIALS, sequence_length))
# uscite = np.zeros((N_TRIALS, sequence_length))

# COMBINATION PARAMETERS

# MAX = N_ROWS * 10

# GENERATE THE SEQUENCES ################################################

# ripetizioni = math.ceil((N_TRIALS * sequence_length) * perc/100)

# past_tact_num = []
# for n in range(N_TRIALS):
#     sequence = []
#     tact_sequence = []
#     for i in range(sequence_length):
#         num = random.randrange(1, MAX + 1)
#         if 1<= num <= 10:
#             tact_num = 1
#         elif 11<= num <= 20:
#             tact_num = 2
#         elif 21 <= num <= 30:
#             tact_num = 3
#         elif 31 <= num <= 40:
#             tact_num = 4
#         elif 41 <= num <= 50:
#             tact_num = 5
#         elif 51 <= num <= 60:
#             tact_num = 6
#         elif 61 <= num <= 70:
#             tact_num = 7
#         elif 71 <= num <= 80:
#             tact_num = 8
#         elif 81 <= num <= 90:
#             tact_num = 9
#         elif 91 <= num <= 100:
#             tact_num = 10
#         elif 101 <= num <= 110:
#             tact_num = 11
#         elif 111<= num <= 120:
#             tact_num = 12
#
#         tact_sequence.append(tact_num)
#         sequence.append(num)
#     string_to_print = "SEQUENCE:" + str(sequence) + "\n"
#     print(string_to_print)
#     string_to_print = "TACT SEQUENCE:" + str(tact_sequence) + "\n"
#     print(string_to_print)
#     occurrencies = Counter(tact_sequence)
#     print(occurrencies)
#####################################################################
if LV == "FAM":
    # 1
    SEQ1 = [34, 65, 5]
    TACT_SEQ1 = [4, 7, 1]
    ANS1 = [7, 4, 1]
    TACT_ANS1 = [65, 34, 5]
    trial_1 = {"seq": SEQ1,
               "tact_seq": TACT_SEQ1,
               "ans": ANS1,
               "tact_ans": TACT_ANS1}
    # 2
    SEQ2 = [84, 25, 56]
    TACT_SEQ2 = [9, 3, 6]
    ANS2 = [9, 6, 3]
    TACT_ANS2 = [84, 56, 25]
    trial_2 = {"seq": SEQ2,
               "tact_seq": TACT_SEQ2,
               "ans": ANS2,
               "tact_ans": TACT_ANS2}
    # 3
    SEQ3 = [43, 22, 75]
    TACT_SEQ3 = [5, 3, 8]
    ANS3 = [8, 5, 3]
    TACT_ANS3 = [75, 43, 22]
    trial_3 = {"seq": SEQ3,
               "tact_seq": TACT_SEQ3,
               "ans": ANS3,
               "tact_ans": TACT_ANS3}

    TRIALS = {"1": trial_1,
              "2": trial_2,
              "3": trial_3}




if LV == 1:
    # LIV_1

    # 1
    SEQ1 = [14, 77, 54]
    TACT_SEQ1 = [2, 8, 6]
    ANS1 = [8, 6, 2]
    TACT_ANS1 =[77,54,14]
    trial_1 = {"seq": SEQ1,
               "tact_seq": TACT_SEQ1,
               "ans": ANS1,
               "tact_ans": TACT_ANS1}
    # 2
    SEQ2 = [41, 67, 34]
    TACT_SEQ2 = [5, 7, 4]
    ANS2 = [7,5,4]
    TACT_ANS2 =[67,41,34]
    trial_2 = {"seq": SEQ2,
               "tact_seq": TACT_SEQ2,
               "ans": ANS2,
               "tact_ans": TACT_ANS2}
    # 3
    SEQ3 = [13, 87, 26]
    TACT_SEQ3 = [1, 9, 3]
    ANS3 = [9,3,1]
    TACT_ANS3 = [87,26,13]
    trial_3 = {"seq": SEQ3,
               "tact_seq": TACT_SEQ3,
               "ans": ANS3,
               "tact_ans": TACT_ANS3}

    TRIALS = {"1": trial_1,
              "2": trial_2,
              "3": trial_3}
elif LV == 2:
    # LIV_2

    # 1
    SEQ1 = [8, 113, 64, 22, 33, 16]
    TACT_SEQ1 = [1, 12, 7, 3, 4, 2]
    ANS1 = [12,7,4,3,2,1]
    TACT_ANS1 = [113,64,33,22,16,8]
    trial_1 = {"seq": SEQ1,
               "tact_seq": TACT_SEQ1,
               "ans": ANS1,
               "tact_ans": TACT_ANS1}
    # 2
    SEQ2 = [52, 115, 101, 12, 46, 94]
    TACT_SEQ2 = [6, 12, 11, 2, 5, 10]
    ANS2 = [12,11,10,6,5,2]
    TACT_ANS2 =[115,101,94,52,46,12]
    trial_2 = {"seq": SEQ2,
               "tact_seq": TACT_SEQ2,
               "ans": ANS2,
               "tact_ans": TACT_ANS2}

    # 3
    SEQ3 = [98, 32, 68, 49, 10, 21]
    TACT_SEQ3 = [10, 4, 7, 5, 1, 3]
    ANS3 = [10,7,5,4,3,1]
    TACT_ANS3 = [98,68,49,32,21,10]
    trial_3 = {"seq": SEQ3,
               "tact_seq": TACT_SEQ3,
               "ans": ANS3,
               "tact_ans": TACT_ANS3}

    TRIALS = {"1": trial_1,
              "2": trial_2,
              "3": trial_3}
elif LV == 3:

    # LIV 3

    # 1
    SEQ1 = [18, 69, 7, 110, 78, 47, 50, 55, 32]
    TACT_SEQ1 = [2, 7, 1, 11, 8, 5, 5, 6, 4]
    ANS1 = [11,8,7,6,5,5,4,2,1]
    TACT_ANS1 = [110,78,69,55,50,47,32,18,7]
    trial_1 = {"seq": SEQ1,
               "tact_seq": TACT_SEQ1,
               "ans": ANS1,
               "tact_ans": TACT_ANS1}
    # 2
    SEQ2 = [75, 69, 72, 78, 20, 84, 119, 7, 24]
    TACT_SEQ2 = [8, 7, 8, 8, 2, 9, 12, 1, 3]
    ANS2 = [12,9,8,8,8,7,3,2,1]
    TACT_ANS2 =[119,84,78,75,72,69,24,20,7]
    trial_2 = {"seq": SEQ2,
               "tact_seq": TACT_SEQ2,
               "ans": ANS2,
               "tact_ans": TACT_ANS2}

    # 3
    SEQ3 = [87, 109, 64, 69, 70, 94, 14, 119, 80]
    TACT_SEQ3 = [9, 11, 7, 7, 7, 10, 2, 12, 8]
    ANS3 = [12,11,10,9,8,7,7,7,2]
    TACT_ANS3 = [119,109,94,87,80,70,69,64,14]
    trial_3 = {"seq": SEQ3,
               "tact_seq": TACT_SEQ3,
               "ans": ANS3,
               "tact_ans": TACT_ANS3}

    TRIALS = {"1": trial_1,
              "2": trial_2,
              "3": trial_3}
elif LV == 4:
    # LIV 4

    # 1
    SEQ1 = [11, 78, 117, 97, 66, 31, 83, 109, 22, 57, 24, 98]
    TACT_SEQ1 = [2, 8, 12, 10, 7, 4, 9, 11, 3, 6, 3, 10]
    ANS1 = [12,11,10,10,9,8,7,6,4,3,3,2]
    TACT_ANS1 = [117,109,98,97,83,78,66,57,32,24,22,11]
    trial_1 = {"seq": SEQ1,
               "tact_seq": TACT_SEQ1,
               "ans": ANS1,
               "tact_ans": TACT_ANS1}

    # 2
    SEQ2 = [96, 80, 94, 10, 106, 113, 31, 92, 46, 87, 14, 59]
    TACT_SEQ2 = [10, 8, 10, 1, 11, 12, 4, 10, 5, 9, 2, 6]
    ANS2 = [12,11,10,10,10,9,8,6,5,4,2,1]
    TACT_ANS2 = [113,106,96,94,92,87,80,59,46,32,14,10]
    trial_2 = {"seq": SEQ2,
               "tact_seq": TACT_SEQ2,
               "ans": ANS2,
               "tact_ans": TACT_ANS2}

    # 3
    SEQ3 = [92, 88, 64, 111, 119, 48, 120, 22, 104, 98, 33, 15]
    TACT_SEQ3 = [10, 9, 7, 12, 12, 5, 12, 3, 11, 10, 4, 2]
    ANS3 = [12,12,12,11,10,10,9,7,5,4,3,2]
    TACT_ANS3 =[120,119,111,104,98,92,88,64,48,33,22,15]
    trial_3 = {"seq": SEQ3,
               "tact_seq": TACT_SEQ3,
               "ans": ANS3,
               "tact_ans": TACT_ANS3}

    TRIALS = {"1": trial_1,
              "2": trial_2,
              "3": trial_3}



########################################### STRINGS FOR PADDRAW ###########################################

# STRING PARAMETERS

start_row = 11
taxels = 1
start_col = 0
tag = "L"

seq_for_paddraw = {}
for i in range(N_TRIALS):
    str_en = ""
    couple = i + 1
    key = str(couple)
    curr_inc = N_ROWS - np.array(TRIALS[key]["tact_seq"])


    for j in range(sequence_length):
        current_tag = tag + "{0:0=2d}".format(j + 1)
        if curr_inc[j] == 12:
            pass
        else:
            string_en = pt.draw_vert_line(start_col, start_row, int(curr_inc[j]), taxels, current_tag)
            str_en += string_en


        start_col += 1

    seq_for_paddraw[str(couple)]= str_en
    start_col = 0

pass

###########################################################################################################

########################################## SEQUENCES FOR ACOUSTIC #########################################

for i in range(N_TRIALS):
    couple = i + 1
    curr_inc = TRIALS[str(couple)]["seq"]
    inc_tts = ""
    # save mp3
    for j in range(sequence_length):
        inc_tts += str(curr_inc[j]) + ", "
    text_to_speech = gTTS(inc_tts, lang='it')
    audio_name = "LV" + str(LV) + "_" + str(couple) + ".mp3"
    text_to_speech.save(audio_name)

###########################################################################################################

# filename = "LV" + str(LV) + "ans.txt"
#
# with open(filename, "w") as json_file:
#     json.dump(TRIALS, json_file)