import loadfile as lf
import numpy as np
import os

def get_table(attribute) :
    if attribute.startswith('p_') :
        return 'part'
    elif attribute.startswith('ps_') :
        return 'partsupp'
    elif attribute.startswith('s_') :
        return 'supplier'
    elif attribute.startswith('c_') :
        return 'customer'
    elif attribute.startswith('n_') :
        return 'nation'
    elif attribute.startswith('r_') :
        return 'region'
    elif attribute.startswith('l_') :
        return 'lineitem'
    elif attribute.startswith('o_') :
        return 'orders'
    
def get_table_h(attribute) :
    if attribute == "l_extendedprice" or attribute == "l_discount" :
        return 'lineitem_h'
    elif attribute == "n_name" :
        return 'nation_h'
    elif attribute == "o_orderdate" :
        return 'orders_h'
    elif attribute == "s_nationkey" :
        return 'supplier_h'
    elif attribute == "l_suppkey" :
        return 'lineitem_h2'
    
    return get_table(attribute)

def get_io_cost(inputfile, outputfile, tablelist, type) :
    # make fragment info {site : {attribute : length}}
    frag_dict = lf.load_fragment(inputfile)
    
    # make access frequency array
    rst_array = np.zeros((5, 22)) # site number 5, query number 22

    # load all needed data
    freq = lf.load_freq("./init/freq.txt")

    #calculate
    query_file_list = os.listdir("./init/query")
    i = 0
    for file in query_file_list :
        with open("./init/query/%s"%file, "rt") as f :
            query = f.read()
        print(file)
        
        for rqsite in frag_dict.keys() :
            if freq[rqsite][i] == 0 :
                continue
            
            for othsite in frag_dict.keys() :
                # initiate site reference toggle
                for table in tablelist.keys() :
                    tablelist[table][1] = 0
                
                # calculate access frequency
                for att in frag_dict[othsite] :
                    if query.find(att) >= 0 :
                        if type == "vertical" :
                            table = get_table(att)
                            tablelist[table][1] = 1
                        elif type == "hybrid" :
                            table = get_table_h(att)
                            tablelist[table][1] = 1
                        elif type == "replication" :
                            if (rqsite != othsite and att not in frag_dict[rqsite]) or rqsite == othsite:
                                    #print(rqsite, ",", othsite, ",", att)
                                    table = get_table(att)
                                    tablelist[table][1] = 1
                                                
                record_sum = 0
                for table in tablelist.keys() :
                    if tablelist[table][1] == 1 :
                        record_sum += tablelist[table][0]
                
                # add site access frequency
                rst_array[othsite][i] += record_sum * freq[rqsite][i]
                
                #print("{}, {} data transfer cost : {}".format(rqsite, othsite, dfc))
        i += 1 

    with open(outputfile, "wt") as f :
        for i in range(5) :
            for j in range(22) :
                f.write("%d "%(rst_array[i][j]))
            f.write("\n")
    
if __name__ == "__main__" :
    tablelist = {"part" : [200000, 0], "partsupp":[800000, 0], "supplier":[10000, 0], "customer":[150000, 0], "nation":[25, 0], "region":[5, 0], "lineitem":[6001215, 0], "orders":[1500000, 0]}
    tablelist_h = {"part" : [200000, 0], "partsupp":[800000, 0], "supplier":[10000, 0], "customer":[150000, 0], "nation":[25, 0], "region":[5, 0], "lineitem":[6001215, 0], "orders":[1500000, 0], 
            "lineitem_h" :[1200243, 0],"lineitem_h2":[1500304, 0], "nation_h" : [5, 0], "supplier_h" : [2500, 0], "orders_h" : [300000, 0]}

    get_io_cost("fragment2.txt","io_cost2.txt", tablelist, "vertical")
    get_io_cost("fragment_hybrid.txt", "io_cost_h.txt", tablelist_h, "hybrid")
    get_io_cost("fragment_replication.txt", "io_cost_r.txt", tablelist, "replication")