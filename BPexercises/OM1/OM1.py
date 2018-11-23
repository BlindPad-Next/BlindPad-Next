"""
@OM1
File that start the script for the OM1 experiment
@author Alberto Inuggi, Angelo Raspagliesi, Luca Brayda
@copyright Istituto Italiano di Tecnologia (IIT) 2018
"""

import os
import json
from BPexercises.OM1.ExperimentOM1 import ExperimentOM1


# experimenter (exper) insert:
# - app_address "xxx.xxx.xxx.xxx"
# - username "string"
# - map name "string"
# - group (controls or experimental) [0,1]
# - target to reach [0,1,2]
#
# sw show the map with one target blinking (STATE_RUNNING).
# participant (part) explores the map, when ready starts walking, experimenter doubletap the App to pause, sw remove targets (STATE_WAITING).
# when part ends, exper press pause again. sw asks 3 values for each target: (STATE_INSERTING)
#       - id of the closest taxel (positive 1-based integer)
#       - distance between part and closest target (float in meters, with sign.)
#       - time to reach the target
# after 3rd enter, sw shows target blinking + part last position (STATE_RUNNING).
# part explores his position, when ready starts walking => new trial (exper presses spacebar) (STATE_WAITING)
# and so on....after third walk, experiment ends.

if __name__ == "__main__":

    # EXPERIMENT PARAMETERS
    with open(os.path.join('input_data', "params.json")) as json_file:
        params = json.load(json_file)
    abspath = os.path.abspath(__file__)
    dname = os.path.dirname(abspath)

    params["project_path"] = os.path.join(dname, PATH)
    # if you wanna execute from there...
    # params["project_path"] = os.path.dirname(os.path.normpath(__file__))

    # instanciate EXP class
    experiment = ExperimentOM1(params, None)

    # 1) PRODUCTION USER DATA
    experiment.get_input()
    experiment.start_experiment()

    # # 2) DEBUG USER DATA
    # app_address = '10.245.71.72'
    # username = 's1'
    # map_name = 'milano'
    # exp_group = 1  # 0: control, no feedback, 1: experimental, yes feedback
    # target_id = 0  # 0,1,2 : id of the target to user
    #
    # if experiment.debug_set_input(app_address, username, map_name, exp_group, target_id) is not None:
    #     experiment.start_experiment()   # start !!
    # else:
    #     print('error in maps file....experiment aborted !!')
