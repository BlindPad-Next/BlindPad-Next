"""
@Figure_HB_BP
Class that allow to create and manipulate a geometrical object on BP and on HB
@author Angelo Raspagliesi, Alberto Inuggi, Luca Brayda
@copyright Istituto Italiano di Tecnologia (IIT) 2018
"""

import numpy as np
import copy
from BPexercises.Common import primitives as pt
from BPexercises.GEO3.Figure import Figure


class Figure_HB_BP (Figure):

    # start_space = None
    width_cell = None
    height_cell = None

    def __init__(self, tag, fig, st_row, st_col, pd_socket, size, max_rows, max_cols, rot_id=0):

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

        self.width_cell = size["width"]
        self.height_cell = size["height"]

        # I add the data info of each base figure to the initial zero matrix at the offset specified by x & y
        for r in range(self.height_cell):
            for c in range(self.width_cell):
                self.map[r + st_row][c + st_col] = fig["rotations"][self.current_rotation]["map"][r][c]

        self.current_code = self.get_shifted_code(self.original_code, st_row, st_col)
        self.show_figure(tag, self.current_code, 1)

