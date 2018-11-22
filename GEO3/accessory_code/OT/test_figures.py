import json
import time
import copy
import os

from BPexercises.Common.AppConnector import AppConnector
from BPexercises.Common import primitives as pt
from BPexercises.GEO3.Figure import Figure
from BPexercises.Common.padDrawComm import PadDrawComm

global curr_figure


# return the figure associated to the given fig_name
def get_figure_by_name(fig_name, figures_list):
    for figure in figures_list:
        if figure['name'] == fig_name:
            return copy.deepcopy(figure)
    return None


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
        pd_socket.send(bytes('clear();', 'utf-8'))
        fig = get_figure_by_name(f['name'], figures)
        Figure('target', fig, 0, 0, pd_socket, rot)
        time.sleep(0.5)

if __name__ == "__main__":

    number_of_loops = 100000000
    connect_APP = True
    connect_PD = True

    # EXPERIMENT PARAMETERS
    with open(os.path.join('input_data', "params.json")) as json_file:
        params = json.load(json_file)

    # BLINDPAD APP
    bp_c = None
    if connect_APP is True:
        bp_c = AppConnector(params['app_address'], params['app_port'], on_events)

    # PADDRAW APP
    pd_socket = None
    if connect_PD is True:
        pd_address = 'localhost'
        pd_socket = PadDrawComm(pd_address, params['pd_port'])

    # READ FIGURES DICTIONARY
    path = os.path.join("input_data", "figures_bbrot.json")
    with open(path) as json_file:
        figures = json.load(json_file)['figures']

    loops = 0
    while loops < number_of_loops:
        for fig in figures:
            for r in range(4):
                pd_socket.send(bytes('clear();', 'utf-8'))
                fig = get_figure_by_name(fig['name'], figures)
                Figure('target', fig, 0, 0, pd_socket, r)
                time.sleep(1.5)
        loops = loops + 1

    curr_figure = 0
    tot_figures = len(figures)
    show_figure(curr_figure)


print('finished')