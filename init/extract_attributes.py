import pymysql


def ext_atts(host, user, password, db, charset='utf8'):
    """
    _summary_
    Extract attributes from mariadb database and store into init/attributes.txt
    'attributes.txt' will be formed as follow :
    (index) (attribute_name)\n

    Args:
        host (string): host ip of db server
        user (string): user name to login
        password (string): password of user
        db (string): database name to connect
        charset (str, optional): decode format. Defaults to 'utf8'.
    """

    conn = pymysql.connect(host=host, user=user,
                           password=password, db=db, charset=charset)
    cur = conn.cursor()

    get_atts_sql = ("SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA='" 
                    + db 
                    + "' AND TABLE_NAME IN ( SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA='" 
                    + db + "')")
    cur.execute(get_atts_sql)

    with open("./init/attributes.txt", "wt") as f:
        i = 0
        while True:
            row = cur.fetchone()
            if row == None : break
            f.write("%d %s\n"%(i, row[0].lower()))
            i += 1
    
    conn.close()
    
if __name__ == "__main__" :
    ext_atts("192.168.56.102", "root", "1234", 'tpch')