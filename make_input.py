import numpy as np
import math

#data length, probability
#array of data length
#probablilty per query and attribute -> 2way array
#output : AA matrix
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

if __name__ == "__main__" :
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
    