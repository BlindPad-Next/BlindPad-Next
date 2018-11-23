#! /usr/bin/python3
"""
@utilities
@author Alberto Inuggi, Angelo Raspagliesi, Luca Brayda
@copyright Istituto Italiano di Tecnologia (IIT) 2018
"""
import builtins as __builtin__
import datetime
import errno
import json
import os
import re
import sys
import time
import traceback
from functools import wraps

# import logging as log
# from __OT import constants as consts


# from Common.ldr import AnalogPlot



# termocolor need install termocolor package
# sudo apt-get install python3-termcolor (for python3.x)
# sudo apt-get install python-termcolor  (for python 2.x)
# usage : print(colored('hello', 'red'), colored('world', 'green'))


def get_exception_message(exc):
    """
    @function get_exception_message
    It gets the exception message and returns a
    colored printable message
    """
    #string = "Error: " + str(exc)  +  "\n" + get_debug_info()
    #return colored(string, 'red', attrs=['bold'])

    string = "Error: " + str(exc) + "\n" + get_debug_info()
    return json.dumps({"string": string})


def get_debug_info():
    """
    @function getDebugInfo
    This method returns the string with the information of what
    caused the exception to be raised.

    @return string the value with the debug info to write on the log file
    """
    string = ""
    for frame in traceback.extract_tb(sys.exc_info()[2]):

        file_name, line_no, function, text = frame

        if file_name is None:
            file_name = ''
        if line_no is None:
            line_no = ''
        if function is None:
            function = ''
        if text is None:
            text = ''

        string += " in file: " + str(file_name) + \
                  " line no: " + str(line_no) +  \
                  " function: " + function + \
                  " text: " + text + "\n"

    return string

def get_list_of_members(class_object):
    """
    @function get_list_of_members
    class_object the object of the class you want the members of
    """
    return [attr for attr in dir(class_object()) if not callable(getattr(class_object(), attr)) and not attr.startswith("__")]


def strip_last_character(string, character='\\'):
    """
    @function strip_last_character
    It removes the last character from the input string if the last character is
    the same as the one passed as input character.
    By default the input character is the \ backslash
    @param string the string to remove the character from
    @param character the character to remove from the input string
    @return the output string
    """
    try:
        return string.rstrip(character)

    except Exception as e:
        print(get_exception_message(e))
        # log.exception(str(e))

def create_folder_if_not_exists(path_file):
    """
    @function create_folder_if_not_exists
    The function checks if the folder exists, if it does not, it creates the missing file.
    @param path_file the path of the file which we need to create if it does not exist.
    """
    try:
        # create directory of not exist
        print(path_file)
        if not os.path.exists(os.path.dirname(path_file)):
            try:
                os.makedirs(os.path.dirname(path_file))
            except OSError as exc:  # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise Exception(u'Folder does not exists')
    except Exception as e:
        print(get_exception_message(e))
        # log.exception(str(e))



def print_json(string):
    """
    @function print_json
    this method takes a string as input and it creates a jon packet to send to
    the javascript counterpart to be printed.
    @param *args the arguments to send a json string
    """

    data = {}
    data['string'] = string
    # import json
    json_data = json.dumps(data)
    print(json_data)


def create_file(filename, header):
    """
    @function create_file
    :param filename:
    :param header:
    :return: f: file created
    """

    f = open(filename, "w")
    header_date = datetime.datetime.now()
    f.write(header_date.strftime("%Y-%m-%d %H:%M\n"))
    f.write(header + "\n")

    return f


def write_to_file_time(file, start_time, string):
    """
    @function write_to_file_time
    :param file:
    :param start_time:
    :param string:
    :return:
    """

    time_sample = round((time.time() - start_time), 3)
    if string is None or not string:
        string_to_write = str(time_sample) + "    " + "NaN,NaN,NaN\n"
    else:
        string_to_write = str(time_sample) + "    " + string  #+ "\n" la stringa ha già la newline

    file.write(string_to_write)

def write_to_file(file, string):

    if string is None or not string:
        string_to_write = "NaN\n"
    else:
        string_to_write = string  + "\n"  #la stringa ha già la newline

    file.write(string_to_write)


def purge(dir, pattern):
    """
    @function purge remove all file matching the pattern in the specified directory
    :param dir: the path of the directory in which are contained the files to be eliminated
    :param pattern: the pattern of the filename of the files to be eliminated
    """
    for f in os.listdir(dir):
        if re.search(pattern, f):
            os.remove(os.path.join(dir, f))


def init_log_files(app_path):
    pattern = "tamo3.log.{0,1}.{0,1}\d{0,2}"

    log_path = os.path.join(app_path, "log_file")
    if not os.path.exists(log_path):
        os.makedirs(log_path)

    # remove old log files
    purge(log_path, pattern)








