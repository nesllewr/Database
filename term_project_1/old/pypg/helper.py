import requests
import xmltodict
import random
from pypg import function
from pypg import query

def initialize():
    # create member table
    cols  = " idx bigserial primary key, "
    cols += " name varchar(40) not null, "
    cols += " phone varchar(20) not null, "
    cols += " local varchar(40) not null, "
    cols += " domain varchar(40) not null, "
    cols += " pw varchar(20) not null, "
    cols += " lat varchar(30), "
    cols += " lng varchar(30), "
    cols += " type varchar(10) "
    
    query.createTable("member", cols)
    
    # create hospital table
    cols  = " idx bigserial primary key, "
    cols += " FK_member integer, "
    cols += " name varchar(40) not null, "
    cols += " docCnt integer not null, "
    cols += " subject varchar(30) not null, "
    cols += " stime varchar(20), "
    cols += " etime varchar(20), "
    cols += " holiday integer, "
    cols += " foreign key(FK_member) "
    cols += " references member(idx) "
    cols += " on delete cascade "
    cols += " on update cascade "
    
    query.createTable("hospital", cols)
    
    # create pharmacy table
    cols  = " idx bigserial primary key, "
    cols += " FK_member integer, "
    cols += " name varchar(40) not null, "
    cols += " stime varchar(20), "
    cols += " etime varchar(20), "
    cols += " holiday integer, "
    cols += " foreign key(FK_member) "
    cols += " references member(idx) "
    cols += " on delete cascade "
    cols += " on update cascade "
    
    query.createTable("pharmacy", cols)
    
    # import customer.csv(member data) if member table is empty
    memberCnt = query.select({
        "cols": "count(*) as cnt",
        "table": "member"
    })[0][0]
    
    if memberCnt <= 0:
        query.copy({
            "fileName": "customers.csv",
            "tableName": "member",
            "cols": ["name", "phone", "local", "domain", "pw", "lat", "lng"]
        })
    
    # import hospital data from API if hospital table is empty
    hospitalCnt = query.select({
        "cols": "count(*) as cnt",
        "table": "hospital"
    })[0][0]
    
    if hospitalCnt <= 0:
        subjects = ["내과", "외과", "정형외과", "영상의학과", "마취통증학과", "치과", "안과"]
        stime = ["9:00", "9:30","10:00","10:30","11:00"]
        etime = ["16:00","16:30","17:00","17:30","18:00"]
        
        url  = "http://apis.data.go.kr/B551182/hospInfoService/getHospBasisList?serviceKey=XhfOkkV4VVmhR%2F2YKF%2FPmSlse%2F94onDOCkeG%2FrZ6zdShdhyS%2FbpcVXd1F78UWW4NhX4DIDVrltg1YisMdslXaw%3D%3D"
        url += "&numOfRows=2"
        url += "&radius=5000"
        url += "&yPos=37.5585146"
        url += "&xPos=127.0331892"
        url += "&pageNo=1"

        res = requests.get(url)
        res = xmltodict.parse(res.text)
        res = res.get("response").get("body").get("items").get("item")

        for row in res:
            data = {
                "name": row["yadmNm"],
                "phone": row["telno"],
                "local": function.createRandomCode(6),
                "domain": "hospital",
                "pw": function.createRandomCode(5) + row["clCd"],
                "lng": row["XPos"],
                "lat": row["YPos"],
                "docCnt": row["sdrCnt"],
                "subject": subjects[random.randint(0, 6)],
                "stime": stime[random.randint(0, 4)],
                "etime": etime[random.randint(0, 4)],
                "holiday": random.randint(0, 6)
            }
            
            query.insert({
                "tableName": "member",
                "cols": "name, phone, local, domain, pw, lng, lat, type",
                "values": "'" + data["name"] + "', '" + data["phone"] + "', '" + data["local"] + "', '" + data["domain"] + "', '" + data["pw"] + "', '" + data["lng"] + "', '" + data["lat"] + "', 2"
            })
        

