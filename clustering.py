import numpy as np

def clustering(att_order, usg_path, freq_path, acc_path) :
    """
    _summary_
    Cluster attributes to site_n groups such that there are minimal applications that access all groups of attributes

    Args:
        att_order (array) : permutation of attributes
        usg_path (str): usage matrix file path
        freq_path (str): access frequency matrix file path
        acc_path (str): access matrix file path
        site_n(int) : the number of sites(groups)
    """
    ## usg matrix
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
    #print(usg.shape)
    
    ## freq matrix
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
    #print(freq.shape)
    
    ## acc matrix
    acc = []
    with open(acc_path, "rt") as f :
        for line in f.readlines() :
            for v in line.split() :
                acc.append(int(v))
    acc = np.array(acc)
    #print(acc)
    
    ## find point that maximizes 'ctq * cbq - coq^2'
    att_order = np.array(att_order)
    att_n = att_order.shape[0]
    query_n = usg.shape[0]
    site_n = freq.shape[0]
    find_point = []
    for p in range(att_n-1, 0, -1) :
        ctq = 0 #total number of accesses to attributes by queries that access only TA
        cbq = 0 #total number of accesses to attributes by queries that access only BA
        coq = 0 #total number of accesses to attributes by queries that access both TA and BA
        q_chck = np.zeros(query_n) #check quries that access only TA or BA
        
        for q in range(query_n) :
            ## ctq
            access = 0
            for i in range(att_n-1, p-1, -1) :
                if usg[q][att_order[i]] == 1 : 
                    access = 1
                    break
            if access == 0 :
                freq_sum = 0
                for s in range(site_n) :
                    freq_sum += freq[s][q]
                ctq += acc[q] * freq_sum
                q_chck[q] = 1
            
            ## cbq
            access = 0
            for i in range(p) :
                if usg[q][att_order[i]] == 1 :
                    access = 1
                    break
            if access == 0 :
                freq_sum = 0
                for s in range(site_n) :
                    freq_sum += freq[s][q]
                cbq += acc[q] * freq_sum
                q_chck[q] = 1
        
        ## coq
        for q in range(query_n) :
            if q_chck[q] == 0 :
                freq_sum = 0
                for s in range(site_n) :
                    freq_sum += freq[s][q]
                coq += acc[q] * freq_sum
        print(ctq, cbq, coq)
        find_point.insert(0, ctq * cbq - (coq*2))
    find_point.insert(0, 0)
    print(find_point)
    point = find_point.index(max(find_point))
    #print(find_point[36])
    
    return point
            
if __name__ == "__main__" :
    att_order = [58, 36, 31, 30, 22, 19, 15, 3, 7, 59, 43, 60, 55, 54, 12, 11, 57, 14, 28, 26, 29, 13, 50, 25, 34, 24, 4, 10, 40, 2, 48, 45, 17, 16, 0, 52, 53, 37, 56, 6, 5, 23, 1, 33, 32, 35, 46, 47, 49, 51, 27, 21, 20, 18, 38, 42, 41, 44, 39, 8, 9]
    print(clustering(att_order, "./init/usg.txt", "./init/freq.txt", "./init/acc.txt"))
    print(att_order[36])