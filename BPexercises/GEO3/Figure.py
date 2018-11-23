"""
@Figure
Class that allow to create and manipulate a geometrical object on BP
@author Alberto Inuggi, Angelo Raspagliesi, Luca Brayda
@copyright Istituto Italiano di Tecnologia (IIT) 2018
"""


import numpy as np
import time
import copy
from BPexercises.Common import primitives as pt


class Figure:

    map = None
    pd_socket = None
    tag = None
    figure = None  # contains: {name:"", rotations:[{code:[], data:[]},{},{},{}]}

    original_code = None    # original code before displacement
    current_code = None     # final code after displacement
    current_code_str = ''   # string version of final code
    current_rotation = None
    current_row = None
    current_col = None

    MAX_ROWS = 12
    MAX_COLS = 16

    def __init__(self, tag, fig, st_row, st_col, pd_socket, rot_id=0):

        self.tag = tag
        self.pd_socket = pd_socket
        self.figure = fig

        self.current_rotation = rot_id
        self.current_col = st_col
        self.current_row = st_row

        self.original_code = self.figure["rotations"][self.current_rotation]["code"]

        self.map = np.zeros((self.MAX_ROWS, self.MAX_COLS))

        # I add the data info of each base figure to the initial zero matrix at the offset specified by x & y
        for r in range(4):
            for c in range(4):
                self.map[r+st_row][c+st_col] = fig["rotations"][self.current_rotation]["map"][r][c]

        self.current_code = self.get_shifted_code(self.original_code, st_row, st_col)
        self.show_figure(tag, self.current_code, 1)

    # create a new drawing code, given an original one & current position
    def get_shifted_code(self, original_code, st_row, st_col):

        nlines = len(self.original_code)
        new_code = np.zeros((nlines, 4))

        for l in range(nlines):
            new_code[l][0] = original_code[l][0] + st_col
            new_code[l][2] = original_code[l][2] + st_col
            new_code[l][1] = original_code[l][1] + st_row
            new_code[l][3] = original_code[l][3] + st_row

        return new_code

    # draw or delete a figure
    def show_figure(self, tag, code, visibility=1):

        self.current_code_str = ''
        nlines = len(code)
        for l in range(nlines):
            # line(startx, starty, endx, endy, value, tag)
            self.current_code_str = self.current_code_str + "line(" + str(int(code[l][0])) + "," + str(int(code[l][1])) + "," + str(int(code[l][2])) + "," + str(int(code[l][3])) + ", " + str(visibility) + "," + "*" + tag + ");"

        # print("creating figure with tag: " + tag + " and code: " + self.current_code_str)
        self.pd_socket.send_cmd(self.current_code_str)

    # calculate new position, check borders & target => if ok => draw new pos
    def move(self, direction, target_figure, step=1):
        step = 1  # I could move as many step I want in paddraw, but map update is still not ready to do that

        # next position
        new_map = self.move_map(direction)

        vs_border = self.crash_borders(direction, self.map)
        vs_other_figure = self.check_maps_overlap(new_map, target_figure.map)
        if vs_border is False and vs_other_figure is False:
            if direction is "left":
                msg = pt.move(-step, 0, self.tag)
                self.current_col = self.current_col - step
            elif direction is "right":
                msg = pt.move(step, 0, self.tag)
                self.current_col = self.current_col + step
            elif direction is "up":
                msg = pt.move(0, -step, self.tag)
                self.current_row = self.current_row - step
            elif direction is "down":
                msg = pt.move(0, step, self.tag)
                self.current_row = self.current_row + step


            self.map = new_map
            self.pd_socket.send_cmd(msg)
            return 1
        else:
            if vs_other_figure is True:
                return 0
            if vs_border is True:
                return -1

    # rotate CW the figure. calc new rotation, calc new map, check overlays with target => if not => do_rotate_map
    def rotate_cw(self, target_figure):
        #  it moves through the rotations entries of the figure..thus doing a clockwise rotation of 90 degrees
        next_rotation = self.current_rotation + 1
        if next_rotation > 3:
            next_rotation = 0

        # I add the data info of each base figure to the initial zero matrix at the offset specified by x & y
        new_map = np.zeros((self.MAX_ROWS, self.MAX_COLS))
        for r in range(4):
            for c in range(4):
                if (r+self.current_row) >= self.MAX_ROWS or (c+self.current_col) >= self.MAX_COLS:
                    return -1
                new_map[r+self.current_row][c+self.current_col] = self.figure["rotations"][next_rotation]["map"][r][c]

        vs_border = self.crash_borders_rotate(new_map)
        vs_other_figure = self.check_maps_overlap(new_map,target_figure.map)

        if vs_other_figure is False and vs_border is False:
            self.map = new_map
            self.do_rotate_map(next_rotation, target_figure)
            return 1
        else:
            if vs_other_figure is True:
                return 0
            if vs_border is True:
                return -1

    # rotate the map. 1) clear all, 2) show target, 3) recreate self
    def do_rotate_map(self, new_rotation, target_figure):

        self.pd_socket.send_cmd(pt.clear())

        self.current_rotation = new_rotation
        self.original_code = self.figure["rotations"][self.current_rotation]["code"]
        self.current_code = self.get_shifted_code(self.original_code, self.current_row, self.current_col)
        self.show_figure(self.tag, self.current_code, 1)

        target_figure.show_figure(target_figure.tag, target_figure.current_code, 1)

    # move map after a translation toward a specific direction. used to move it after successful checks, but also to calculate the possible future position
    def move_map(self, direction):
        temp_map = copy.deepcopy(self.map)
        if direction is "left":
            for r in range(self.MAX_ROWS):
                for c in range(self.MAX_COLS - 1):
                    temp_map[r][c] = self.map[r][c + 1]
                temp_map[r][self.MAX_COLS - 1] = 0

        elif direction is "right":
            for r in range(self.MAX_ROWS):
                for c in range(self.MAX_COLS - 1, 0, -1):
                    temp_map[r][c] = self.map[r][c - 1]
                temp_map[r][0] = 0

        elif direction is "up":
            for c in range(self.MAX_COLS):
                for r in range(self.MAX_ROWS - 1):
                    temp_map[r][c] = self.map[r + 1][c]
                temp_map[self.MAX_ROWS - 1][c] = 0

        elif direction is "down":
            for c in range(self.MAX_COLS):
                for r in range(self.MAX_ROWS - 1, 0, -1):
                    temp_map[r][c] = self.map[r - 1][c]
                temp_map[0][c] = 0

        return temp_map

    # check whether two maps have at least one point where both are 1 => return True
    def check_maps_overlap(self, map1, map2):
        nr = len(map1)
        nc = len(map1[0])
        for r in range(nr):
            for c in range(nc):
                if map1[r][c] == 1 and map2[r][c] == 1:
                    return True
        return False

    # determine whether figure's movement would make it crash the pad borders
    def crash_borders(self, direction, fmap):

        if direction is "left":
            if self.get_left_border(fmap) > 0:
                return False
            else:
                return True
        elif direction is "right":
            if self.get_right_border(fmap) < (self.MAX_COLS-1):
                return False
            else:
                return True
        elif direction is "up":
            if self.get_top_border(fmap) > 0:
                return False
            else:
                return True
        elif direction is "down":
            if self.get_bottom_border(fmap) < (self.MAX_ROWS-1):
                return False
            else:
                return True

    # determine whether figure's rotation would make it crash the pad borders
    def crash_borders_rotate(self, fmap):

        minid_COLS = self.MAX_COLS
        maxid_COLS = 0
        minid_ROWS = self.MAX_ROWS
        maxid_ROWS = 0

        for r in range(self.MAX_ROWS):
            arr = [i for i, j in enumerate(fmap[r, :]) if j == 1]
            if len(arr) > 0:
                minid_COLS = min(min(arr), minid_COLS)
                maxid_COLS = max(max(arr), maxid_COLS)

        for c in range(self.MAX_COLS):
            arr = [i for i, j in enumerate(fmap[:, c]) if j == 1]
            if len(arr) > 0:
                minid_ROWS = min(min(arr), minid_ROWS)
                maxid_ROWS = max(max(arr), maxid_ROWS)

        crash_arr = [0,0,0,0]

        if minid_COLS > 0:
            crash_arr[0] = False
        else:
            crash_arr[0] = True

        if maxid_COLS < (self.MAX_COLS - 1):
            crash_arr[1] = False
        else:
            crash_arr[1] = True

        if minid_ROWS > 0:
            crash_arr[2] = False
        else:
            crash_arr[2] = True

        if maxid_ROWS < (self.MAX_ROWS - 1):
            crash_arr[3] = False
        else:
            crash_arr[3] = True

        if True in crash_arr:
            return True
        else:
            return False

    # get borders
    def get_borders(self, fmap):
        return [self.get_top_border(fmap), self.get_left_border(fmap), self.get_bottom_border(fmap), self.get_right_border(fmap)]

    def get_left_border(self, fmap):
        minid = self.MAX_COLS
        for r in range(self.MAX_ROWS):
            arr = [i for i, j in enumerate(fmap[r, :]) if j == 1]
            if len(arr) > 0:
                minid = min(min(arr), minid)

        return minid

    def get_right_border(self, fmap):
        maxid = 0
        for r in range(self.MAX_ROWS):
            arr = [i for i, j in enumerate(fmap[r, :]) if j == 1]
            if len(arr) > 0:
                maxid = max(max(arr), maxid)

        return maxid

    def get_top_border(self, fmap):
        minid = self.MAX_ROWS
        for c in range(self.MAX_COLS):
            arr = [i for i, j in enumerate(fmap[:, c]) if j == 1]
            if len(arr) > 0:
                minid = min(min(arr), minid)

        return minid

    def get_bottom_border(self, fmap):
        maxid = 0
        for c in range(self.MAX_COLS):
            arr = [i for i, j in enumerate(fmap[:, c]) if j == 1]
            if len(arr) > 0:
                maxid = max(max(arr), maxid)

        return maxid
