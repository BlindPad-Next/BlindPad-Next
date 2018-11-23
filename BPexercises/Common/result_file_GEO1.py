#! /usr/bin/python3

"""
@class Results_file_GEO1
@author Angelo Raspagliesi, Alberto Inuggi, Luca Brayda
@copyright Istituto Italiano di Tecnologia (IIT) 2018
"""

from BPexercises.Common import utilities as utils
from BPexercises.Common.file import File
# from Common import logging as log


class Results_file_GEO1(File):
    """
    @class Results_file_GEO1
    class which manages the file to store the exploration data.
    """
    def __init__(self, username, path=u''):
        """
        @constructor
        opens the file to write the results data
        """
        try:
            filename = 'GEO1.txt'
            super().__init__(username, path, filename)

        except Exception as e:
            print(utils.get_exception_message(e))
            # log.exception(str(e))

    def get_heading(self):
        """
        @function get_heading
        The function return the string of the heading
        @return the string of the heading
        """
        try:
            heading = u'Trial n°' + self.sep + u'reactTime'
            return heading

        except Exception as e:
            print(utils.get_exception_message(e))
            # log.exception(str(e))


    def write_data_vector(self, data):
        """
        @function write_data
        Given an input data vector, it writes down the matrix
        """
        try:
            string = "%s" + self.sep
            for item in data:
                if isinstance(item, float):
                    item = format(item, '.4f')
                self.f.write(string % item)
            self.f.write(u'\n')

        except Exception as e:
            print(utils.get_exception_message(e))
            # log.exception(str(e))


    def log_data(self, results_data):
        """
        @function log_data
        It logs the entire matrix.
        @param exploration_data the vector of data vectors to write to file
        """
        try:
            self.f = open(self.filename, 'a')
            string = "%s" + self.sep
            for item in results_data:
                if isinstance(item, float):
                    item = format(item, '.4f')
                self.f.write(string % item)
            self.f.write(u'\n')
        except Exception as e:
            print(utils.get_exception_message(e))
            # log.exception(str(e))
