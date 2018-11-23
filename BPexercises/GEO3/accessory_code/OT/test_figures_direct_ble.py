import json
import time
import copy
import os

from BPexercises.GEO3.Figure import Figure
from BPexercises.GEO3.accessory_code.OT import com_bt_v3 as com_bt, img_matrixs_preloaded as mat

global curr_figure


# return the figure associated to the given fig_name
def get_figure_by_name(fig_name, figures_list):
    for figure in figures_list:
        if figure['name'] == fig_name:
            return copy.deepcopy(figure)
    return None


# def convert_lines_to_map(msg):
#     mymap = np.zeros((13, 17))
#     #msg = "line(0,11,0,10,1,*L01);line(1,11,1,4,1,*L02);line(2,11,2,6,1,*L03);"
#     cmd_list = msg.split(';')
#     for c in range(len(cmd_list) - 1):
#
#         strcmd = cmd_list[c][5:]
#         arr_values = strcmd.split(",")
#         for v in range(5):
#             arr_values[v] = int(arr_values[v])
#
#         positions = arr_values[0:4]
#         value = arr_values[4]
#
#         if positions[0] == positions[2]:
#             # vertical
#             if positions[1] > positions[3]:
#                 for r in range(positions[3], positions[1]+1, 1):
#                     mymap[r + 1][positions[0] + 1] = value
#             else:
#                 for r in range(positions[1], positions[3]+1, 1):
#                     mymap[r + 1][positions[0] + 1] = value
#
#         elif positions[1] == positions[3]:
#             # horizontal
#             if positions[0] > positions[2]:
#                 for c in range(positions[2], positions[0]+1, 1):
#                     mymap[positions[1]][c + 1] = value
#             else:
#                 for r in range(positions[1], positions[3]+1, 1):
#                     mymap[positions[1]][c + 1] = value
#
#         elif positions[1] == positions[3] and positions[0] == positions[2]:
#             # point
#             mymap[positions[1] + 1][positions[1] + 1] = value
#
#     return mymap



def on_events(type, event):

    global curr_figure
    if event == 'SL' or event == '2' or event == 'L':
        curr_figure = curr_figure - 1
        if curr_figure < 0:
            curr_figure = tot_figures - 1
        show_figure(curr_figure)
    elif event == 'SR' or event == '5' or event == 'R':
        curr_figure = curr_figure + 1
        if curr_figure == tot_figures:
            curr_figure = 0
        show_figure(curr_figure)
    elif event == 'DT' or event == '6' or event == 'space':
        show_figure(curr_figure)


def show_figure(figure_id):
    f = figures[figure_id]

    for rot in range(4):
        grid = mat.zeros
        btDemo.print_Grid(grid)
        fig = get_figure_by_name(f['name'], figures)
        Figure('target', fig, 0, 0, btDemo, rot)
        time.sleep(0.5)

if __name__ == "__main__":

    connect_APP = True
    connect_PD = True

    N_ROWS = 12
    N_COLUMNS = 16

    # EXPERIMENT PARAMETERS
    with open(os.path.join('input_data', "params.json")) as json_file:
        params = json.load(json_file)

    btDemo = com_bt.blueToothDemo(N_ROWS, N_COLUMNS)

    # READ FIGURES DICTIONARY
    path = os.path.join("input_data", "figures_bbrot.json")
    with open(path) as json_file:
        figures = json.load(json_file)['figures']

    for fig in figures:
        for r in range(4):
            grid = mat.zeros
            btDemo.print_Grid(grid)
            fig = get_figure_by_name(fig['name'], figures)
            Figure('target', fig, 0, 0, btDemo, r)
            time.sleep(2)

    curr_figure = 0
    tot_figures = len(figures)
    show_figure(curr_figure)


print('finished')