import numpy as np
def BEA(AA) :
    """
    Reordering attributes to maximize the global affinity measure

    Args:
        AA (2_way array): Attribute Affinity matrix
    """
    AA = np.array(AA)
    n = AA.shape[0] #number of attributes
    rst = [0] #initialize reordering result with attribute 0th
    
    for att in range(1,n):
        pos = len(rst) #max position
        conts = np.zeros((pos+1,)) #contributions per each position
             
        rst = list(map(int, rst))
        
        for k in range(pos+1) :
            #cont_ikj = 2bond_ik + 2bond_kj - 2bond_ij
            if k == 0 :
                bond_ik = 0
            else :
                bond_ik = np.inner(AA[:,rst[k-1]], AA[:,att])
            
            if k == pos:
                bond_kj = 0
            else :
                bond_kj = np.inner(AA[:,rst[k]], AA[:,att])
                
            if k == 0 or k == pos :
                bond_ij = 0
            else :
                bond_ij = np.inner(AA[:,rst[k-1]], AA[:,rst[k]])

            conts[k] = 2*bond_ik + 2*bond_kj - 2*bond_ij
        
        max_cont_pos = np.argmax(conts)
        tmp = np.zeros((pos+1,))
        tmp[:max_cont_pos] = rst[:max_cont_pos]
        tmp[max_cont_pos] = att
        tmp[max_cont_pos+1:] = rst[max_cont_pos:]
        rst = tmp
    
    CA = np.zeros((n,n)) #CA is Clustered Affinity matrix
    tmp = np.zeros((n,n))
    rst = list(map(int, rst))
    
    #reorder columns
    for i in range(n) :
        tmp[:,i] = AA[:,rst[i]]
    
    #reorder rows
    for i in range(n) :
        CA[i,:] = tmp[rst[i],:]
    
    return (rst, CA)
    
if __name__ == "__main__" :
    AA = [[1, 0, 1, 0],
          [0, 1, 0, 1],
          [1, 0, 1, 0],
          [0, 1, 0, 1]]
    
    rst, CA = BEA(AA)
    print(rst)
    print(*CA, sep='\n')