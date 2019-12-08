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
            session['hosname']=result['name']
            result = json.dumps(result)
            return '2'
        else :
            session['mode'] = checkedtype            
            result = helper.get_datatype(session['local'],session['domain'],checkedtype)[0]
            session['phaidx']=result['idx']
            session['pharmlat']=result["lat"]
            session['pharmlng']=result['lng']
            session['pharmname']=result['name']
            result = json.dumps(result)
            return '3'
    else :
        return "failed"

#환자 페이지
@app.route('/patient')
def patient():
    return render_template("patient.html")

@app.route('/visited',methods=["post"])
def visited():
    result = helper.get_visited_hos(session['idx'])
    result = json.dumps(result)
    return result


@app.route("/checkpres", methods=["POST"])
def checkpres():
    result = helper.check_prescription_info(session['idx'])
    result = json.dumps(result)
    return result

#환자페이지 - 병원 정보 찾기
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
    #id = request.args.get("idx")
    id = request.form["idx"]
    where = request.form["where"]
    
    result = helper.get_workingtime(id,where)
    result = json.dumps(result)
    return result

@app.route("/reservetime",methods=["POST"])
def reservetime():
    where = request.form["where"]
    hosid = request.form["idx"]
    pre = request.form["pre"]
    rhtime = request.form['bday'] +" "+request.form['btime']+":00"
    helper.reservation(where,hosid, session['idx'], rhtime,pre)
    return "ok"

#환자페이지 - 약국 예약
@app.route('/searchpha',methods=["GET"])
def searchpha():
    id = request.args.get("idx")
    return render_template('searchpha.html',preidx=id)


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

#병원 - 예약 취소(삭제)
@app.route("/delete",methods=["POST"])
def delete_reservation():
    id = request.form['idx']
    helper.delete_data(id)
    return "ok"
 
#병원 - 처방관리
@app.route("/prescript", methods=["GET"])
def prescript():
    id = request.args.get("idx")
    rtime = request.args.get('time')
    result = helper.get_workingtime(id, "member")[0]
    return render_template('prescript.html', name=result[1], hosname=session['hosname'],rtime = rtime)

@app.route("/setprescript",methods=["POST"])
def setprescript():
    helper.set_prescription(request.form,session['hosidx'])
    return "ok"
    
#병원 - 환자방문 이력
@app.route('/visitedpatient',methods=["post"])
def visitedpa():
    result = helper.get_visited_pat(session['hosidx'])
    result = json.dumps(result)
    return result



#약국 페이지
@app.route('/pharmacy')
def pharmacy():
    return render_template("pharmacy.html")

@app.route("/checkphar", methods=["POST"])
def checkphar():
    result = helper.check_pharmacy_info(session['phaidx'])
    result = json.dumps(result)
    return result

@app.route("/prescription", methods=["GET"])
def prescription():
    id = request.args.get("idx")
    checkstate = request.args.get("done")
    result = helper.get_workingtime(id, "prescription")[0]
    return render_template('prescription.html', id = id, checkstate=checkstate, data=result, phaname =session['pharmname'])

@app.route("/changestate",methods=["POST"])
def changestate():
    newstate = request.form['newstate']
    idx = request.form['idx']
    print(newstate,idx)
    result = helper.change_state(newstate,idx)
    return "ok"

@app.route("/completeprescription",methods=["POST"])
def completeprescription():
    newstate = request.form['newstate']
    idx = request.form['idx']
    word = request.form['word']
    result = helper.complete_prescription(newstate,idx,word)
    return "ok"


if __name__ == "__main__":
    app.run(host='0.0.0.0',debug=True)