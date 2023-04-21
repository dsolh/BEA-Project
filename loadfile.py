#########################################
# load file needed to make input matrix #
#########################################
import numpy as np

def load_usg(usg_path) :
    usg = []
    with open(usg_path, "rt") as f :
        lines = f.readlines()
        i = 0
        for line in lines[1:] :
            usg.append([])
            line = line.split()
            for v in line[1:] :
                usg[i].append(int(v))
            i += 1
    usg = np.array(usg)
    return usg

def load_freq(freq_path) :
    freq = []
    with open(freq_path, "rt") as f :
        lines = f.readlines()
        i = 0
        for line in lines[1:] :
            freq.append([])
            line = line.split()
            for v in line[1:] :
                freq[i].append(int(v))
            i += 1
    freq = np.array(freq)
    return freq

def load_acc(acc_path) :
    acc = []
    with open(acc_path, "rt") as f :
        for line in f.readlines() :
            for v in line.split() :
                acc.append(int(v))
    acc = np.array(acc)
    return acc

def load_dist(dist_path) :
    dist = []
    with open(dist_path, "rt") as f :
        i = 0
        for line in f.readlines() :
            dist.append([])
            for v in line.split() :
                dist[i].append(int(v))
            i += 1
    dist = np.array(dist)
    return dist

def load_attr(att_path) :
    att_list = []
    with open(att_path, "rt") as f :
        for line in f.readlines() :
            line = line.split()
            att_list.append(line[1])
    return att_list

def load_fragment(fragment_path) :
    frag_dict = {}
    with open(fragment_path, "rt") as f :
        i = 0
        for line in f.readlines() :
            frag_dict[i] = []
            atts = line.split()
            for att in atts :
                frag_dict[i].append(att)
            i += 1
    return frag_dict

def load_fragment_dict(fragment_dict_path) :
    frag_dict = {}
    with open(fragment_dict_path, "rt") as f :
        i = 0
        for line in f.readlines() :
            frag_dict[i] = {}
            attinfos = line.split()
            for attinfo in attinfos :
                info = attinfo.split(":")
                frag_dict[i][info[0]] = int(info[1])
            i += 1
    return frag_dict
            