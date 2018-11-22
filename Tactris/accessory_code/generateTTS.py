"""
@generateTTS
This script generates the audio files for Tactris
@author Angelo Raspagliesi, Alberto Inuggi, Luca Brayda
@copyright Istituto Italiano di Tecnologia (IIT) 2018
"""

from gtts import gTTS
#
# # MOVING STATE
# tts = gTTS("mosso a destra", lang='it')
# tts.save('destra.mp3')
#
# tts = gTTS("mosso a sinistra", lang='it')
# tts.save('sinistra.mp3')
#
# tts = gTTS("mosso in alto", lang='it')
# tts.save('alto.mp3')
#
# tts = gTTS("mosso in basso", lang='it')
# tts.save('basso.mp3')
#
# tts = gTTS("ruotato", lang='it')
# tts.save('ruota.mp3')
#
# tts = gTTS("alt, sei sul bordo", lang='it')
# tts.save('bordo.mp3')
#
# tts = gTTS("alt, stai toccando un'altra figura", lang='it')
# tts.save('contatto_figura.mp3')
#
# tts = gTTS("hai scelto la figura 1", lang='it')
# tts.save('scelta_0.mp3')
#
# tts = gTTS("hai scelto la figura 2", lang='it')
# tts.save('scelta_1.mp3')
#
# tts = gTTS("hai scelto la figura 3", lang='it')
# tts.save('scelta_2.mp3')
#
# tts = gTTS("figura posizionata", lang='it')
# tts.save('posizionata.mp3')

# tts = gTTS("to the right", lang='en')
# tts.save('destra_en.mp3')
#
# tts = gTTS("to the left", lang='en')
# tts.save('sinistra_en.mp3')
#
# tts = gTTS("rotated", lang='en')
# tts.save('ruota_en.mp3')
#
# tts = gTTS("alt, you're on the edge", lang='en')
# tts.save('bordo_en.mp3')
#
# tts = gTTS("figure placed", lang='en')
# tts.save('posizionata_en.mp3')

# # MOVING & SELECTING STATE
# tts = gTTS("ricomincia la stessa prova", lang='it')
# tts.save('ricomincia.mp3')
#
# # SELECTING STATE
# tts = gTTS("figura 1", lang='it')
# tts.save('fig0.mp3')
#
# tts = gTTS("figura 2", lang='it')
# tts.save('fig1.mp3')
#
# tts = gTTS("figura 3", lang='it')
# tts.save('fig2.mp3')
#
# tts = gTTS("muovi la figura", lang='it')
# tts.save('muovi.mp3')
#
tts = gTTS("move the figure", lang='en')
tts.save('muovi_en.mp3')
#
# tts = gTTS("Esplora i tratti e scegli quello giusto", lang='it')
# tts.save('start.mp3')
#
# tts = gTTS("Hai completato questa prova, passa ad una nuova figura", lang='it')
# tts.save('fine_trial.mp3')
#
# tts = gTTS("Se confermi la scelta, premi F, altrimenti premi A", lang='it')
# tts.save('03_conferma_scelta_but.mp3')
#
# tts = gTTS("Se confermi la scelta, fai un doppio tocco, altrimenti fai un tocco lungo", lang='it')
# tts.save('03_conferma_scelta_gest.mp3')
#
# tts = gTTS("Bravo, hai finito l'esercizio. Grazie di aver partecipato", lang='it')
# tts.save('esperimento_finito.mp3')
#
# # TEXT FILES
# start_but = open("01_start_but.txt", "r")
# tts_start_but = gTTS(start_but.read(), lang="it")
# tts_start_but.save("01_start_but.mp3")
#
# start_gest = open("01_start_gest.txt", "r")
# tts_start_gest = gTTS(start_gest.read(), lang="it")
# tts_start_gest.save("01_start_gest.mp3")
#
# consegna_moving_but_0 = open("02_consegna_moving_but_0.txt", "r")
# tts_consegna_moving_but_0 = gTTS(consegna_moving_but_0.read(), lang="it")
# tts_consegna_moving_but_0.save("02_consegna_moving_but_0.mp3")
#
# consegna_moving_but_1 = open("02_consegna_moving_but_1.txt", "r")
# tts_consegna_moving_but_1 = gTTS(consegna_moving_but_1.read(), lang="it")
# tts_consegna_moving_but_1.save("02_consegna_moving_but_1.mp3")
#
# consegna_moving_gest_0 = open("02_consegna_moving_gest_0.txt", "r")
# tts_consegna_moving_gest_0 = gTTS(consegna_moving_gest_0.read(), lang="it")
# tts_consegna_moving_gest_0.save("02_consegna_moving_gest_0.mp3")
#
# consegna_moving_gest_1 = open("02_consegna_moving_gest_1.txt", "r")
# tts_consegna_moving_gest_1 = gTTS(consegna_moving_gest_1.read(), lang="it")
# tts_consegna_moving_gest_1.save("02_consegna_moving_gest_1.mp3")
#
# consegna_conferma_scelta_but = open("03_consegna_conferma_scelta_but.txt", "r")
# tts_consegna_conferma_scelta_but = gTTS(consegna_conferma_scelta_but.read(), lang="it")
# tts_consegna_conferma_scelta_but.save("03_consegna_conferma_scelta_but.mp3")
#
# consegna_conferma_scelta_gest = open("03_consegna_conferma_scelta_gest.txt", "r")
# tts_consegna_conferma_scelta_gest = gTTS(consegna_conferma_scelta_gest.read(), lang="it")
# tts_consegna_conferma_scelta_gest.save("03_consegna_conferma_scelta_gest.mp3")
