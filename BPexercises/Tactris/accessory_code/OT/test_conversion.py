import numpy as np
from BPexercises.Common.padDrawComm import PadDrawComm
from datetime import datetime
import BPexercises.Common.primitives as pt
from BPexercises.Common.AppConnector import AppConnector





Epfl = ([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
       [0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 1, 1, 0, 1, 1, 0],
       [1, 1, 0, 0, 1, 1, 0, 1, 0, 1, 1, 0, 0, 1, 1, 0],
       [1, 1, 0, 0, 1, 1, 0, 1, 0, 1, 1, 0, 0, 1, 1, 0],
       [1, 1, 1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 0],
       [1, 1, 1, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 1, 1, 0],
       [1, 1, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 1, 1, 0],
       [1, 1, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 1, 1, 0],
       [0, 1, 1, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1],
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
       [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]])

ones = np.ones((12,16))






pd_address = 'localhost'
pd_port = 12345
pd_socket = PadDrawComm(pd_address, pd_port)

code = ""
count = 0

mat = np.array(Epfl)
ones_indices = np.nonzero(mat)

startTime = datetime.now()
for i in range(0,mat.shape[0]):
    x = np.where(ones_indices[0] == i)
    cols = ones_indices[1][x]
    for j in range(len(cols)):
        try:
            if cols[j+1] == cols[j]+1:
                count += 1
            else:
                stop = cols[j]
                start = cols[j] - count
                count = 0
                string = "line(" + str(start) + "," + str(i) + "," + str(stop) + "," + str(i) + ",1);"
                code += string
        except IndexError:
            stop = cols[j]
            start = cols[j] - count
            count = 0
            string = "line(" + str(start) + "," + str(i) + "," + str(stop) + "," + str(i) + ",1);"
            code += string


# code = pt.convert_map_to_pens(ones)

pd_socket.send_cmd(code)

print(datetime.now() - startTime)