#
#def initialize():
#
#    # member table
#    # name = yadmNm
#    # phone = telno
#    # local = random code
#    # domain = ""
#    # passwd = local + clCd
#    # lng = XPos
#    # lat = YPos
#    # type = 1
#
#    # subject = ["내과", "외과", "정형외과", "영상의학과", "마취통증학과", "치과", "안과"]
#    # hospital
#    # fk_member = 
#    # name = yadmNm
#    # docCnt = sdrCnt
#    # subject = subject random
#    # dist = distance
#    # workingTime = 휴일/오픈시간(시:분)/클로즈시간(시:분)
#    
#    opentime = ["9:00", "9:30","10:00","10:30","11:00"]
#    endtime = ["16:00","16:30","17:00","17:30","18:00"]
#
#    if result[0][0] <= 0:
#        url = 'http://apis.data.go.kr/B551182/hospInfoService/getHospBasisList?serviceKey=XhfOkkV4VVmhR%2F2YKF%2FPmSlse%2F94onDOCkeG%2FrZ6zdShdhyS%2FbpcVXd1F78UWW4NhX4DIDVrltg1YisMdslXaw%3D%3D'
#        url += '&format=json'
#        url += '&numOfRows=100'
#        url += '&radius=5000'
#        url += '&yPos=37.5585146'
#        url += '&xPos=127.0331892'
#        url += '&pageNo=1'
#
#        res = requests.get(url)
#        res = xmltodict.parse(res.text)
#        res = res.get("response").get("body").get("items").get("item")
#
#        subjects = ["내과", "외과", "정형외과", "영상의학과", "마취통증학과", "치과", "안과"]
#
#        for row in res:
#            name = row["yadmNm"]
#            phone = row["telno"].replace("-", "")
#            local = createRandomCode(6)
#            domain = "HYUtermproject"
#            passwd = createRandomCode(5) + row["clCd"]
#            lng = row["XPos"]
#            lat = row["YPos"]
#            docCnt = row["sdrCnt"]
#            subject = subjects[random.randint(0, 6)]
#            dist = row["distance"]
#            # 0: 일요일 ~ 6: 토요일
#            workingTime = str(random.randint(0, 6)) + "/" + opentime[random.randint(0, 4)] + "/" + endtime[random.randint(0, 4)]
#
#            sql = f'''insert into member (name, phone, local, domain, passwd, lng, lat, type) values (\'{name}\', \'{phone}\', \'{local}\', \'{domain}\', \'{passwd}\', \'{lng}\', \'{lat}\', 2)'''
#            cursor.execute(sql)
#            connect.commit()
#
#            sql = f'''select idx from member where local = \'{(local)}\''''
#            cursor.execute(sql)
#            idx = cursor.fetchall()[0][0]
#
#            sql = f'''insert into hospital (fk_member, name, docCnt, subject, dist, workingTime) values (\'{idx}\', \'{name}\', \'{docCnt}\', \'{subject}\', \'{dist}\', \'{workingTime}\')'''
#            cursor.execute(sql)
#            connect.commit()
#
#        url = 'http://apis.data.go.kr/B551182/pharmacyInfoService/getParmacyBasisList?serviceKey=XhfOkkV4VVmhR%2F2YKF%2FPmSlse%2F94onDOCkeG%2FrZ6zdShdhyS%2FbpcVXd1F78UWW4NhX4DIDVrltg1YisMdslXaw%3D%3D'
#        url += '&format=json'
#        url += '&numOfRows=100'
#        url += '&radius=5000'
#        url += '&yPos=37.5585146'
#        url += '&xPos=127.0331892'
#        url += '&pageNo=1'
#
#        res = requests.get(url)
#        res = xmltodict.parse(res.text)
#        res = res.get("response").get("body").get("items").get("item")
#        
#        for row in res:
#            name = row["yadmNm"]
#            phone = ""
#            if row.get("telno") != None:
#                phone = row["telno"].replace("-", "")
#            local = createRandomCode(6)
#            domain = "HYUtermproject"
#            passwd = createRandomCode(5) + row["clCd"]
#            lng = row["XPos"]
#            lat = row["YPos"]
#            dist = row["distance"]
#            workingTime = str(random.randint(0, 6)) + "/" + opentime[random.randint(0, 4)] + "/" + endtime[random.randint(0, 4)]
#
#            sql = f'''insert into member (name, phone, local, domain, passwd, lng, lat, type) values (\'{name}\', \'{phone}\', \'{local}\', \'{domain}\', \'{passwd}\', \'{lng}\', \'{lat}\', 3)'''
#            cursor.execute(sql)
#            connect.commit()
#
#            sql = f'''select idx from member where local = \'{(local)}\''''
#            cursor.execute(sql)
#            idx = cursor.fetchall()[0][0]
#
#            sql = f'''insert into pharmacy (fk_member, name, dist, workingTime) values (\'{idx}\', \'{name}\',\'{dist}\', \'{workingTime}\')'''
#            cursor.execute(sql)
#            connect.commit()
#
#    connect.close()
#
#def insert_data(data):
#    print(data)
#    connect = pg.connect(connect_string)
#    cursor = connect.cursor()
#    sql = f'''INSERT INTO member (name,phone,local,domain,passwd,type)
#            VALUES(\'{data["name"]}\', \'{data["phone"]}\',\'{data["local"]}\',\'{data["domain"]}\',\'{data["passwd"]}\',\'{data["type"]}\');
#    '''
#    cursor.execute(sql)
#    connect.commit()
#    connect.close()
#    return "ok"
#
#def validate_data(data):
#    connect = pg.connect(connect_string)
#    cursor = connect.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
#    sql = f'''select * from member where concat(local, \'@\', domain) = \'{data["email"]}\' AND passwd = \'{data["password"]}\''''
#    cursor.execute(sql)
#    result = cursor.fetchall()
#    connect.close()
#    return result
#
#def update_data(data,local, domain):
#    connect = pg.connect(connect_string)
#    cursor = connect.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
#    sql = f'''UPDATE member SET type = \'{data["type"]}\' where local = \'{local}\' AND domain=\'{domain}\''''
#    cursor.execute(sql)
#    connect.commit()
#    connect.close()
#    return "ok"
