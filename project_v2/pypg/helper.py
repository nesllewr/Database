import psycopg2 as pg
import psycopg2.extras
import csv

pg_local = {
    'host':"localhost",
    'user':"postgres",
    'dbname':"dbA2",
    'password':"Ska25zns!"
}

#postgres://dbuser:1234@postgres/dbapp
#localhost == 127.0.0.1
#postgres://postgress:비번@127.0.0.1/postgres

db_connector = pg_local 

connect_string = "host={host} user={user} dbname={dbname} password={password}".format(
    **db_connector)

# def read_tables(word):
def read_names(word):
    connect = pg.connect(connect_string)
    cursor = connect.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    sql = f'''SELECT * FROM phonebook WHERE name like \'{word}%\';
    '''
    cursor.execute(sql)
    result = cursor.fetchall()
    connect.close()
    return result

def read_phone(word):
    connect = pg.connect(connect_string)
    cursor = connect.cursor()
    sql = f'''SELECT * FROM phonebook WHERE phone like \'{word}%\';
    '''
    cursor.execute(sql)
    result = cursor.fetchall()
    connect.close()
    return result

def insert_data(name,phone):
    connect = pg.connect(connect_string)
    cursor = connect.cursor()
    sql = f'''INSERT INTO phonebook (name,phone)
            VALUES(\'{name}\', \'{phone}\');
    '''
    cursor.execute(sql)
    connect.commit()
    connect.close()
    return "ok"

def update_data(index, name, phone):
    connect = pg.connect(connect_string)
    cursor = connect.cursor()
    sql = f'''UPDATE phonebook SET name = \'{name}\', phone = \'{phone}\'
            WHERE idx = \'{index}\';
    '''
    cursor.execute(sql)
    connect.commit()
    connect.close()
    return "ok"

def select_data(index):
    connect = pg.connect(connect_string)
    cursor = connect.cursor()
    sql = f'''SELECT * FROM phonebook WHERE idx = \'{index}\';'''
    cursor.execute(sql)
    result = cursor.fetchall()
    connect.close()

    return result


def delete_data(index):
    connect = pg.connect(connect_string)
    cursor = connect.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    sql = f'''DELETE FROM phonebook WHERE idx = \'{index}\';
    '''
    cursor.execute(sql)
    connect.commit()
    connect.close()
    return "ok"

# update phonebook set name = ..., phone = ... where idx = ...
# insert into phonebook (name, phone) values (..., ...)

def initialize_table():

    sql = f'''CREATE TABLE if not exists phonebook (
            idx bigserial primary key,
            name varchar(40) NOT NULL,
            phone varchar(11) NOT NULL
            );
        '''
    
    try:
        connect = pg.connect(connect_string)
        cursor = connect.cursor()
        cursor.execute(sql)

        connect.commit()
        connect.close()
    except pg.OperationalError as e:
        print(e)
    
    connect = pg.connect(connect_string)
    cursor = connect.cursor()
    cursor.execute('''select count(*) as cnt from phonebook''')
    result = cursor.fetchall()

    if result[0][0] <= 0 :
        f = open('contact.csv','r',encoding='utf-8')
        reader = csv.reader(f)
        i = 0
        for line in reader:
            if i == 0:
                i = i + 1
                continue

            sql = f'''insert into phonebook (name, phone) values ('{line[0]}', '{line[1]}')'''
            cursor.execute(sql)
            connect.commit()
        f.close()
    
    connect.close()