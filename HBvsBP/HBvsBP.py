"""
@HBvsBP
File that start the script for the HBvsBP experiment
@author Angelo Raspagliesi, Alberto Inuggi, Luca Brayda
@copyright Istituto Italiano di Tecnologia (IIT) 2018
"""

import os
import json
from BPexercises.HBvsBP.ExperimentHBvsBP import ExperimentHBvsBP

# ============================================================================================================
# The experiment accepts the following inputs:
# ============================================================================================================
#
# 1)  app_address       : specify the App address within the local network. e.g.
#                           : "192.168.1.3",
#                           : "10.245.71.73",
#                           : "10.245.71.124"
#
# 2) exp_type           :   accepted values     =   0: for children 8-14 years  (only translate)
#                                                   1: for participants from 15-60 years (translate and rotate)
#
# 3) user_name          :   participants code   =   any string
#
# 4) modality           :   accepted values     =   0: BlindPad
#                                                   1: HyperBraille
#
#
# 5) trial type         :   accepted values     =   A or B.
#                                                   this value must be counterbalanced at the end of the whole
#                                                   experimental session.
#
# 6) is_familiarization :   accepted values     =   0 : real experiment
#                                                   1 : familiarization
# ============================================================================================================
if __name__ == "__main__":

    try:
        # EXPERIMENT PARAMETERS
        with open(os.path.join('input_data', "params.json")) as json_file:
            params = json.load(json_file)

        abspath = os.path.abspath(__file__)
        dname = os.path.dirname(abspath)

        params["project_path"] = os.path.join(dname, PATH)
        # if you wanna execute from there...
        # params["project_path"] = os.path.dirname(os.path.normpath(__file__))

        # instanciate EXP class
        experiment = ExperimentHBvsBP(params)

        experiment.get_input()
        # PRODUCTION USER DATA
        experiment.start_experiment()  # start !!

        # DEBUG USER DATA
        # app_address = params['app_address']
        # # exp_type = 1    # 0: 8-14y, 1:15-50y
        # user = 'prova'
        # modality = 0    # 0:blindpad, 1: hyperbraille
        # # # trials_type = 'A'
        # is_familiarization = 0
        # # user_responses = 'gest'
        # start_from = 1
        # #
        # experiment.debug_set_input(user, modality, is_familiarization, start_from)
        # experiment.start_experiment()   # start !!


    except Exception as e:
        print(e)