#! /usr/bin/python3

"""
@class File
@author Angelo Raspagliesi, Alberto Inuggi, Luca Brayda
@copyright Istituto Italiano di Tecnologia (IIT) 2018
"""

import datetime
import os

# from Common import logging as log
from . import utilities as utils
# from __OT import constants as consts


class File:
    """
    @class File
    class which manages the file to store the experiment results.
    """
    f = None
    filename = None
    enable_heading = True
    sep = u'\t'  #consts.separation_character

    def __init__(self, username, path=u'', filename=u''):
        """
        @constructor
        opens the file to write the results data
        """
        try:
            date_time = datetime.datetime.now()

            path = utils.strip_last_character(path, '\\')
            # path = utils.strip_last_character(path, '\/')
            date_time_str = date_time.strftime('%Y-%m-%d')

            if path != "":
                path = path + u'\\'

            self.filename = path + username + '_' + date_time_str + '_' + filename
            if not os.path.exists(self.filename):
                self.open('w')
            else:
                self.open('a')

        except Exception as e:
            print(utils.get_exception_message(e))
            # log.exception(str(e))

    def open(self, mode):
        """
        @function open
        It opens the file
        """
        try:
            utils.create_folder_if_not_exists(self.filename)
            self.f = open(self.filename, mode)
        except Exception as e:
            print(utils.get_exception_message(e))
            # log.exception(str(e))

    def close(self):
        """
        @function close
        It closes the open file
        """
        try:
            self.f.close()

        except Exception as e:
            print(utils.get_exception_message(e))
            # log.exception(str(e))

    def write_heading(self):
        """
        @function write_heading
        The function writes down the heading of the exploration data to store
        """
        try:
            heading = self.get_heading()

            if self.enable_heading:
                self.f.write(heading)
                self.f.write(u'\n')
                self.close()

        except Exception as e:
            print(utils.get_exception_message(e))
            # log.exception(str(e))

    def get_heading(self):
        """
        @function get_heading
        To be implemented
        """
        raise NotImplementedError("Subclass must implement abstract method")

    # data is a dictionary
    def write_unknown_dictionary(self, data):
        """
        @function write_unknown_dictionary
        Given an input unknown dictionary, it writes down the matrix
        """
        try:
            string = "%s" + self.sep
            for item in data:
                if isinstance(data[item], float):
                    stritem = format(data[item], '.4f')
                elif isinstance(data[item], bool):
                    if data[item] is True:
                        stritem = "1"
                    else:
                        stritem = "0"
                else:
                    stritem = str(data[item])

                self.f.write(string % stritem)
            self.f.write(u'\n')

        except Exception as e:
            print(utils.get_exception_message(e))
            # log.exception(str(e))
