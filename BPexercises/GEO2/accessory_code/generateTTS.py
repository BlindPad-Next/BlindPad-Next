# def speak(text, lang='it'):
#     """Text to speech. For fun."""
#     try:
#         from gtts import gTTS
#         from pygame import mixer
#         from tempfile import TemporaryFile
#
#         tts = gTTS(text=text, lang=lang)
#         mixer.init()
#
#         sf = TemporaryFile(suffix='.ogg')
#         tts.write_to_fp(sf)
#         sf.seek(0)
#         mixer.music.load(sf)
#         mixer.music.play()
#     except Exception:
#         raise

from gtts import gTTS
from BPexercises.Common import TTS as tts
import os

# annuncio_tact = "Adesso ti mostrerò un'altra immagine"
# annuncio_aud = "Adesso ti farò ascoltare un'altra sequenza"
# cambia = "Cambia colonna"
# cancella = "Cancella colonna"
# annulla = "Annulla, scelta"
# prima = "Prima colonna"
# ordinata = "Ecco la sequenza da te ordinata"
# completa = "Hai ordinato la sequenza"
# nessuna = "Nessuna scelta da annullare"

#
# tts1 = gTTS(annuncio_tact, lang='it')
# tts1.save('Annuncio_tact.mp3')
#
# tts4 = gTTS(annuncio_aud, lang='it')
# tts4.save('Annuncio_aud.mp3')
#
# tts2 = gTTS(cambia, lang='it')
# tts2.save('Cambia.mp3')
#
# tts3 = gTTS(cancella, lang= 'it')
# tts3.save('Cancella.mp3')
#
# tts5 = gTTS(annulla, lang='it')
# tts5.save("Annulla.mp3")

# tt6 = gTTS(prima, lang ='it')
# tt6.save("Prima.mp3")

# tt7 = gTTS(nessuna, lang ='it')
# tt7.save("Nessuna.mp3")

consegna_tatto = open("Consegna_Presentazione_Tattile_no_b.txt", "r")
tts_consegna_tatto = gTTS(consegna_tatto.read(), lang="it")
tts_consegna_tatto.save("Consegna_Tatto.mp3")

# consegna_acustico = open("Consegna_Presentazione_Acustica.txt", "r")
# tts_consegna_acustico = gTTS(consegna_acustico.read(), lang="it")
# tts_consegna_acustico.save("Consegna_Acustico.mp3")

consegna_FAM_1 = open("Consegna_FAM_no_b.txt", "r")
tts_consegna_FAM_1 = gTTS(consegna_FAM_1.read(), lang="it")
tts_consegna_FAM_1.save("Consegna_FAM.mp3")
#
# consegna_FAM_2 = open("Consegna_FAM_2.txt", "r")
# tts_consegna_FAM_2 = gTTS(consegna_FAM_2.read(), lang="it")
# tts_consegna_FAM_2.save("Consegna_FAM_2.mp3")
#
# consegna_FAM_3 = open("Consegna_FAM_3.txt", "r")
# tts_consegna_FAM_3 = gTTS(consegna_FAM_3.read(), lang="it")
# tts_consegna_FAM_3.save("Consegna_FAM_3.mp3")