import loadfile as lf
import numpy as np
import pymysql
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

def get_communication_cost() :
    # make fragment info {site : {attribute : length}}
    frag_dict = lf.load_fragment_dict('fragment_dict2.txt')
    
    # make table reference list {table : [primary key length, num of records, refenceflag]}
    tbl_rf = {"part" : [4, 200000, 0], "partsupp":[8, 800000, 0], "supplier":[4, 10000, 0], "customer":[4, 150000, 0], "nation":[4, 25, 0], "region":[4, 5, 0], "lineitem":[8, 6001215, 0], "orders":[4, 1500000, 0]}
    
    # communication cost array per request site
    cc_array = np.zeros((5, 22))
    
    # load all needed data
    freq = lf.load_freq("./init/freq.txt")
    dist = lf.load_dist("./init/dist.txt")

    #calculate
    query_file_list = os.listdir("./init/query")
    i = 0
    for file in query_file_list :
        with open("./init/query/%s"%file, "rt") as f :
            query = f.read()
            
        for rqsite in frag_dict.keys() :
            if freq[rqsite][i] == 0 :
                continue
            
            cc = 0 #communication cost
            for othsite in frag_dict.keys() :
                # check same site
                if rqsite == othsite :
                    continue
                
                # initiate site reference toggle
                for table in tbl_rf.keys() :
                    tbl_rf[table][2] = 0
                
                # calculate data transfer cost
                dtc = 0
                for att in frag_dict[othsite].keys() :
                    if query.find(att) >= 0 :
                        table = get_table(att)
                        tbl_rf[table][2] = 1
                        dtc += frag_dict[othsite][att] * tbl_rf[table][1]
                                        
                for table in tbl_rf.keys() :
                    if tbl_rf[table][2] == 1 :
                        dtc += tbl_rf[table][0] * tbl_rf[table][1]
                  
                #print("{}, {} data transfer cost : {}".format(rqsite, othsite, dtc))
                
                cc += dtc * (dist[rqsite][othsite]/1000000) # microseconds -> seconds
            
            cc_array[rqsite][i] = cc
        i += 1 
    
    with open("./communication_cost2.txt", "wt") as f :
        for i in range(5) :
            for j in range(22) :
                f.write("%.2f "%(cc_array[i][j]))
            f.write("\n")
    # 병렬처리 고려 안 한 결과
    
def get_data_transfer_cost(inputfile, outputfile, tablelist, type) :
    # make fragment info {site : {attribute : length}}
    frag_dict = lf.load_fragment_dict(inputfile)
    
    # data transfer cost array per request site
    dtc_array = np.zeros((5, 22))
    
    # load all needed data
    freq = lf.load_freq("./init/freq.txt")

    #calculate
    query_file_list = os.listdir("./init/query")
    i = 0
    for file in query_file_list :
        with open("./init/query/%s"%file, "rt") as f :
            query = f.read()
            
        for rqsite in frag_dict.keys() :
            if freq[rqsite][i] == 0 :
                continue
            
            total_dtc = 0 # total data transfer cost
            for othsite in frag_dict.keys() :
                # check same site
                if rqsite == othsite :
                    continue
                
                # initiate site reference toggle
                for table in tablelist.keys() :
                    tablelist[table][2] = 0
                
                # calculate data transfer cost
                dtc = 0
                for att in frag_dict[othsite].keys() :
                    if query.find(att) >= 0 :
                        if type == "vertical" :
                            table = get_table(att)
                            tablelist[table][2] = 1
                            dtc += frag_dict[othsite][att] * tablelist[table][1]
                        elif type == "hybrid" :
                            table = get_table_h(att)
                            tablelist[table][2] = 1
                            dtc += frag_dict[othsite][att] * tablelist[table][1]
                        elif type == "replication" :
                            if (rqsite != othsite and att not in frag_dict[rqsite].keys()) or rqsite == othsite:
                                    table = get_table(att)
                                    tablelist[table][2] = 1
                                    dtc += frag_dict[othsite][att] * tablelist[table][1]                         
                                        
                for table in tablelist.keys() :
                    if tablelist[table][2] == 1 :
                        dtc += tablelist[table][0] * tablelist[table][1]
                  
                #print("{}, {} data transfer cost : {}".format(rqsite, othsite, dfc))
                
                total_dtc += dtc
            
            dtc_array[rqsite][i] = total_dtc
        i += 1 
    
    with open(outputfile, "wt") as f :
        for i in range(5) :
            for j in range(22) :
                f.write("%d "%(dtc_array[i][j]))
            f.write("\n")

if __name__ == "__main__" :
    tablelist = {"part" : [4, 200000, 0], "partsupp":[8, 800000, 0], "supplier":[4, 10000, 0], "customer":[4, 150000, 0], "nation":[4, 25, 0], "region":[4, 5, 0], "lineitem":[8, 6001215, 0], "orders":[4, 1500000, 0]}
    tablelist_h = {"part" : [4, 200000, 0], "partsupp":[8, 800000, 0], "supplier":[4, 10000, 0], "customer":[4, 150000, 0], "nation":[4, 25, 0], "region":[4, 5, 0], "lineitem":[8, 6001215, 0], "orders":[4, 1500000, 0], 
            "lineitem_h" :[8, 1200243, 0],"lineitem_h2":[8, 1500304, 0], "nation_h" : [4, 5, 0], "supplier_h" : [4, 2500, 0], "orders_h" : [4, 300000, 0]}

    #get_communication_cost()
    get_data_transfer_cost("fragment_dict2.txt", "data_transfer_cost2.txt", tablelist, "vertical")
    get_data_transfer_cost("fragment_dict_h.txt", "data_transfer_cost_h.txt", tablelist_h, "hybrid")
    get_data_transfer_cost("fragment_dict_r.txt", "data_transfer_cost_r.txt", tablelist, "replication")