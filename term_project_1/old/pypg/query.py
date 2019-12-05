import psycopg2 as pg
import psycopg2.extras

pgLocal = {
    'host': 'localhost',
    'user': 'postgres',
    'dbname': 'dbTerm',
    'password': 'postgres1!'
}

dbConnect = ' host = {host} user = {user} dbname = {dbname} password = {password} '.format(**pgLocal)

def createTable(tableName, cols):
    print("Create '" + tableName + "' table")
    
    sql = ' create table if not exists "' + tableName + '" ( ' + cols + ' ); '
    
    try:
        connect = pg.connect(dbConnect)
        cursor = connect.cursor()
        cursor.execute(sql)
        connect.commit()
        print("Success create '" + tableName + "' table")
        connect.close()
        
    except pg.OperationalError as e:
        print(e)

def select(data):
    sql = " select " + data["cols"] + " from " + data["table"]
    
    if data.get("where") != None:
        sql += " where " + data.where
    if data.get("limit") != None:
        sql += " limit " + data.limit
        
    print("sql>" + sql)
    
    connect = pg.connect(dbConnect)
    cursor = connect.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    connect.close()
    
    return result

#insert({
#    "tableName": tableName,
#    "cols": cols,
#    "values": values
#})
def insert(data):
    sql = " insert into " + data["tableName"] + " ( " + data["cols"] + " ) values ( " + data["values"] + " ) "
    
    connect = pg.connect(dbConnect)
    cursor = connect.cursor()
    cursor.execute(sql)
    connect.commit()
    connect.close()
    
    return None

#copy({
#    "fileName": fileName,
#    "tableName": tableName,
#    "cols": [column1, column2, ...]
#})
def copy(data):
    print("Copy from '" + data["fileName"] + "' into table '" + data["tableName"] + "'")
    connect = pg.connect(dbConnect)
    cursor = connect.cursor()
    f = open(data["fileName"], "r", encoding = "UTF8")
    next(f)
    cursor.copy_from(f, data["tableName"], sep = ',', columns = data["cols"])
    f.close()
    connect.commit()
    connect.close()
    
    print("Success copy from '" + data["fileName"] + "' into table '" + data["tableName"] + "'")
    
    return None