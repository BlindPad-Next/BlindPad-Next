"""
@Figure
Class that inherit the methods from Figure class and
allow to manipulate geometical tract in tactris
@author Angelo Raspagliesi, Alberto Inuggi, Luca Brayda
@copyright Istituto Italiano di Tecnologia (IIT) 2018
"""

import numpy as np
import copy
from BPexercises.Common import primitives as pt
from BPexercises.GEO3.Figure import Figure


class Figure_Tactris (Figure):

    # start_space = None

    def __init__(self, tag, fig, st_row, st_col, pd_socket, total_figure, max_rows, max_cols, rot_id=0):

        self.tag = tag
        self.pd_socket = pd_socket
        self.figure = fig

        self.current_rotation = rot_id
        self.current_col = st_col
        self.current_row = st_row

        self.original_code = self.figure["rotations"][self.current_rotation]["code"]
        # self.start_space = start_space

        self.MAX_ROWS = max_rows
        self.MAX_COLS = max_cols
        self.map = np.zeros((self.MAX_ROWS, self.MAX_COLS))

        # I add the data info of each base figure to the initial zero matrix at the offset specified by x & y
        for r in range(4):
            for c in range(4):
                self.map[r + st_row][c + st_col] = fig["rotations"][self.current_rotation]["map"][r][c]

        vs_other_figure = self.check_maps_overlap(self.map, total_figure)
        self.current_code = self.get_shifted_code(self.original_code, st_row, st_col)

        if not vs_other_figure:
            self.show_figure(tag, self.current_code, 1)
        else:
            raise ValueError('Game over')


    # calculate new position, check borders & target => if ok => draw new pos
    def move(self, direction, target_figure, step=1):
        step = 1  # I could move as many step I want in paddraw, but map update is still not ready to do that

        # next position
        new_map = self.move_map(direction)

        vs_border = self.crash_borders(direction, self.map)
        vs_other_figure = self.check_maps_overlap(new_map, target_figure)
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
                if direction is "left" or direction is "right":
                    return -1
                else:
                    return 0


    def move_until_crash(self, target_figure):

        res = self.move('down', target_figure, 1)
        while res:
            res = self.move('down', target_figure, 1)
            if res == -1:
                break

        return res

    # rotate CW the figure. calc new rotation, calc new map, check overlays with target => if not => do_rotate_map
    def rotate_cw(self, total_figure, total_figure_code):
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
        vs_other_figure = self.check_maps_overlap(new_map,total_figure) # oppure target_figure.map

        if vs_other_figure is False and vs_border is False:
            self.map = new_map
            self.do_rotate_map(next_rotation, total_figure_code)
            return 1
        else:
            if vs_other_figure is True:
                return 0
            if vs_border is True:
                return -1

    # rotate the map. 1) clear all, 2) show target, 3) recreate self
    def do_rotate_map(self, new_rotation, total_figure_code):

        self.pd_socket.send_cmd(pt.clear())

        self.current_rotation = new_rotation
        self.original_code = self.figure["rotations"][self.current_rotation]["code"]
        self.current_code = self.get_shifted_code(self.original_code, self.current_row, self.current_col)
        self.show_figure(self.tag, self.current_code, 1)

        # if total_figure_code is None:
        #     total_figure_code = pt.convert_map_to_horz_lines(target_figure)

        self.pd_socket.send_cmd(total_figure_code)
        # target_figure.show_figure(target_figure.tag, target_figure.current_code, 1)



