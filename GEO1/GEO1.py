"""
@GEO1
File that start the script for the GEO1 experiment
@author Angelo Raspagliesi, Alberto Inuggi, Luca Brayda
@copyright Istituto Italiano di Tecnologia (IIT) 2018
"""


import os
import json
from BPexercises.GEO1.ExperimentGEO1 import ExperimentGEO1

# ============================================================================================================
# The experiment accepts the following inputs:
# ============================================================================================================
#
# 1) app_address        : specify the App address within the local network. e.g.
#                           : "192.168.1.3",
#                           : "10.245.71.73",
#                           : "10.245.71.124"
#
# 2) user_mode          :   accepted values     =   0: if the blindpad is connected with USB
#                                                   1: if the blindpad is connected with bluetooth
#
# 3) user_name          :   participants code   =   any string
#
# 4) modality           :   accepted values     =   0: experiment done with blindpad
#                                                   1: conventionally with TTS
#                                                   this value must be counterbalanced at the end of the whole
#                                                   experimental session.
#
# 5) is_familiarization :   accepted values     =   0 : real experiment
#                                                   1 : familiarization
# ============================================================================================================


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
    experiment = ExperimentGEO1(params)

    # PRODUCTION USER DATA
    experiment.get_input()

    # DEBUG USER DATA
    # user = 'prova'
    # modality = 0   # 0:tactile, 1: auditory
    # is_familiarization = 0
    # ip_address = "10.245.71.72" # input("Inserire indirizzo ip del telefono: ")
    # mode = 0 #input("Inserire 1 se si usa il bluetooth o 0 se si usa l'USB: ")
    # experiment.debug_set_input(mode, ip_address, user, modality, is_familiarization)

    # start !!
    experiment.start_experiment()