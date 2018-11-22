"""
@primitives
This file contains all the commands or macros that it possible to send to Paddraw through the python scripts
@author Angelo Raspagliesi, Alberto Inuggi, Luca Brayda
@copyright Istituto Italiano di Tecnologia (IIT) 2018
"""

import numpy as np
import time

#******************************                   DRAWABLE COMPONENTS                   ******************************#

def draw_line(start_col, start_row, end_col, end_row, value, tag=""):
    """
    @function draw line:
    it creates a string in order to draw a line on PADDRAW
    :param start_col: between 0 and 15
    :param start_row: between 0 and 11
    :param end_col: between 0 and 15
    :param end_row: between 0 and 11
    :param value: 0 mean taxel down, 1 mean taxel up
    :param tag: string that identifies the object (only the following characters may be used [a-z], [A-Z], [0-9]
    :return: the string for paddraw
    """

    s = ","
    tag = '*' + tag
    seq = (str(start_col), str(start_row), str(end_col), str(end_row), str(value), tag)
    line = "line(" + s.join(seq) + ");"

    return line


def draw_horz_line(start_col, start_row, end_col, value, tag=""):

    end_row = start_row
    line = draw_line(start_col, start_row, end_col, end_row, value, tag)
    return line


def draw_vert_line(start_col, start_row, end_row, value, tag=""):

    end_col = start_col
    line = draw_line(start_col, start_row, end_col, end_row, value, tag)
    return line


def draw_rect(left, top, width, height, value, tag=""):
    """
    @function draw_rect:
    it creates a string in order to draw a rectangle on PADDRAW
    :param left: x value of the upper left point of the rectangle [0-15]
    :param top: y value of the upper left point of the rectangle [0-12]
    :param width: width of the rectangle (may be negative)
    :param height: height of the rectangle (may be negative)
    :param value: 0 mean taxel down, 1 mean taxel up
    :param tag: string that identifies the object (only the following characters may be used [a-z], [A-Z], [0-9]
    :return: the string for paddraw
    """

    s = ","
    tag = '*' + tag
    seq = (str(left), str(top), str(width), str(height), str(value), tag)
    rect = "rect(" + s.join(seq) + ");"

    return rect


def draw_circle(cX, cY, r, value, tag=""):
    """
    @function draw_circle:
    it creates a string in order to draw a circle on PADDRAW
    :param cX: x component of the center point
    :param cY: y component of the center point
    :param r: radius of the circle #TODO da controllare bene
    :param value: 0 mean taxel down, 1 mean taxel up
    :param tag: string that identifies the object (only the following characters may be used [a-z], [A-Z], [0-9]
    :return: the string for paddraw
    """

    s = ","
    tag = '*' + tag
    seq = (str(cX), str(cY), str(r), str(value), tag)
    circle = "circle(" + s.join(seq) + ");"

    return circle


def pen(pos_col, pos_row, tag=""):
    s = ','
    tag = '*' + tag
    seq = (str(pos_col), str(pos_row), tag)
    pen = "pen(" + s.join(seq) + ");"
    return pen


def fill(pos_col, pos_row, value, tag=""):
    s = ','
    tag = '*' + tag
    seq = (str(pos_col), str(pos_row), str(value), tag)
    string = "fill(" + s.join(seq) + ");"
    return string




#******************************                   EFFECT COMPONENTS                   ******************************#


def move(hor, vert, tag=""):
    """
    @function move:
    it moves the tactile maps on paddraw
    :param vert: positive integer moves the map down, negative integer moves the map up
    :param hor: positive integer moves the map to the right, negative int moves the map to the left
    :param tag: string that identifies the object (only the following characters may be used [a-z], [A-Z], [0-9]
    :return: the string for paddraw
    """
    s = ','
    tag = '*' + tag
    seq = (str(hor), str(vert), tag)
    string = "move(" + s.join(seq) + ");"
    time.sleep(0.5)
    return string


def rotate(deg, tag=""):
    """
    @function rotate:
    it rotate the tactile maps on paddraw
    :param deg: positive integer rotate in clockwise direction, negative integer rotate in counterclockwise direction
    :param tag: string that identifies the object (only the following characters may be used [a-z], [A-Z], [0-9]
    :return: the string for paddraw
    """

    s = ','
    tag = '*' + tag
    seq = (str(deg), tag)
    string = "rotate(" + s.join(seq) + ");"
    return string


def flip_vert(tag=""):

    tag = '*' + tag
    string = "flip_vert(" + tag + ");"
    return string


def flip_hor(tag=""):

    tag = '*' + tag
    string = "flip_hor(" + tag + ");"
    return string

# TODO the function should be accept a list of tags
def invert(*args):
    tags = [i for i in args]
    tag = str(tags)
    string = "invert(" + tag + ");"
    return string

#******************************                   OTHER COMPONENTS                   ******************************#


