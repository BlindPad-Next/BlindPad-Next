"""
@Figure
Class that inherit the methods from Figure class and
allow to manipulate braille char on BP
@author Angelo Raspagliesi, Alberto Inuggi, Luca Brayda
@copyright Istituto Italiano di Tecnologia (IIT) 2018
"""

import numpy as np
import copy
from BPexercises.Common import primitives as pt
from BPexercises.GEO3.Figure import Figure

class BrailleChar(Figure):

    width_cell = None
    height_cell = None

    def __init__(self, tag, fig, st_row, st_col, size, pd_socket, rot_id=0):

        self.tag = tag
        self.pd_socket = pd_socket
        self.figure = fig

        self.current_rotation = rot_id
        self.current_col = st_col
        self.current_row = st_row

        self.original_code = self.figure["rotations"][self.current_rotation]["code"]
        self.map = np.zeros((self.MAX_ROWS, self.MAX_COLS))

        self.width_cell = size["width"]
        self.height_cell = size["height"]

        # I add the data info of each base figure to the initial zero matrix at the offset specified by x & y
        for r in range(self.height_cell):
            for c in range(self.width_cell):
                self.map[r + st_row][c + st_col] = fig["rotations"][self.current_rotation]["map"][r][c]

        self.current_code = self.get_shifted_code(self.original_code, st_row, st_col)
        self.show_figure(tag, self.current_code, 1)

        # rotate CW the figure. calc new rotation, calc new map, check overlays with target => if not => do_rotate_map

    def rotate_cw(self, target_figure):
        #  it moves through the rotations entries of the figure..thus doing a clockwise rotation of 90 degrees
        next_rotation = self.current_rotation + 1
        if next_rotation > 3:
            next_rotation = 0

        # I add the data info of each base figure to the initial zero matrix at the offset specified by x & y
        new_map = np.zeros((self.MAX_ROWS, self.MAX_COLS))
        for r in range(self.height_cell):
            for c in range(self.width_cell):
                if (r + self.current_row) >= self.MAX_ROWS or (c + self.current_col) >= self.MAX_COLS:
                    return -1
                new_map[r + self.current_row][c + self.current_col] = self.figure["rotations"][next_rotation]["map"][r][
                    c]

        vs_border = self.crash_borders_rotate(new_map)
        vs_other_figure = self.check_maps_overlap(new_map, target_figure.map)

        if vs_other_figure is False and vs_border is False:
            self.map = new_map
            self.do_rotate_map(next_rotation, target_figure)
            return 1
        else:
            if vs_other_figure is True:
                return 0
            if vs_border is True:
                return -1