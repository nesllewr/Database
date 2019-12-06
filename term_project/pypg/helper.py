import psycopg2 as pg
import psycopg2.extras
import random
import csv
import xmltodict
import requests

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

def createRandomCode(length):
    string = ""
    code = [
        ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"],
        ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
    ]

    for i in range(length):
        # code[code_type][code_index]
        string += code[random.randint(0, 1)][random.randint(0, 9)]

    return string

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
        
    sql = f'''CREATE TABLE if not exists hospital (
            idx bigserial primary key,
            FK_member integer,
            name varchar(40) NOT NULL,
            docCnt integer NOT NULL,
            subject varchar(30) NOT NULL,
            dist text,
            workingTime text,
            addr text,
            foreign key(FK_member) references member(idx) on delete cascade on update cascade
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
    
    sql = f'''CREATE TABLE if not exists pharmacy (
            idx bigserial primary key,
            FK_member integer,
            name varchar(40) NOT NULL,
            dist text,
            workingTime text,
            foreign key(FK_member) references member(idx) on delete cascade on update cascade
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
    
    sql = f'''CREATE TABLE if not exists rehospital (
            idx bigserial primary key,
            FK_member integer,
            FK_hospital integer,
            rtime timestamp,          
            foreign key(FK_member) references member(idx) on delete cascade on update cascade
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
    
    sql = f'''CREATE TABLE if not exists repharmacy (
            idx bigserial primary key,
            FK_member integer,
            FK_pharmacy integer,
            rtime timestamp,         
            foreign key(FK_member) references member(idx) on delete cascade on update cascade
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
    
    cursor.execute('''select count(*) as cnt from hospital''')
    result = cursor.fetchall()

    # member table
    # name = yadmNm
    # phone = telno
    # local = random code
    # domain = ""
    # passwd = local + clCd
    # lng = XPos
    # lat = YPos
    # type = 1

    # subject = ["내과", "외과", "정형외과", "영상의학과", "마취통증학과", "치과", "안과"]
    # hospital
    # fk_member = 
    # name = yadmNm
    # docCnt = sdrCnt
    # subject = subject random
    # dist = distance
    # workingTime = 휴일/오픈시간(시:분)/클로즈시간(시:분)
    
    opentime = ["9:00", "9:30","10:00","10:30","11:00"]
    endtime = ["16:00","16:30","17:00","17:30","18:00"]

    if result[0][0] <= 0:
        url = 'http://apis.data.go.kr/B551182/hospInfoService/getHospBasisList?serviceKey=XhfOkkV4VVmhR%2F2YKF%2FPmSlse%2F94onDOCkeG%2FrZ6zdShdhyS%2FbpcVXd1F78UWW4NhX4DIDVrltg1YisMdslXaw%3D%3D'
        url += '&format=json'
        url += '&numOfRows=100'
        url += '&radius=5000'
        url += '&yPos=37.5585146'
        url += '&xPos=127.0331892'
        url += '&pageNo=1'

        res = requests.get(url)
        res = xmltodict.parse(res.text)
        res = res.get("response").get("body").get("items").get("item")

        subjects = ["내과", "외과", "정형외과", "영상의학과", "마취통증학과", "치과", "안과"]

        for row in res:
            name = row["yadmNm"]
            phone = row["telno"].replace("-", "")
            local = createRandomCode(6)
            domain = "HYUtermproject"
            passwd = createRandomCode(5) + row["clCd"]
            lng = row["XPos"]
            lat = row["YPos"]
            docCnt = row["sdrCnt"]
            subject = subjects[random.randint(0, 6)]
            dist = row["distance"]
            addr = row["addr"]
            # 0: 일요일 ~ 6: 토요일
            workingTime = str(random.randint(0, 6)) + "/" + opentime[random.randint(0, 4)] + "/" + endtime[random.randint(0, 4)]

            sql = f'''insert into member (name, phone, local, domain, passwd, lng, lat, type) values (\'{name}\', \'{phone}\', \'{local}\', \'{domain}\', \'{passwd}\', \'{lng}\', \'{lat}\', 2)'''
            cursor.execute(sql)
            connect.commit()

            sql = f'''select idx from member where local = \'{(local)}\''''
            cursor.execute(sql)
            idx = cursor.fetchall()[0][0]

            sql = f'''insert into hospital (fk_member, name, docCnt, subject, dist, workingTime, addr) values (\'{idx}\', \'{name}\', \'{docCnt}\', \'{subject}\', \'{dist}\', \'{workingTime}\', \'{addr}\')'''
            cursor.execute(sql)
            connect.commit()

        url = 'http://apis.data.go.kr/B551182/pharmacyInfoService/getParmacyBasisList?serviceKey=XhfOkkV4VVmhR%2F2YKF%2FPmSlse%2F94onDOCkeG%2FrZ6zdShdhyS%2FbpcVXd1F78UWW4NhX4DIDVrltg1YisMdslXaw%3D%3D'
        url += '&format=json'
        url += '&numOfRows=100'
        url += '&radius=5000'
        url += '&yPos=37.5585146'
        url += '&xPos=127.0331892'
        url += '&pageNo=1'

        res = requests.get(url)
        res = xmltodict.parse(res.text)
        res = res.get("response").get("body").get("items").get("item")
        
        for row in res:
            name = row["yadmNm"]
            phone = ""
            if row.get("telno") != None:
                phone = row["telno"].replace("-", "")
            local = createRandomCode(6)
            domain = "HYUtermproject"
            passwd = createRandomCode(5) + row["clCd"]
            lng = row["XPos"]
            lat = row["YPos"]
            dist = row["distance"]
            workingTime = str(random.randint(0, 6)) + "/" + opentime[random.randint(0, 4)] + "/" + endtime[random.randint(0, 4)]

            sql = f'''insert into member (name, phone, local, domain, passwd, lng, lat, type) values (\'{name}\', \'{phone}\', \'{local}\', \'{domain}\', \'{passwd}\', \'{lng}\', \'{lat}\', 3)'''
            cursor.execute(sql)
            connect.commit()

            sql = f'''select idx from member where local = \'{(local)}\''''
            cursor.execute(sql)
            idx = cursor.fetchall()[0][0]

            sql = f'''insert into pharmacy (fk_member, name, dist, workingTime) values (\'{idx}\', \'{name}\',\'{dist}\', \'{workingTime}\')'''
            cursor.execute(sql)
            connect.commit()

    connect.close()

def insert_data(data):
    print(data)
    connect = pg.connect(connect_string)
    cursor = connect.cursor()
    sql = f'''INSERT INTO member (name,phone,local,domain,passwd,lat,lng,type)
            VALUES(\'{data["name"]}\', \'{data["phone"]}\',\'{data["local"]}\',\'{data["domain"]}\',\'{data["passwd"]}\',\'37.5585146\',\'127.0331892\',\'{data["type"]}\');
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

def get_datatype(local, domain):
    connect = pg.connect(connect_string)
    cursor = connect.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    sql = f'''select * from member where local = \'{local}\' AND domain=\'{domain}\''''
    cursor.execute(sql)
    result = cursor.fetchall()[0]
    connect.close()
    return result


def update_data(data,local, domain):
    connect = pg.connect(connect_string)
    cursor = connect.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    sql = f'''UPDATE member SET type = \'{data["type"]}\' where local = \'{local}\' AND domain=\'{domain}\''''
    cursor.execute(sql)
    connect.commit()
    connect.close()
    return "ok"

def select_hospital_data(mode,word,curlat, curlng) :
    connect = pg.connect(connect_string)
    cursor = connect.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    condition = ""
    setlat = "37.5585146"
    setlng = "127.0331892"
    curlat = str(curlat)
    curlng = str(curlng)
    
    if mode == "surround" :
        condition = "(6371*acos(cos(radians('"+curlat+"'))*cos(radians('"+setlat+"'))*cos(radians('"+setlng+"')-radians('"+curlng+"'))+sin(radians('"+curlat+"'))*sin(radians('"+setlat+"')))) <= 5000 "
    elif mode == "subject" :
        condition = " hospital.subject LIKE '%" + word+"%'"
    elif mode == "hospname" : 
        condition = " hospital.name LIKE '%"+ word + "%'"

    sql = " select * from hospital join member on member.idx = hospital.FK_member where" + condition + " limit 10 "
    cursor.execute(sql)
    result = cursor.fetchall()
    connect.close()
    return result



def select_pharmacy_data(mode,word,curlat, curlng) :
    connect = pg.connect(connect_string)
    cursor = connect.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    condition = ""
    setlat = "37.5585146"
    setlng = "127.0331892"
    curlat = str(curlat)
    curlng = str(curlng)
    
    if mode == "surround" :
        condition = "(6371*acos(cos(radians('"+curlat+"'))*cos(radians('"+setlat+"'))*cos(radians('"+setlng+"')-radians('"+curlng+"'))+sin(radians('"+curlat+"'))*sin(radians('"+setlat+"')))) <= 5000 "
    
    sql = " select * from pharmacy join member on member.idx = pharmacy.FK_member where" + condition + " limit 10 "
    cursor.execute(sql)
    result = cursor.fetchall()
    connect.close()
    return result

def check_hospital_info(local,domain):
    connect = pg.connect(connect_string)
    cursor = connect.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    sql = " select * from hospital join member on member.idx = hospital.FK_member where local = '" + local + "' and domain = '" + domain + "'"
    print(sql)
    # sql = " select * , "+condition+ "AS distance from hospital join member on member.idx = hospital.FK_member where local ='" + local + "'AND domain = '"+ domain +"' HAVING distance <= 5000 ORDER BY distance"

    cursor.execute(sql)
    result = cursor.fetchall()[0]
    connect.close()
    return result

def select_patient_data(mode,word,table):
    connect = pg.connect(connect_string)
    cursor = connect.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    condition=""
    if mode == "paname" :
        contion = "WHERE member.name LIKE '%" + word + "%'"
    elif mode == "paphone" :
        contion = "WHERE member.phone LIKE '%" + word + "%'"
    elif mode =="date":
        contion = ""
    else :
        condition =""

    if table =="hospital":
        sql = " select * from rehospital join member on member.idx = rehospital.FK_member "+ condition
    elif table =="pharmacy":
        sql = " select * from repharmacy join member on member.idx = repharmacy.FK_member "+ condition
 
    # sql = " select * , "+condition+ "AS distance from hospital join member on member.idx = hospital.FK_member where local ='" + local + "'AND domain = '"+ domain +"' HAVING distance <= 5000 ORDER BY distance"

    cursor.execute(sql)
    result = cursor.fetchall()[0]
    connect.close()
    return result

def delete_data(index):
    connect = pg.connect(connect_string)
    cursor = connect.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    sql = f'''DELETE FROM rehospital WHERE FK_hospital = \'{index}\';
    '''
    cursor.execute(sql)
    connect.commit()
    connect.close()
    return "ok"


def get_workingtime(index,where):
    connect = pg.connect(connect_string)
    cursor = connect.cursor()
    sql = "SELECT * FROM "+where+" join member on member.idx = "+where+".FK_member WHERE member.idx = "+index+";"
    #sql = f'''SELECT * FROM \'{where}\' join member on member.idx = \'{where}\'.FK_member WHERE member.idx = \'{index}\';'''
    cursor.execute(sql)
    result = cursor.fetchall()
    connect.close()
    return result

def reservation(tablename,hosid, userid, rhtime):
    connect = pg.connect(connect_string)
    cursor = connect.cursor()
    userid = str(userid)
    sql = "INSERT INTO re"+tablename+" (FK_"+tablename+", FK_member,rtime) VALUES('"+ hosid +"','"+userid+"','"+rhtime+"')"
    cursor.execute(sql)
    connect.commit()
    connect.close()
    return "ok"









    