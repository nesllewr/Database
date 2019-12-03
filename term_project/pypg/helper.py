import psycopg2 as pg
import psycopg2.extras
import csv

pg_local = {
    'host':"localhost",
    'user':"postgres",
    'dbname':"dbTerm",
    'password':"Ska25zns!"
}

#postgres://dbuser:1234@postgres/dbapp
#localhost == 127.0.0.1
#postgres://postgress:빕번@127.0.0.1/postgres

db_connector = pg_local 

connect_string = "host={host} user={user} dbname={dbname} password={password}".format(
    **db_connector)

def initialize():
    # Initialize table
    sql = f'''CREATE TABLE if not exists member (
            idx bigserial primary key,
            name varchar(40) NOT NULL,
            phone varchar(11) NOT NULL,
            local varchar(40) NOT NULL,
            domain varchar(40) NOT NULL,
            passwd varchar(20) NOT NULL,
            lat varchar(30),
            lng varchar(30),
            type varchar(10) 
            );
        '''
    print("SQL Try!")
    
    try:
        connect = pg.connect(connect_string)
        cursor = connect.cursor()
        cursor.execute(sql)
        print("SQL Success!")

        connect.commit()
        connect.close()
    except pg.OperationalError as e:
        print(e)
    
    connect = pg.connect(connect_string)
    cursor = connect.cursor()
    cursor.execute('''select count(*) as cnt from member''')
    result = cursor.fetchall()

    #table에 data가 없는 경우 초기 데이터 contact.csv을 table에 copy
    if result[0][0] <= 0 :
        f = open(r'C:\Users\llewr\Database\term_project\customers.csv', 'r', encoding='UTF8')
        cursor.copy_from(f, "member", sep=',', columns=['name', 'phone','local','domain','passwd','lat','lng'])
        #파일 객체 table name seperator(delim) [column옵션] 
        f.close()

        connect.commit()
    
    connect.close()

def insert_data(data):
    print(data)
    connect = pg.connect(connect_string)
    cursor = connect.cursor()
    sql = f'''INSERT INTO member (name,phone,local,domain,passwd,type)
            VALUES(\'{data["name"]}\', \'{data["phone"]}\',\'{data["local"]}\',\'{data["domain"]}\',\'{data["passwd"]}\',\'{data["type"]}\');
    '''
    cursor.execute(sql)
    connect.commit()
    connect.close()
    return "ok"

def validate_data(data):
    connect = pg.connect(connect_string)
    cursor = connect.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    sql = f'''select * from member where concat(local, \'@\', domain) = \'{data["email"]}\' AND passwd = \'{data["password"]}\''''
    cursor.execute(sql)
    result = cursor.fetchall()
    connect.close()
    return result