def erase(pos_col="", pos_row="", tag=""):

    s = ','
    tag = '*' + tag
    seq = (str(pos_col), str(pos_row), tag)
    string = "erase(" + s.join(seq) + ");"
    return string


def erase_point(figure):
    string = ""
    len_line = 0
    for i in range(len_line):
        curr_point_y = figure["start_row"] - i
        string += erase(figure["start_col"], curr_point_y)#, figure["tag"])

    return string


def erase_vert_line(figure):
    string = draw_vert_line(figure["start_col"], figure["start_row"], figure["end_row"], 0)
    return string


def clear():
    return "clear();"


# takes a ;-separated list of paddraw line() commands and transform to a [13,17] matrix
# to be used for a direct python=>blindpad BLE connection
def convert_lines_to_map(msg):
    """
    @function convert_lines_to_map
    takes a ;-separated list of paddraw line() commands and transform to a [13,17] matrix
    to be used for a direct python=>blindpad BLE connection
    :param msg: the list of paddraw line() commands
    :return: the [13,17] matrix
    """
    mymap = np.zeros((13, 17))
    cmd_list = msg.split(';')
    for c in range(len(cmd_list) - 1):

        strcmd = cmd_list[c][5:]
        arr_values = strcmd.split(",")
        for v in range(5):
            arr_values[v] = int(arr_values[v])

        positions = arr_values[0:4]
        value = arr_values[4]

        if positions[0] == positions[2]:
            # vertical
            if positions[1] > positions[3]:
                for r in range(positions[3], positions[1]+1, 1):
                    mymap[r + 1][positions[0] + 1] = value
            else:
                for r in range(positions[1], positions[3]+1, 1):
                    mymap[r + 1][positions[0] + 1] = value

        elif positions[1] == positions[3]:
            # horizontal
            if positions[0] > positions[2]:
                for c in range(positions[2], positions[0]+1, 1):
                    mymap[positions[1]][c + 1] = value
            else:
                for r in range(positions[1], positions[3]+1, 1):
                    mymap[positions[1]][c + 1] = value

        elif positions[1] == positions[3] and positions[0] == positions[2]:
            # point
            mymap[positions[1] + 1][positions[1] + 1] = value

    return mymap


def convert_map_to_pens(mymap):
    """
    @function convert_map_to_pens
    takes a [12,16] map and renders it through up-to-12 horizontal line commands toward PadDraw (uses cmd "pen")
    :param mymap: the [12,16] map
    :return: the entire code string
    """

    row = len(mymap)
    col = len(mymap[0])

    str_code = ""
    for r in range(row):
        for c in range(col):
            if mymap[r][c] > 0:
                str_code = str_code + "pen(" + str(c) + ", " + str(r) + ");"

    return str_code


def convert_map_to_horz_lines(mymap):
    """
    @function convert_map_to_hor_lines
    takes a [12,16] map and renders it through up-to-12 horizontal line commands toward PadDraw (uses cmd "line")
    faster than convert_map_to_pens when the map contain a large number of raised taxels
    :param mymap: the [12,16] map
    :return: the entire code string
    """

    mat = np.array(mymap)
    ones_indices = np.nonzero(mat)

    code = ""
    count = 0

    for i in range(0, mat.shape[0]):
        x = np.where(ones_indices[0] == i)
        cols = ones_indices[1][x]
        for j in range(len(cols)):
            try:
                if cols[j + 1] == cols[j] + 1:
                    count += 1
                else:
                    stop = cols[j]
                    start = cols[j] - count
                    count = 0
                    string = "line(" + str(start) + "," + str(i) + "," + str(stop) + "," + str(i) + ",1);"
                    code += string
            except IndexError:
                stop = cols[j]
                start = cols[j] - count
                count = 0
                string = "line(" + str(start) + "," + str(i) + "," + str(stop) + "," + str(i) + ",1);"
                code += string

    return code

def convert_map_to_horz_lines_erase(mymap,tag):
    """
    @function convert_map_to_hor_lines_erase
    same as convert_map_to_horz_lines but it deletes lines
    faster than convert_map_to_pens when the map contain a large number of raised taxels
    :param mymap: the [12,16] map
    :param tag: the tag of the figure you want to delete
    :return: the entire code string
    """

    mat = np.array(mymap)
    ones_indices = np.nonzero(mat)

    code = ""
    count = 0

    for i in range(0, mat.shape[0]):
        x = np.where(ones_indices[0] == i)
        cols = ones_indices[1][x]
        for j in range(len(cols)):
            try:
                if cols[j + 1] == cols[j] + 1:
                    count += 1
                else:
                    stop = cols[j]
                    start = cols[j] - count
                    count = 0
                    string = "line(" + str(start) + "," + str(i) + "," + str(stop) + "," + str(i) + ",0," + str(tag)+");"
                    code += string
            except IndexError:
                stop = cols[j]
                start = cols[j] - count
                count = 0
                string = "line(" + str(start) + "," + str(i) + "," + str(stop) + "," + str(i) + ",0," + str(tag)+");"
                code += string

    return code