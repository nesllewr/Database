import psycopg2
from flask import Flask
from flask import request, session, g, redirect, url_for, abort, render_template, flash
from pypg import helper
import requests
import json
import xmltodict
import datetime

# create our little application :)
app = Flask(__name__)
app.config.from_object(__name__)
app.secret_key = "any"

app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

@app.after_request
def after_request(response):
    response.headers["Cache-Contorl"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"]=0
    response.headers["Pragm"] = "no-cache"
    return response

@app.route('/')
def index():
    helper.initialize()
    if session.get("logined") == True:
        return redirect('/mode')
    return render_template('login.html')

@app.route('/register', methods=['POST'])
def register():
    # = request.form
    helper.insert_data(request.form)
    # helper.insert_data(data["local"],data["domain"],data["password"],data["name"],data["phone"], data["type"])
    return "ok"

@app.route('/login', methods=['POST'])
def validate():
    result = helper.validate_data(request.form)
    if len(result) > 0 :
        result = result[0]
        session["logined"] = True
        session['idx'] = result['idx']
        session['local'] = result["local"]
        session['domain'] = result["domain"]
        session['name'] = result["name"]
        session['type'] = result["type"]
        if result['lat'] == None :
            session['lat'] = 37.5585146
        else :
            session['lat'] = result['lat']

        if result['lng'] == None :
            session['lng'] = 127.0331892
        else :
            session['lng'] = result['lng']
       
        if result["type"] == None:
            return "type" 
        else :
            return "ok"
    else :
        return "failed"


@app.route('/settype')
def settype():
    return render_template('settype.html')

@app.route('/typesave', methods=['POST'])
def savetype():
    typeset = request.form['type']
    result = helper.update_data(typeset,session['local'],session['domain'])
    session["type"] = result
    return "ok"

@app.route('/mode')
def mode():
    typeset=session['type'].split('/')
    return render_template('mode.html', typeset = typeset)

@app.route('/typecheck', methods=['POST'])
def checktype():
    checkedtype = request.form["checkedtype[]"]
    
    typeset=session['type'].split('/')
    if checkedtype in typeset :
        if checkedtype == '1' :
            session['mode'] = checkedtype
            return '1'
        elif checkedtype == '2' :
            session['mode'] = checkedtype
            result = helper.get_datatype(session['local'],session['domain'])
            session['hoslat']=result["lat"]
            session['hoslng']=result['lng']
#            print(session['hoslat'], session["hoslng"])
#            print(result)
            return '2'
        else :
            session['mode'] = checkedtype            
            result = helper.get_datatype(session['local'],session['domain'])
            session['pharmlat']=result["lat"]
            session['pharmlng']=result['lng']
            return '3'
    else :
        return "failed"

@app.route('/patient')
def patient():
    return render_template("patient.html")

@app.route('/hospital')
def hospital():
    return render_template("hospital.html")

@app.route('/pharmacy')
def pharmacy():
    return render_template("pharmacy.html")

@app.route('/main')
def main():
    return render_template("main.html")

@app.route('/join')
def join():
    return render_template('join.html')

@app.route("/logout")
def logout():
    session.clear()
    session["logined"] = False
    return redirect("/")

@app.route("/data_hospital", methods=["POST"])
def data_hospital():
    result = []
    pageNo = 1
    
    url = 'http://apis.data.go.kr/B551182/hospInfoService/getHospBasisList?serviceKey=XhfOkkV4VVmhR%2F2YKF%2FPmSlse%2F94onDOCkeG%2FrZ6zdShdhyS%2FbpcVXd1F78UWW4NhX4DIDVrltg1YisMdslXaw%3D%3D'
    url += '&format=json'
    url += '&numOfRows=100'
    url += '&radius=5000'
    url += '&yPos='+session['lat']
    url += '&xPos='+session['lng']

    while pageNo <= 5:
        response = requests.get(url + '&pageNo=' + str(pageNo))
        response = xmltodict.parse(response.text)
        response = response.get("response").get("body").get("items").get("item")
        result.append(response)
        if len(response) != 100:
            break
        pageNo = pageNo + 1

    response = json.dumps(result, indent=4)
    return response


@app.route("/data_pharmacy", methods=["POST"])
def data_pharmacy():
    result = []
    pageNo = 1

    url = 'http://apis.data.go.kr/B551182/pharmacyInfoService/getParmacyBasisList?serviceKey=XhfOkkV4VVmhR%2F2YKF%2FPmSlse%2F94onDOCkeG%2FrZ6zdShdhyS%2FbpcVXd1F78UWW4NhX4DIDVrltg1YisMdslXaw%3D%3D'
    url += '&format=json'
    url += '&numOfRows=100'
    url += '&radius=5000'
    url += '&yPos='+session['lat']
    url += '&xPos='+session['lng']

    while pageNo <= 5:
        response = requests.get(url + '&pageNo=' + str(pageNo))
        response = xmltodict.parse(response.text)
        response = response.get("response").get("body").get("items").get("item")
        result.append(response)
        if len(response) != 100:
            break
        pageNo = pageNo + 1

    response = json.dumps(result, indent=4)
    return response

@app.route("/selecthosp", methods=["POST"])
def selecthosp():
    mode = request.form["mode"]
    word = request.form["word"]
    result = helper.select_hospital_data(mode,word,session['lat'], session['lng'])
    result = json.dumps(result)
    return result

@app.route("/selectpharm", methods=["POST"])
def selectpharm():
    mode = request.form["mode"]
    word = request.form["word"]
    result = helper.select_pharmacy_data(mode,word,session['lat'], session['lng'])
    result = json.dumps(result)
    return result

@app.route("/checkhosp", methods=["POST"])
def checkhosp():
    result = helper.check_hospital_info(session['local'], session['domain'])
    result = json.dumps(result)
    return result

@app.route("/selectpat", methods=["POST"])
def selectpat():
    mode = request.form["mode"]
    word = request.form["word"]
    where = request.form["where"]
<<<<<<< HEAD
    print("1")
=======
>>>>>>> d1c87004fb4421f723e373adf29dc674fef9eb27
    result = helper.select_patient_data(mode,word,where)
    print("2")
    result = json.dumps(result)
    return result

@app.route("/delete",methods=["POST"])
def delete_reservation():
    id = request.form['idx']
    print(id)
    helper.delete_data(id)
    return "ok"

@app.route("/reserve", methods=["GET"])
def reserve():
    id = request.form.get("idx")
    where = request.form.get("where")
    return render_template('reserve.html')


@app.route("/selectTime", methods=["POST"])
def getTime():
    print(request.form)
    #id = request.args.get("idx")
    id = request.form["idx"]
    where = request.form["where"]
    
    result = helper.get_workingtime(id,where)
    result = json.dumps(result)
    return result

@app.route("/reservetime",methods=["POST"])
def rhtime():
    where = request.form["where"]
    hosid = request.form["idx"]
    rhtime = request.form['bday'] +" "+request.form['btime']+":00"
    print(rhtime)
    helper.reservation(where,hosid, session['idx'], rhtime)
    return "ok"

@app.route("/prescript", methods=["GET"])
def prescript():
    id = request.form.get("idx")
    return render_template('prescripte.html')



if __name__ == "__main__":
    app.run(host='0.0.0.0',debug=True)
