"""
@class playSound
@author Angelo Raspagliesi, Alberto Inuggi, Luca Brayda
@copyright Istituto Italiano di Tecnologia (IIT) 2018
"""

from pygame import mixer
import os
import inspect

class PlaySound():

    """
    Base class used to play a audio file
    """

    path_audio_file = None
    id_channel = None

    def __init__(self):

        mixer.init()

    def playit(self, path_file, id_channel, loop=0):

        channel = mixer.Channel(id_channel)

        sound = mixer.Sound(path_file)
        channel.play(sound, loops=loop)

    def playit_wait(self, path_file, id_channel, loop=0):
        """
        It plays the file by using the pygame library and wait for its completion
        @param path_file: the path where the audio file is locate
        @param id_channel: the channel used
        """
        self.playit(path_file, id_channel, loop)
        while self.is_playing(id_channel):
            pass
        return


    def is_playing(self, id_channel):
        return mixer.Channel(id_channel).get_busy()

    def stopit(self, id_channel):
        mixer.Channel(id_channel).stop()
