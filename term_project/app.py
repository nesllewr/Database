import psycopg2
from flask import Flask
from flask import request, session, g, redirect, url_for, abort, render_template, flash
from pypg import helper
import json

# create our little application :)
app = Flask(__name__)
app.config.from_object(__name__)
app.secret_key = "any"

@app.route('/')
def index():
    helper.initialize()
    if session.get("logined") == True:
        return redirect('/main')
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
        session['local'] = result["local"]
        session['domain'] = result["domain"]
        session['name'] = result["name"]
        session['type'] = result["type"]
        return "ok"
    else :
        return "failed"
    
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

if __name__ == "__main__":
    app.run(host='0.0.0.0',debug=True)
