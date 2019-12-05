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
        url += "&numOfRows=100"
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
            
            idx = query.select({
                "cols": "idx",
                "table": "member",
                "where": "local = '" + data["local"] + "'"
            })[0][0]
            
            query.insert({
                "tableName": "hospital",
                "cols": "FK_member, name, docCnt, subject, stime, etime, holiday",
                "values": "'" + str(idx) + "', '" + data["name"] + "', '" + str(data["docCnt"]) + "', '" + data["subject"] + "', '" + data["stime"] + "', '" + data["etime"] + "', '" + str(data["holiday"]) + "'"
            })