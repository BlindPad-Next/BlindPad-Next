import time
import json
import numpy as np
import random
from BPexercises.Common import TTS as tts

# EXPERIMENT PARAMETERS

with open("params.json") as json_file:
    params = json.load(json_file)


# OPEN FILE WITH SEQUENCES
file = "LV" + str(params["LV"]) + ".txt"
with open(file) as json_file:
    tact_imgs = json.load(json_file)

# OPEN FILE WITH SEQUENCES FOR TTS
tts_file = "LV" + str(params["LV"]) + "_tts.txt"
with open(tts_file) as json_file:
    tts_imgs = json.load(json_file)


# OPEN FILE WITH ANSWERS
ans_file = "LV" + str(params["LV"]) + "_ans.txt"
with open(ans_file) as json_file:
    answers = json.load(json_file)


# SHUFFLE TRIALS
trials = random.sample([1, 2, 3, 4, 5], params["N_TRIALS"])
entrate_tts = []
uscite_tts = []

# GENERATE STRING FOR TTS
for i in range(params["N_TRIALS"]):

    chosen = trials[i]
    key_entrate = "e" + str(chosen)
    key_uscite = "u" + str(chosen)
    entrate_tts.append(tts.entrate(tts_imgs[key_entrate], params["LV"]))
    uscite_tts.append(tts.uscite(tts_imgs[key_uscite], params["LV"]))


file = open("Consegna_Presentazione_Acustica.txt", "r")
# tts.speak(file.read())


for i in range(params["N_TRIALS"]):

    quest, string_quest = tts.rand_question()
    tts.speak(entrate_tts[i])
    time.sleep(2)
    tts.speak(uscite_tts[i])
    time.sleep(2)
    tts.speak(string_quest)

    # wait for user interaction and response











