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


    opentime = ["9:00", "9:30","10:00","10:30","11:00"]
    endtime = ["16:00","16:30","17:00","17:30","18:00"]


    # hospital table
    sql = "CREATE TABLE if not exists hospital (idx bigserial primary key, name varchar(40) NOT NULL,phone varchar(11) NOT NULL, doccnt integer NOT NULL, subject varchar(60) NOT NULL, lat varchar(30),lng varchar(30),addr text, holiday text, opent text, closet text);"

    print("SQL try----------")

    try:
        connect = pg.connect(connect_string)
        cursor = connect.cursor()
        cursor.execute(sql)
        print("SQL Success!")

        connect.commit()
        connect.close()
    except pg.OperationalError as e:
        print(e)


    #pharmacy table
    sql = "CREATE TABLE if not exists pharmacy (idx bigserial primary key, name varchar(40) NOT NULL,phone varchar(11) NOT NULL, lat varchar(30),lng varchar(30),addr text, holiday text, opent text, closet text);"


    print("SQL try----------")

    try:
        connect = pg.connect(connect_string)
        cursor = connect.cursor()
        cursor.execute(sql)
        print("SQL Success!")

        connect.commit()
        connect.close()
    except pg.OperationalError as e:
        print(e)

    #member table
    sql = "CREATE TABLE if not exists member (idx bigserial primary key, name varchar(40) NOT NULL,phone varchar(11) NOT NULL,local varchar(40) NOT NULL,domain varchar(40) NOT NULL,passwd varchar(20) NOT NULL,lat varchar(30),lng varchar(30),typeset varchar(10),hosidx integer,phaidx integer);"

    print("SQL try----------")

    try:
        connect = pg.connect(connect_string)
        cursor = connect.cursor()
        cursor.execute(sql)
        print("SQL Success!")

        connect.commit()
        connect.close()
    except pg.OperationalError as e:
        print(e)

    #reservation hospital table
    sql = f'''CREATE TABLE if not exists rehospital (
            idx bigserial primary key,
            FK_member integer,
            FK_hospital integer,
            rtime timestamp,
            FK_prescription integer,
            checked integer,          
            foreign key(FK_member) references member(idx) on delete cascade on update cascade
            );
        '''

    print("SQL try----------")

    try:
        connect = pg.connect(connect_string)
        cursor = connect.cursor()
        cursor.execute(sql)
        print("SQL Success!")

        connect.commit()
        connect.close()
    except pg.OperationalError as e:
        print(e)
    
    #prescription table
    sql = f'''CREATE TABLE if not exists prescription (
            idx bigserial primary key,
            fk_member integer,
            fk_hospital integer,
            memname varchar(40),
            hosname text,
            issuetime timestamp,
            medtime timestamp,
            medicine text,
            dose text,
            daymed integer,
            totalday integer,
            isdone integer,
            commentline text,
            foreign key(FK_member) references member(idx) on delete cascade on update cascade
            );
        '''

    print("SQL try----------Prescription")

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

    #reservation repharmacy table
    sql = f'''CREATE TABLE if not exists repharmacy (
            idx bigserial primary key,
            FK_prescription integer,
            FK_pharmacy integer,
            rtime timestamp,       
            foreign key(FK_prescription) references prescription(idx) on delete cascade on update cascade
            );
        '''

    print("SQL try----------Repharmacy")

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
        f = open(r'C:\Users\llewr\Database\term_project_v2\customers.csv', 'r', encoding='UTF8')
        next(f) #데이터 첫 줄 넘어가기 (header line)
        cursor.copy_from(f, "member", sep=',', columns=['name', 'phone','local','domain','passwd','lat','lng'])
        #파일 객체 table name seperator(delim) [column옵션] 
        f.close()

        connect.commit()

    #hospital 초기 데이터 넣기 
    cursor.execute('''select count(*) as cnt from hospital''')
    result = cursor.fetchall()
    if result[0][0] <=0:
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
            lng = row["XPos"]
            lat = row["YPos"]
            docCnt = row["sdrCnt"]
            subject = []
            for i in random.sample(range(0, 7), random.randint(1, 7)):
                subject.append(subjects[i])
            # subject = subjects[random.sample(range(0,6),random.randint(0, 6))]
            subject= "/".join(subject)
            dist = row["distance"]
            addr = row["addr"]
            holiday = str(random.randint(0, 6)) 
            opent = opentime[random.randint(0, 4)] 
            closet = endtime[random.randint(0, 4)]

            sql = f'''insert into hospital (name,phone,doccnt,subject,lng,lat,addr,holiday,opent,closet) values ( \'{name}\', \'{phone}\',\'{docCnt}\', \'{subject}\',\'{lng}\',\'{lat}\', \'{addr}\',\'{holiday}\', \'{opent}\', \'{closet}\')'''
            cursor.execute(sql)
            connect.commit()

    
    #pharmacy 초기 데이터 넣기
    
    cursor.execute('''select count(*) as cnt from pharmacy''')
    result = cursor.fetchall()
    if result[0][0] <=0 :    
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
            lng = row["XPos"]
            lat = row["YPos"]
            addr = row["addr"]
            holiday = str(random.randint(0, 6)) 
            opent = opentime[random.randint(0, 4)] 
            closet = endtime[random.randint(0, 4)]

            sql = f'''insert into pharmacy (name,phone,lng,lat,addr,holiday,opent,closet) values ( \'{name}\', \'{phone}\', \'{lng}\',\'{lat}\', \'{addr}\',\'{holiday}\', \'{opent}\', \'{closet}\')'''
            cursor.execute(sql)
            connect.commit()


    connect.close

