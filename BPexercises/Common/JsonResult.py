#! /usr/bin/python3

"""
@class JsonResult
@author Alberto Inuggi, Angelo Raspagliesi, Luca Brayda
@copyright Istituto Italiano di Tecnologia (IIT) 2018
"""

import json
import os

from BPexercises.Common import utilities as utils
import datetime
# from Common import logging as log


class JsonResult:
    """
    @class JsonResult
    class which manages the file to store the experiment resuls as json file.
    """
    def __init__(self, username, path=u''):
        """
        @constructor
        opens the file to write the results data
        """
        try:
            filename = '.json'
            date_time = datetime.datetime.now()
            path = utils.strip_last_character(path, '\\')
            # path = utils.strip_last_character(path, '\/')
            date_time_str = date_time.strftime('%Y-%m-%d')

            if path != "":
                path = path + u'\\'

            self.filename = path + username + '_' + date_time_str + filename
            if os.path.isfile(self.filename):
                open(self.filename, mode='a')
            else:
                with open(self.filename, mode='w') as f:
                    f.write(json.dumps({"results": []}))

        except Exception as e:
            print(utils.get_exception_message(e))
            # log.exception(str(e))

    def write_data_vector(self, data):
        """
        @function write_data
        Given an input data, it reads the existing json content, append the new entry
        and write down the whole new dataset
        """
        try:

            with open(self.filename) as feedsjson:
                feeds = json.load(feedsjson)

            feeds['results'].append(data)
            with open(self.filename, mode='w') as f:
                f.write(json.dumps(feeds, indent=2))

        except Exception as e:
            print(utils.get_exception_message(e))
            # log.exception(str(e))

    def log_data(self, results_data):
        """
        @function log_data
        It logs the entire matrix.
        @param results_data the vector of data vectors to write to file
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

    def get_heading(self):
        pass
