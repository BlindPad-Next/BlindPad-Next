import numpy as np
import copy


class myMap:

    MAX_ROWS = 12
    MAX_COLS = 16

    def __init__(self, st_row=0, st_col=0, minimap=None):

        self.map = np.zeros((self.MAX_ROWS, self.MAX_COLS))

        if minimap is not None:
            # I add the data info of each base figure to the initial zero matrix at the offset specified by x & y
            for r in range(4):
                for c in range(4):
                    self.map[r+st_row][c+st_col] = minimap[r][c]

    # calculate new position, check borders & target => if ok => draw new pos
    def move(self, direction, target_figure, step=1):
        step = 1  # I could move as many step I want in paddraw, but map update is still not ready to do that

        # next position
        new_map = self.move_map(direction)

        if self.can_move_borders(direction, self.map) is True and self.check_maps_overlap(new_map, target_figure.map) is False:
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
        else:
            pass  # TODO bip !!

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
                new_map[r+self.current_row][c+self.current_col] = self.figure["rotations"][next_rotation]["map"][r][c]

        if self.check_maps_overlap(new_map, target_figure.map) is False:
            self.map = new_map
            self.do_rotate_map(next_rotation, target_figure)

        else:
            pass  # TODO bip !!!

    # move map after a translation toward a specific direction. used to move it after successful checks, but also to calculate the possible future position
    def move(self, direction):
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
    def check_maps_overlap(self, other_map):
        nr = len(self.map)
        nc = len(self.map[0])
        for r in range(nr):
            for c in range(nc):
                if self.map[r][c] == 1 and other_map[r][c] == 1:
                    return True
        return False

    # determine whether figure's movement would keep into the pad borders
    def can_move_borders(self, direction):

        if direction is "left":
            if self.get_left_border() > 0:
                return True
            else:
                return False
        elif direction is "right":
            if self.get_right_border() < (self.MAX_COLS-1):
                return True
            else:
                return False
        elif direction is "up":
            if self.get_top_border() > 0:
                return True
            else:
                return False
        elif direction is "down":
            if self.get_bottom_border() < (self.MAX_ROWS-1):
                return True
            else:
                return False

    # get borders
    def get_borders(self):
        return [self.get_top_border(), self.get_left_border(), self.get_bottom_border(), self.get_right_border()]

    def get_left_border(self):
        minid = self.MAX_COLS
        for r in range(self.MAX_ROWS):
            arr = [i for i, j in enumerate(self.map[r, :]) if j == 1]
            if len(arr) > 0:
                minid = min(min(arr), minid)

        return minid

    def get_right_border(self):
        maxid = 0
        for r in range(self.MAX_ROWS):
            arr = [i for i, j in enumerate(self.map[r, :]) if j == 1]
            if len(arr) > 0:
                maxid = max(max(arr), maxid)

        return maxid

    def get_top_border(self):
        minid = self.MAX_ROWS
        for c in range(self.MAX_COLS):
            arr = [i for i, j in enumerate(self.map[:, c]) if j == 1]
            if len(arr) > 0:
                minid = min(min(arr), minid)

        return minid

    def get_bottom_border(self):
        maxid = 0
        for c in range(self.MAX_COLS):
            arr = [i for i, j in enumerate(self.map[:, c]) if j == 1]
            if len(arr) > 0:
                maxid = max(max(arr), maxid)

        return maxid


