"""
@Main
@author Angelo Raspagliesi, Alberto Inuggi, Luca Brayda
@copyright Istituto Italiano di Tecnologia (IIT) 2018
"""



import os
import json


try:
    abspath = os.path.abspath(__file__)
    dname = os.path.dirname(abspath)

    # EXPERIMENT PARAMETERS
    with open(os.path.join("paths.json")) as json_file:
        file = json.load(json_file)
        demos = file["demos"]
        paths = file["paths"]

    print("Choose the demo you want to execute")
    print("0 --> Braille")
    print("1 --> GEO1")
    print("2 --> GEO2")
    print("3 --> GEO3")
    print("4 --> HBvsBP")
    print("5 --> OM1")
    print("6 --> OM2")
    print("7 --> Tactris")

    demo_chosen = None

    while demo_chosen is None:
        demo_chosen = input("Insert number: ")
        try:
            demo_chosen = int(demo_chosen)
            if demo_chosen < 0 or demo_chosen > 7:
                demo_chosen = None
                print("Choose the demo you want to execute")
            else:
                os.chdir(os.path.join(dname, paths[demo_chosen]))
                PATH = paths[demo_chosen]
                filename = demos[demo_chosen]
        except:
            demo_chosen = None
            print("Choose the demo you want to execute")
            pass

    exec(open(filename).read())

except Exception as e:
    print(e)
