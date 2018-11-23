"""
@class playMusic
@author Angelo Raspagliesi, Alberto Inuggi, Luca Brayda
@copyright Istituto Italiano di Tecnologia (IIT) 2018
"""

from pygame import mixer
import os


class PlayMusic():
    """
    Base class used to play a audio file
    """

    path_audio_file = None

    def __init__(self):
        """
        Constructor
        It defines the path where the audio files should generally be located.
        """
        mixer.pre_init()
        # path_filename = os.path.realpath(__file__)
        # self.path_audio_file = os.path.dirname(path_filename)

        ##self.path_audio_file = os.path.dirname(path_filename) + '/' + language + '/'
        pass

    def playit(self, path_file, loop = 0):
        """
        It plays the file by using the pygame library
        @param path_file: the path where the audio file is locate
        """
        mixer.music.load(path_file)
        mixer.music.set_volume(0.5)
        mixer.music.play(loops=loop)

    def playit_wait(self, path_file, loop = 0):
        """
        It plays the file by using the pygame library and wait for its completion
        @param path_file: the path where the audio file is locate
        """
        self.playit(path_file, loop)
        while self.is_playing():
            pass
        return

    def is_playing(self):
        """
        @function is_playing
        Return true if the mixer is playing.
        """
        return mixer.music.get_busy()

    def stopit(self):#, path_file):
        """
        It stops the file by using the pygame library
        :param path_file: the path where the audio file is located.
        """
        # mixer.music.load(path_file)
        mixer.music.stop()

