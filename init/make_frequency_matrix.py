import numpy as np

def mk_freq(site, query) :
    """
    _summary_
    Create random access frequency of queries per sites.
    Store freq matrix as a file

    Args:
        site (int): the number of sites
        query (int): the number of queries
    """
    ## create matrix
    freq = []
    for s in range(site):
        freq.append([])
        for q in range(query):
            freq[s].append(np.random.randint(101))
            
    ## store matrix as a file
    with open("./init/freq.txt", "wt") as f :
        f.write("     ")
        for q in range(1, query+1) :
            f.write("{:<5}".format(q))
        f.write("\n")
        
        i = 1
        for fr in freq :
            f.write("{:<5}".format(i))
            for v in fr :
                f.write("{:<5}".format(v))
            f.write("\n")
            i += 1

if __name__ == "__main__" :
    mk_freq(5, 22)