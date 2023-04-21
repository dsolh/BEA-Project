import os

def mk_usg() :
    """
    _summary_
    Create usage matrix(row is query, column is attribute) that contains the values of the attributes' usage by each query.
    Each of values means below:
    usg(1,1) = 1 if query 1 uses attribute 1
    usg(1,1) = 0 if query 1 not use attribute 1
    """
    ## store attributes into list
    att_list = []
    with open("./init/attributes.txt", "rt") as f :
        for line in f.readlines() :
            l = line.strip().split()
            att_list.append(l[1])
    
    ## create usage matrix
    usg = []
    query_file_list = os.listdir("./init/query")
    i = 0
    for file in query_file_list :
        with open("./init/query/%s"%file, "rt") as f :
            query = f.read()
            usg.append([])
            for att in att_list :
                if query.find(att.lower()) >= 0 :
                    usg[i].append(1)
                else :
                    usg[i].append(0)
            i += 1
    
    ## store matrix as a file
    with open("./init/usg.txt", "wt") as f :
        f.write("     ")
        for att in att_list :
            f.write("{:<20}".format(att.lower()))
        f.write("\n")
        
        i = 1
        for u in usg :
            f.write("{:<5}".format(i))
            for v in u :
                f.write("{:<20}".format(v))
            f.write("\n")
            i += 1
                            
    
if __name__ == "__main__" :
    mk_usg()
    