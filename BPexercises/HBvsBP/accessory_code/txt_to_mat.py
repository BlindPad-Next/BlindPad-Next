import numpy as np
import os

filename = os.path.join('input_data',"sad.pbm")
mat = np.loadtxt(filename)
mat_l = np.ndarray.tolist(mat.astype(int))
print(mat_l)