def insert_data(data):
    connect = pg.connect(connect_string)
    cursor = connect.cursor()
    sql = f'''INSERT INTO member (name,phone,local,domain,passwd,lat,lng)
            VALUES(\'{data["name"]}\', \'{data["phone"]}\',\'{data["local"]}\',\'{data["domain"]}\',\'{data["passwd"]}\',\'{data['lat']}\',\'{data["lng"]}\');
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

def update_data(data,local, domain):
    connect = pg.connect(connect_string)
    cursor = connect.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    #typeset =data.split('/')
    condition = ""
    if '2' in data :
        hosidx = str(random.randint(1,100))
        condition = "', hosidx = '"+ hosidx
    if '3' in data :
        phaidx =  str(random.randint(1,100))
        condition +="', phaidx = '" + phaidx

    sql = "UPDATE member SET typeset ='"+ data + condition +"'where local='"+local+"' AND domain ='"+domain+"'"
    cursor.execute(sql)

    connect.commit()
    connect.close()
    return data

def get_datatype(local, domain,mode):
    connect = pg.connect(connect_string)
    cursor = connect.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    if mode == '2':
        sql = "select hosidx from member where local ='"+local+"' AND domain ='"+domain+"'"
        cursor.execute(sql)
        result = cursor.fetchall()
        if len(result) > 0 : #result가 없는 경우 [0] 접근 불가
            result = result[0]   
            sql = "select * from hospital where hospital.idx ='"+str(result['hosidx'])+"'"
            cursor.execute(sql)
    elif mode == '3':
        sql = "select phaidx from member where local ='"+local+"' AND domain ='"+domain+"'"
        cursor.execute(sql)
        result = cursor.fetchall()
        if len(result) > 0 : #result가 없는 경우 [0] 접근 불가
            result = result[0]   
            sql = "select * from pharmacy where pharmacy.idx ='"+str(result['phaidx'])+"'"
            cursor.execute(sql)
    
    result = cursor.fetchall()
    connect.close()
    return result


#환자페이지
def check_prescription_info(index) :
    connect = pg.connect(connect_string)
    cursor = connect.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    #sql = " select * from prescription join repharmacy on repharmacy.fk_prescription = prescription.idx where fk_member = '" + str(index) + "'"
    sql = "select * from prescription where fk_member  = '" + str(index) + "' order by issuetime DESC "
    cursor.execute(sql)
    result = cursor.fetchall()
    if len(result) > 0 : #result가 없는 경우 [0] 접근 불가
        for row in result:
            row["issuetime"] = row.get("issuetime").strftime("%Y-%m-%d %H:%M:%S")
            if(row.get("rtime")!=None):
                row["rtime"] = row.get("rtime").strftime("%Y-%m-%d %H:%M:%S")
            if(row.get("medtime")!=None):
                row["medtime"] = row.get("medtime").strftime("%Y-%m-%d %H:%M:%S")

    connect.close()
    return result


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

    sql = " select * from hospital where " + condition 
    
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
    elif mode == "pharmname" : 
        condition = " pharmacy.name LIKE '%"+ word + "%'"

    sql = " select * from pharmacy  where " + condition
    cursor.execute(sql)
    result = cursor.fetchall()
    connect.close()
    return result

#병원페이지 : 처방
def set_prescription(data, hosidx):
    connect = pg.connect(connect_string)
    cursor = connect.cursor()
    hosidx = str(hosidx)
    sql = f'''INSERT INTO prescription(fk_member, fk_hospital, memname, hosname, issuetime,  medicine, dose, daymed, totalday, isdone) VALUES (\'{data["paidx"]}\', \'{hosidx}\',\'{data["patient"]}\',\'{data["hosname"]}\',now(),\'{data["medtype"]}\',\'{data["oncemed"]}\',\'{data["daymed"]}\',\'{data["totalmed"]}\', -1);'''
    cursor.execute(sql)
    connect.commit()
    sql = f'''SELECT idx from rehospital where fk_hospital=\'{hosidx}\' AND fk_member =\'{data["paidx"]}\' AND rtime =\'{data['rtime']}\'''' 
    cursor.execute(sql)
    result = cursor.fetchall()[0]
    print(result)
    sql = "UPDATE rehospital SET checked = 1, fk_prescription= '"+ str(result[0])+"' where fk_hospital = '"+ hosidx+"' AND fk_member ='"+data["paidx"]+"' AND rtime = '"+data['rtime']+"'"
    cursor.execute(sql)
    connect.commit()

    connect.close()
    return "ok"

#병원페이지,약국페이지 데이터 가져오기
def check_hospital_info(index):
    connect = pg.connect(connect_string)
    cursor = connect.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    sql = " select * from hospital where idx = '" + str(index) + "'"

    cursor.execute(sql)
    result = cursor.fetchall()
    if len(result) > 0 : #result가 없는 경우 [0] 접근 불가
        result = result[0]    
    connect.close()
    return result

def check_pharmacy_info(index):
    connect = pg.connect(connect_string)
    cursor = connect.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    sql = " select * from pharmacy where idx = '" + str(index) + "'"

    cursor.execute(sql)
    result = cursor.fetchall()
    if len(result) > 0 : #result가 없는 경우 [0] 접근 불가
        result = result[0]    
    connect.close()
    return result


def select_patient_data(mode,word,table,index):
    connect = pg.connect(connect_string)
    cursor = connect.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    condition=""
    
    print(word)
    if table =="hospital":
        if mode == "paname" :
            condition = "AND member.name LIKE '%" + word + "%'"
        elif mode == "paphone" :
            condition = "AND member.phone LIKE '%" + word + "%'"
        elif mode =="date":
            condition = "AND rehospital.rtime between '" + word +" 00:00:00' and '"+word+" 23:59:59' " 
        else :
            condition =""
        sql = " select * from rehospital join member on member.idx = rehospital.FK_member where rehospital.FK_hospital = '" + str(index) + "' AND checked= '0' " + condition
    elif table =="pharmacy":
        if mode == "paname" :
            condition = "AND prescription.memname LIKE '%" + word + "%'"
        elif mode == "paphone" :
            condition = "AND prescription.phone LIKE '%" + word + "%'"
        elif mode =="date":
            condition = "AND repharmacy.rtime between '" + word +" 00:00:00' and '"+word+" 23:59:59' " 
        else :
            condition =""
        
        sql = " select * from repharmacy join prescription on prescription.idx = repharmacy.FK_prescription where repharmacy.FK_pharmacy = '" + str(index) + "'" + condition

    cursor.execute(sql)
    result = cursor.fetchall()
    print(sql)
    if len(result) > 0 : #result가 없는 경우 [0] 접근 불가
        for row in result:
            row["rtime"] = row.get("rtime").strftime("%Y-%m-%d %H:%M:%S")
            if(table=="pharmacy") : 
                row["issuetime"] = row.get("issuetime").strftime("%Y-%m-%d %H:%M:%S")
                if(row.get("medtime")!=None):
                    row["medtime"] = row.get("medtime").strftime("%Y-%m-%d %H:%M:%S")

    else:
        result = []
    connect.close()
    return result
    
def delete_data(time):
    connect = pg.connect(connect_string)
    cursor = connect.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    sql = "DELETE FROM rehospital WHERE rtime = '"+time+"'"
    #sql = f'''DELETE FROM rehospital WHERE FK_member = \'{index}\';
    #'''
    cursor.execute(sql)
    connect.commit()
    connect.close()
    return "ok"

#약국페이지 -처방전 상태 변화
def change_state(newstate,idx):
    connect = pg.connect(connect_string)
    cursor = connect.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    sql = "UPDATE prescription SET isdone='"+newstate +"' WHERE idx = '"+idx+"';"
    result = cursor.execute(sql)
    connect.commit()
    connect.close()
    return result

def complete_prescription(newstate,idx,word):
    connect = pg.connect(connect_string)
    cursor = connect.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    sql = "UPDATE prescription SET  medtime = now(), isdone=3, commentline='"+word+"' WHERE idx = '"+idx+"';"
    result = cursor.execute(sql)
    connect.commit()
    connect.close()
    return result

    
#예약 페이지
def reservation(tablename,hosid, userid, rhtime,preidx):
    connect = pg.connect(connect_string)
    cursor = connect.cursor()
    userid = str(userid)
    if tablename == "hospital":
        sql = "INSERT INTO re"+tablename+" (FK_"+tablename+", FK_member,rtime,checked) VALUES('"+ hosid +"','"+userid+"','"+rhtime+"',0)"
    elif tablename =="pharmacy":
        change_state('0',preidx)
        sql = "INSERT INTO repharmacy( fk_prescription, fk_pharmacy, rtime) VALUES ( "+preidx+", "+hosid+", '"+rhtime+"');"
    cursor.execute(sql)
    connect.commit()
    connect.close() 
    return "ok"

def get_workingtime(index,where):
    connect = pg.connect(connect_string)
    cursor = connect.cursor()
    sql = "SELECT * FROM "+where+" WHERE "+where+".idx = "+index
    #sql = f'''SELECT * FROM \'{where}\' join member on member.idx = \'{where}\'.FK_member WHERE member.idx = \'{index}\';'''
    cursor.execute(sql)
    result = cursor.fetchall()
    connect.close()
    return result


def get_visited_hos(paidx):
    connect = pg.connect(connect_string)
    cursor = connect.cursor()
    sql = "SELECT prescription.hosname,count(hosname) visited FROM prescription where fk_member='"+str(paidx)+"' group by prescription.hosname order by visited DESC;"
    cursor.execute(sql)
    result = cursor.fetchall()
    connect.close()
    return result


def get_visited_pat(hosidx):
    connect = pg.connect(connect_string)
    cursor = connect.cursor()
    sql = "SELECT prescription.memname,count(memname) visited FROM prescription where fk_hospital='"+str(hosidx)+"' group by prescription.memname order by visited DESC;"
    cursor.execute(sql)
    result = cursor.fetchall()
    connect.close()
    return result
