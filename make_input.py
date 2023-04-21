import numpy as np
import math
import loadfile as lf

def make_input_org2(usg, freq, acc):
    """
    _summary_
    make input matrix for BEA
    
    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    implimentation of 
    Özsu, M. Tamer, and Patrick Valduriez. "Principles of distributed database systems." (1999).
    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

    Args:
        usg (array): usage matrix
        freq (array): access frequency matrix
        acc (array): access number matrix to attributes per quries
    """
    ## make AA matrix
    att_n = usg.shape[1]
    query_n = usg.shape[0]
    site_n = freq.shape[0]
    AA = np.zeros((att_n, att_n))
    for i in range(att_n):
        for j in range(i + 1) :
            sum = 0
            for q in range(query_n) :
                if usg[q][i] == 1 and usg[q][j] == 1 :
                    for s in range(site_n) :
                        sum += freq[s][q] * acc[q]
            AA[i][j] = sum
            AA[j][i] = sum
            
    return AA

def make_input_org(data_length, weights, probability, a) :
    """
    make input matrix for BEA
    
    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    implimentation of 
    Jeffrey A. Hoffer and Dennis G. Severance. "The use of cluster alnalysis in physical data base design". Proceedings of the 1st International Conference on Very Large Data Bases. 1975.
    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

    Args:
        data_length (array): data lengths of each attributes
        weights (array): importance of each queries (e.i. excess frequency, priority)
        probability (array): probability of attribute values required by per queries
        a (flaot): manipulate similarity by the power a
    """
    
    probability = np.array(probability)
    data_length = np.array(data_length)
    
    n = probability.shape[0] #number of attributes
    q = probability.shape[1] #number of queries
    AA = np.zeros((n,n))
    
    for i in range(n) :
        for j in range(i+1) :
            numerator = 0
            denominator = 0
            s_ij = 0
            for t in range(q) :
                p_it = probability[i][t]
                p_jt = probability[j][t]
                l_i = data_length[i]
                l_j = data_length[j]
                if p_it == 0 and p_jt == 0 :
                    c_ijt = 0
                else :
                    c_ijt = (l_i*p_it + l_j*p_jt) / ((l_i+l_j) * max(p_it, p_jt))
                               
                if c_ijt == 0 :
                    s_ijt = 0
                else :
                    s_ijt = ((l_i + l_j) * (c_ijt**a)) / (l_i + l_j)
                
                numerator += weights[t]*s_ijt
                denominator += weights[t]*math.ceil(s_ijt)
            
            s_ij = round(numerator/denominator, 2)
            AA[i][j] = s_ij
            AA[j][i] = s_ij
    
    return AA

def make_input_modified(usg, dist, freq, w1, w2) :
    """
    _summary_
    make input matrix for BEA
    
    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    implimentation of 
    Rahimi, Hossein, Fereshteh-Azadi Parand, and Davoud Riahi. 
    "Hierarchical simultaneous vertical fragmentation and allocation using modified Bond Energy Algorithm in distributed databases." 
    Applied computing and informatics 14.2 (2018): 127-133.
    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

    Args:
        usg (array): usage matrix
        dist (array): distance matrix
        freq(array): access frequency matrix
        w1(float): the weight of n01 and n10
        w2(float): the weight of n00
    """
    ## for convenient programming
    usg = np.array(usg)
    freq = np.array(freq)
    dist = np.array(dist)
    
    ## define variables
    query_n = freq.shape[1]
    site_n = freq.shape[0]
    att_n = usg.shape[1]
    
    ## make MQA
    MQA = dist.dot(freq)
    MQA = MQA * 0.001
    print(MQA)
    
    ## make QS
    q_sum = np.zeros(query_n)
    for q in range(query_n) :
        sum = 0
        for s in range(site_n) :
            sum += MQA[s][q]
        q_sum[q] = sum
    #print(Q_sum)
    QS = q_sum.dot(usg)
    #print(QS)
    ## make AA
    AA = np.zeros((att_n, att_n))
    S = np.zeros((att_n, att_n))
    for i in range(att_n) :
        for j in range(i+1) :
            n00 = 0
            n11 = 0
            n10 = 0
            n01 = 0
        
            for q in range(query_n) :
                if usg[q][i] == 1 and usg[q][j] == 1 :
                    n11 += 1
                elif usg[q][i] == 0 and usg[q][j] == 0 :
                    n00 += 1
                elif usg[q][i] == 0 and usg[q][j] == 1 :
                    n01 += 1
                else :
                    n10 += 1
            if (n01 == 0 and n10 > 0) or (n10 == 0 and n01 > 0) :
                coef = (-1)*(n01 + n10) * w1
            else :
                coef = abs(n01 - n10) * w1
            S[i][j] = (n11 + w2*n00) / (n11 + w2*n00 + coef)
            S[j][i] = S[i][j]
    
    for i in range(att_n) :
        AA[i] = S[i] * QS[i]
    
    #print(AA[0])
    #print(S)
    return S
    

if __name__ == "__main__" :
    #load all needed data
    att_list = lf.load_attr("./init/attributes.txt")
    usg = lf.load_usg("./init/usg.txt")
    freq = lf.load_freq("./init/freq.txt")
    dist = lf.load_dist("./init/dist.txt")
    acc = lf.load_acc("./init/acc.txt")
    
    ## make_input_org2
    #AA = make_input_org2(usg, freq, acc)
    
    ## make_input_modified
    make_input_modified(usg, dist, freq, 0.3, 0.5)
    '''
    usg = np.array(usg)
    usg_t = np.transpose(usg)
    test = usg_t.dot(usg)
    with open("test.txt", "wt") as f:
        for i in range(usg_t.shape[0]) :
            for j in range(usg_t.shape[0]) :
                f.write("{:<5}".format(test[i][j]))
            f.write("\n")
    '''
    '''
    ## make_input_org
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
    
    AA = make_input_org(data_length, weights, probablility, 2)
    print(*AA, sep='\n')
    '''
    
    