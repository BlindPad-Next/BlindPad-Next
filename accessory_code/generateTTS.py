"""
@generateTTS
This script generates the audio files for the GEO1 experiment
@author Angelo Raspagliesi, Alberto Inuggi, Luca Brayda
@copyright Istituto Italiano di Tecnologia (IIT) 2018
"""

from gtts import gTTS
from BPexercises.Common import TTS as tts
import os

# domanda1 = tts.question_en('1')
# domanda2 = tts.question_en('2')
# domanda3 = tts.question_en('3')
# #
# tts1 = gTTS(domanda1)
# tts1.save('Domanda1_en.mp3')
# tts2 = gTTS(domanda2)
# tts2.save('Domanda2_en.mp3')
# tts3 = gTTS(domanda3)
# tts3.save('Domanda3_en.mp3')


# consegna_tatto = open("Consegna_Presentazione_Tattile.txt", "r")
# tts_consegna_tatto = gTTS(consegna_tatto.read(), lang="it")
# tts_consegna_tatto.save("Consegna_Tatto.mp3")

# consegna_acustico = open("Consegna_Presentazione_Acustica.txt", "r")
# tts_consegna_acustico = gTTS(consegna_acustico.read(), lang="it")
# tts_consegna_acustico.save("Consegna_Acustico.mp3")
#
# consegna_FAM_1 = open("Consegna_FAM_1.txt", "r")
# tts_consegna_FAM_1 = gTTS(consegna_FAM_1.read(), lang="it")
# tts_consegna_FAM_1.save("Consegna_FAM_1.mp3")
#
# consegna_FAM_2 = open("Consegna_FAM_2.txt", "r")
# tts_consegna_FAM_2 = gTTS(consegna_FAM_2.read(), lang="it")
# tts_consegna_FAM_2.save("Consegna_FAM_2.mp3")

# consegna_FAM_3 = open("Consegna_FAM_3.txt", "r")
# tts_consegna_FAM_3 = gTTS(consegna_FAM_3.read(), lang="it")
# tts_consegna_FAM_3.save("Consegna_FAM_3.mp3")

# tts_risposta = gTTS("Hai dato la tua risposta", lang="it")
# tts_risposta.save("Risposta.mp3")
#
# tts_entrate = gTTS("Entrate mensili", lang="it")
# tts_entrate.save("Entrate.mp3")
#
# tts_uscite = gTTS("Uscite mensili", lang="it")
# tts_uscite.save("Uscite.mp3")
#
# tts_cambia = gTTS("Cambia immagine", lang="it")
# tts_cambia.save("Cambia.mp3")
#
# tts_tocca = gTTS("Tocca immagine", lang="it")
# tts_tocca.save("Percepisci.mp3")

tts_risposta = gTTS("You gave, your answer. Step to the next trial.")
tts_risposta.save("Risposta_en.mp3")

# tts_entrate = gTTS("Monthly income")
# tts_entrate.save("Entrate_en.mp3")
#
# tts_uscite = gTTS("Monthly outcome")
# tts_uscite.save("Uscite_en.mp3")
#
# tts_cambia = gTTS("Switch image")
# tts_cambia.save("Cambia_en.mp3")
#
# tts_tocca = gTTS("Touch image")
# tts_tocca.save("Percepisci_en.mp3")
