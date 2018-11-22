"""
@OM2
File that start the script for the OM2 experiment
@author Alberto Inuggi, Angelo Raspagliesi, Luca Brayda
@copyright Istituto Italiano di Tecnologia (IIT) 2018
"""

import os
import json
from BPexercises.OM2.ExperimentOM2 import ExperimentOM2

# experimenter (exper) insert:
# - app_address
# - username
# - map name
#
# sw show the map with the three targets blinking (STATE_RUNNING).
# participant (part) explores the map, when ready starts walking, experimenter presses spacebar to pause, sw remove targets (STATE_WAITING).
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
    experiment = ExperimentOM2(params, None)

    # 1) PRODUCTION USER DATA
    experiment.get_input()
    experiment.start_experiment()

    # 2) DEBUG USER DATA
    # app_address = params['app_address']
    # username = 's1'
    # map_name = 'milano'
    #
    # if experiment.debug_set_input(app_address, username, map_name) is not None:
    #     experiment.start_experiment()   # start !!
    # else:
    #     print('error in maps file....experiment aborted !!')
