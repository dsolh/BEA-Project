import loadfile as lf
import numpy as np
import pymysql

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

# get fragment.txt
frag_dict = lf.load_fragment('fragment_replication.txt')

conn = pymysql.connect(host="192.168.56.102", user="root",
                           password="1234", db="tpch1", charset="utf8")

with open("./fragment_dict_r.txt", "wt") as f:
    for site in frag_dict.keys() :
        for att in frag_dict[site] :
            cur = conn.cursor()
            
            table = get_table(att)
            get_atts_sql = ("select column_type, character_maximum_length from information_schema.columns where table_name = \"%s\" and column_name = \"%s\";"%(table, att))
            cur.execute(get_atts_sql)
            
            row = cur.fetchone()
            type = str(row[0])
            if type.startswith("int") :
                length = 4
            elif type.startswith("decimal") :
                length = 16
            elif type.startswith("date") :
                length = 3
            else :
                length = int(row[1])
            
            f.write("%s:%d\t"%(att, length))
        f.write("\n")

conn.close()