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

@app.route("/logout")
def logout():
    session.clear()
    session["logined"] = False
    return redirect("/")

@app.route('/join')
def join():
    return render_template('join.html')

@app.route('/register', methods=['POST'])
def register():
    helper.insert_data(request.form)
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
        session['type'] = result["typeset"]
        session['lat'] = result['lat']
        session['lng'] = result['lng']
        if result["typeset"] == None:
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
            result = helper.get_datatype(session['local'],session['domain'],checkedtype)[0]
            session['hosidx']=result["idx"]
            session['hoslat']=result["lat"]
            session['hoslng']=result['lng']
            print(session['hoslat'], session["hoslng"])
            result = json.dumps(result)
            return '2'
        else :
            session['mode'] = checkedtype            
            result = helper.get_datatype(session['local'],session['domain'],checkedtype)[0]
            session['phaidx']=result['idx']
            session['pharmlat']=result["lat"]
            session['pharmlng']=result['lng']
            result = json.dumps(result)
            return '3'
    else :
        return "failed"

#환자 페이지
@app.route('/patient')
def patient():
    return render_template("patient.html")

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

#예약페이지 관리
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



#병원 페이지
@app.route('/hospital')
def hospital():
    return render_template("hospital.html")

@app.route("/checkhosp", methods=["POST"])
def checkhosp():
    result = helper.check_hospital_info(session['hosidx'])
    result = json.dumps(result)
    return result

@app.route("/selectpat", methods=["POST"])
def selectpat():
    mode = request.form["mode"]
    word = request.form["word"]
    where = request.form["where"]
    if where == "hospital":
        result = helper.select_patient_data(mode,word,where,session['hosidx'])
    elif where == "pharmacy":
        result = helper.select_patient_data(mode,word,where,session['phaidx'])
    result = json.dumps(result)
    return result

@app.route("/delete",methods=["POST"])
def delete_reservation():
    id = request.form['idx']
    print(id)
    helper.delete_data(id)
    return "ok"

#약국 페이지
@app.route('/pharmacy')
def pharmacy():
    return render_template("pharmacy.html")

@app.route("/checkphar", methods=["POST"])
def checkphar():
    result = helper.check_pharmacy_info(session['phaidx'])
    result = json.dumps(result)
    return result


if __name__ == "__main__":
    app.run(host='0.0.0.0',debug=True)