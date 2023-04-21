import pymysql


def ext_atts(host, user, password, db, charset='utf8'):
    """
    _summary_
    Extract attributes from mariadb database and store into init/attributes.txt
    'attributes.txt' will be formed as follow :
    (index) (attribute_name)\n

    Args:
        host (str): host ip of db server
        user (str): user name to login
        password (str): password of user
        db (str): database name to connect
        charset (str, optional): decode format. Defaults to 'utf8'.
    """

    conn = pymysql.connect(host=host, user=user,
                           password=password, db=db, charset=charset)
    cur = conn.cursor()

    get_atts_sql = ("SELECT COLUMN_NAME, COLUMN_KEY FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA='" 
                    + db 
                    + "' AND TABLE_NAME IN ( SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA='" 
                    + db + "')")
    cur.execute(get_atts_sql)

    with open("./init/attributes.txt", "wt") as f:
        i = 0
        while True:
            row = cur.fetchone()
            if row == None : break
            # 만약에 데이터에 db site id 추가하는 방식으로 클러스터링할거면 여기서 site_id 속성은 안 쓰고 넘어가는걸로.
            att = row[0].lower()
            if att != "o_clerk" and att != "p_retailprice" and att != "ps_comment" and att != "p_comment" and att != "r_comment" and att != "n_comment" and att != "l_comment" and row[1] != "PRI":
                f.write("%d %s\n"%(i, att))
                i += 1
    
    conn.close()
    
if __name__ == "__main__" :
    ext_atts("192.168.56.102", "root", "1234", 'tpch1')