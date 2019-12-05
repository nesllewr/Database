import psycopg2
from flask import Flask
from pypg import helper
from flask import render_template
#from flask import request, session, g, redirect, url_for, abort, render_template, flash
#import requests
#import json
#import xmltodict
#
## create our little application :)
app = Flask(__name__)
app.config.from_object(__name__)
app.secret_key = "any"
#
@app.route('/')
def index():
    helper.initialize()
    return render_template("index.html")
#def index():
#    helper.initialize()
#    if session.get("logined") == True:
#        return redirect('/mode')
#    return render_template('login.html')
#
#@app.route('/register', methods=['POST'])
#def register():
#    # = request.form
#    helper.insert_data(request.form)
#    # helper.insert_data(data["local"],data["domain"],data["password"],data["name"],data["phone"], data["type"])
#    return "ok"
#
#@app.route('/login', methods=['POST'])
#def validate():
#    result = helper.validate_data(request.form)
#    if len(result) > 0 :
#        result = result[0]
#        session["logined"] = True
#        session['local'] = result["local"]
#        session['domain'] = result["domain"]
#        session['name'] = result["name"]
#        session['type'] = result["type"]
#        if result["type"] == None:
#            return "type" 
#        else :
#            return "ok"
#    else :
#        return "failed"
#
#
#@app.route('/settype')
#def settype():
#    return render_template('settype.html')
#
#@app.route('/typesave', methods=['POST'])
#def savetype():
#    return "ok"
#
#@app.route('/mode')
#def mode():
#    typeset=session['type'].split('/')
#    return render_template('mode.html', typeset = typeset)
#
#@app.route('/typecheck', methods=['POST'])
#def checktype():
#    checkedtype = request.form["checkedtype[]"]
#    print(checkedtype)
#    typeset=session['type'].split('/')
#    if checkedtype in typeset :
#        if checkedtype == '1' :
#            session['mode'] = checkedtype
#            return '1'
#        elif checkedtype == '2' :
#            session['mode'] = checkedtype
#            return '2'
#        else :
#            session['mode'] = checkedtype
#            return '3'
#    else :
#        return "failed"
#
#@app.route('/patient')
#def patient():
#    return render_template("patient.html")
#
#@app.route('/hospital')
#def hospital():
#    return render_template("hospital.html")
#
#@app.route('/pharmacy')
#def pharmacy():
#    return render_template("pharmacy.html")
#
#@app.route('/main')
#def main():
#    return render_template("main.html")
#
#@app.route('/join')
#def join():
#    return render_template('join.html')
#
#@app.route("/logout")
#def logout():
#    session.clear()
#    session["logined"] = False
#    return redirect("/")
#
#@app.route("/data_hospital", methods=["POST"])
#def data():
#    result = []
#    pageNo = 1
#
#    url = 'http://apis.data.go.kr/B551182/hospInfoService/getHospBasisList?serviceKey=XhfOkkV4VVmhR%2F2YKF%2FPmSlse%2F94onDOCkeG%2FrZ6zdShdhyS%2FbpcVXd1F78UWW4NhX4DIDVrltg1YisMdslXaw%3D%3D'
#    url += '&format=json'
#    url += '&numOfRows=100'
#    url += '&radius=5000'
#    url += '&yPos=37.5585146'
#    url += '&xPos=127.0331892'
#
#    while pageNo <= 5:
#        response = requests.get(url + '&pageNo=' + str(pageNo))
#        response = xmltodict.parse(response.text)
#        response = response.get("response").get("body").get("items").get("item")
#        result.append(response)
#        if len(response) != 100:
#            break
#        pageNo = pageNo + 1
#
#    response = json.dumps(result, indent=4)
#    return response
#
#
#@app.route("/data_pharmacy", methods=["POST"])
#def data_pharmacy():
#    result = []
#    pageNo = 1
#
#    url = 'http://apis.data.go.kr/B551182/pharmacyInfoService/getParmacyBasisList?serviceKey=XhfOkkV4VVmhR%2F2YKF%2FPmSlse%2F94onDOCkeG%2FrZ6zdShdhyS%2FbpcVXd1F78UWW4NhX4DIDVrltg1YisMdslXaw%3D%3D'
#    url += '&format=json'
#    url += '&numOfRows=100'
#    url += '&radius=5000'
#    url += '&yPos=37.5585146'
#    url += '&xPos=127.0331892'
#
#    while pageNo <= 5:
#        response = requests.get(url + '&pageNo=' + str(pageNo))
#        response = xmltodict.parse(response.text)
#        response = response.get("response").get("body").get("items").get("item")
#        result.append(response)
#        if len(response) != 100:
#            break
#        pageNo = pageNo + 1
#
#    response = json.dumps(result, indent=4)
#    return response
#
#
if __name__ == "__main__":
    app.run(host='0.0.0.0',debug=True)