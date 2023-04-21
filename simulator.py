from make_input import make_input_org2
from make_input import make_input_modified
#from make_input import make_input_org
from bea import BEA
from clustering import clustering
import loadfile as lf
import sys
import numpy as np

#load all needed data
att_list = lf.load_attr("./init/attributes.txt")
usg = lf.load_usg("./init/usg.txt")
freq = lf.load_freq("./init/freq.txt")
dist = lf.load_dist("./init/dist.txt")
acc = lf.load_acc("./init/acc.txt")

'''
#test input
data_length = [6, 30, 9, 50, 7, 4, 1, 1, 6, 6, 6, 6, 5, 2, 2, 2, 2, 2, 1, 10, 12, 14]
weights = [4, 2, 5, 9, 2, 12, 4, 2, 52, 12, 52, 1, 104, 24, 8]
probablility = [[1, 0, 0, 0, 1, 0.4, 0, 0, 0, 0, 0.1, 0, 1, 1, 1],
                [1, 0.9, 1, 0.7, 1, 0.4, 0.07, 0.05, 0.02, 0.7, 0.1, 0, 0, 0, 0],
                [0, 0, 0, 0.7, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0.7, 1, 0, 0.07, 0.05, 0, 0, 0, 0.42, 0, 0, 0],
                [0, 0, 0, 0.7, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0.9, 0, 0, 1, 0.4, 0, 0.05, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 1, 0.4, 0.07, 0, 0, 0, 0, 0.42, 0, 0, 0],
                [0, 0, 0, 0, 1, 0.4, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 1, 0.4, 0, 0.05, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 1, 0, 0.07, 0, 0, 0, 0, 0.42, 0, 0, 0],
                [0 ,0, 0, 0, 1, 0, 0.07, 0, 0, 0, 0, 0.42, 0, 0, 0],
                [0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0.42, 0, 0, 0],
                [0, 1, 1, 0, 1, 0, 0, 1, 1, 0, 0, 1, 0, 0, 1],
                [0 ,0, 1, 0, 1, 0.4, 0, 0, 0, 0, 0, 0.42, 0, 0, 0],
                [0, 0, 1, 1, 1, 0.4, 0, 0, 0, 1, 0, 0.42, 0, 0, 0],
                [0, 0.9, 1, 0.7, 1, 0.4, 0, 0.05, 0.02, 0.7, 0, 0.42, 0, 1, 0],
                [0, 0, 0, 0, 1, 0.4, 0, 0, 0.02, 0.7, 0, 0.42, 0, 1, 0],
                [0, 0, 0, 0, 1, 0.4, 0, 0, 0, 0.7, 0, 0, 0, 1, 0],
                [0, 0, 0, 0, 1, 0.4, 0, 0, 0, 0, 1, 0.42, 0, 0, 0],
                [0, 0, 0, 0, 1, 0.4, 0, 0, 0, 0, 0, 0.42, 0, 0, 0],
                [0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0],
                [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

#run original BEA
AA = make_input_org(data_length, weights, probablility, 1)
rst, CA = BEA(AA)
print(rst)

with open("AA_o.txt", "w") as f :
    for i in range(AA.shape[0]) :
        for j in range(AA.shape[0]) :
            f.write("{:<5}".format(AA[i][j]))
        f.write("\n")
        
with open("CA_o_block.txt", "w") as f :
    for i in range(CA.shape[0]) :
        for j in range(CA.shape[0]) :
            f.write("{:<5.2f}".format(CA[i][j]))
        f.write("\n")
'''

#make input matrix
AA = make_input_org2(usg, freq, acc)

#run BEA
rst, CA = BEA(AA)
print(rst)
#print(CA)

with open("AA.txt", "w") as f :
    for i in range(AA.shape[0]) :
        for j in range(AA.shape[0]) :
            f.write("{:<5}".format(int(AA[i][j])))
        f.write("\n")
        
with open("CA.txt", "w") as f :
    for r in rst :
        f.write("{:<20}".format(att_list[r]))
    f.write("\n")
    for i in range(CA.shape[0]) :
        for j in range(CA.shape[0]) :
            f.write("{:<20}".format(CA[i][j]))
        f.write("\n")
        
with open("CA_block.txt", "w") as f :
    for i in range(CA.shape[0]) :
        for j in range(CA.shape[0]) :
            if CA[i][j] >= 100 :
                f.write("{:<3}".format(int(CA[i][j]//100)))
            else :
                f.write("0  ")
        f.write("\n")
#CA_li = CA.tolist()
#m = max(map(max, CA_li))
#print(m)
#print(np.where(CA == m))

#point = clustering(rst, "./init/usg.txt", "./init/acc.txt")
#print(point)

#run modified
AA = make_input_modified(usg, dist, freq, 0.3, 0.5)
rst, CA = BEA(AA)

print(rst)

with open("AA_m.txt", "w") as f :
    for i in range(AA.shape[0]) :
        for j in range(AA.shape[0]) :
            f.write("{:<5.2f}".format(AA[i][j]))
        f.write("\n")
        
with open("CA_m.txt", "w") as f :
    for r in rst :
        f.write("{:<20}".format(att_list[r]))
    f.write("\n")
    for i in range(CA.shape[0]) :
        for j in range(CA.shape[0]) :
            f.write("{:<20.2f}".format(CA[i][j]))
        f.write("\n")
        
with open("CA_m_block.txt", "w") as f :
    for i in range(CA.shape[0]) :
        for j in range(CA.shape[0]) :
            f.write("{:<5.2f}".format(CA[i][j]))
        f.write("\n")

#primary key 한번 빼도 괜찮을듯