import json
import time
import copy
import os
import keyboard

from BPexercises.Common.AppConnector import AppConnector
from BPexercises.Common import primitives as pt
from BPexercises.GEO3.Figure import Figure
from BPexercises.Common.keyThread import KeyThread
from BPexercises.Common.padDrawComm import PadDrawComm


global curr_trial
global trial_cnt
global trialsA
global trialsB

# return the figure associated to the given fig_name
def get_figure_by_name(fig_name, figures_list):
    for figure in figures_list:
        if figure['name'] == fig_name:
            return copy.deepcopy(figure)
    return None


def on_events(type, event):

    global curr_trial
    global trialsA
    global trialsB


    if event == 'SL' or event == '2' or event == 'left':
        curr_trial = curr_trial - 1
        if curr_trial < 0:
            curr_trial = tot_trials - 1
        show_trial(trialsB[curr_trial])
    elif event == 'SR' or event == '5' or event == 'right':
        curr_trial = curr_trial + 1
        if curr_trial == tot_trials:
            curr_trial = 0
        show_trial(trialsB[curr_trial])


def show_trial(t, waitfor=2):
    global trial_cnt

    trial_cnt = trial_cnt + 1
    pd_socket.send_cmd(pt.clear())

    fig = get_figure_by_name(t['target_figure'], figures)
    Figure('target', fig, params['target_positions'][0], params['target_positions'][1], pd_socket, t['rot'])

    for f in range(num_figures):
        tract_pos = params['tracts_positions'][exp_type][f]

        tract_name = eval("t['tract" + str(f) + "']")
        tract_rot = eval("t['rot" + str(f) + "']")

        fig = get_figure_by_name(tract_name, figures)
        Figure("tract" + str(f), fig, tract_pos[0], tract_pos[1], pd_socket, tract_rot)

    time.sleep(waitfor)
    n_corr = len(t['correct_maps'])
    pd_socket.send_cmd(pt.clear())
    pd_socket.send_cmd(pt.convert_map_to_pens(t['correct_maps'][0]))

    if n_corr > 1:
        time.sleep(waitfor)
        pd_socket.send_cmd(pt.clear())
        pd_socket.send_cmd(pt.convert_map_to_pens(t['correct_maps'][1]))

    print("displayed trial :" + t['target_figure'] + "-" + t['tract0'])


if __name__ == "__main__":

    waitfor = 1.0
    start_trial_id = 0
    trial_cnt = 0
    number_of_loops = 100000000
    exp_type = 0
    num_figures = 1
    connect_APP = False
    connect_PD = True

    show_loop = True

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

    # READ ALL AVAILABLE TRIALS
    path = os.path.join("input_data", "trials_" + str(exp_type) + ".json")  # trials_0.json or trials_1.json
    with open(path) as json_file:
        trials = json.load(json_file)['trials']
    trialsA = trials['typeA']
    trialsB = trials['typeB']

    curr_trial = 0
    tot_trials = len(trialsA)

    if show_loop is True:

        loops = 0
        while loops < number_of_loops:

            for tr in range(start_trial_id, tot_trials):
                show_trial(trialsA[tr], waitfor)
                time.sleep(waitfor)
                show_trial(trialsB[tr], waitfor)
                time.sleep(waitfor)
            loops = loops + 1
    else:
        keynext = KeyThread(on_events)
        curr_trial = start_trial_id
        show_trial(trialsB[curr_trial], waitfor)

