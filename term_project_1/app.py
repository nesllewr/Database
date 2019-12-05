import psycopg2
from flask import Flask, render_template, session, request, redirect
from pypg import helper

app = Flask(__name__)
app.config.from_object(__name__)
app.secret_key = "any"

def loginCheck():
    return session.get("logined") == True

@app.route("/")
def index():
    helper.initialize()
    return render_template("index.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/loginok", methods = ["POST"])
def loginok():
    data = request.form
    result = helper.validateAccount(data)
    session["logined"] = result
    return render_template("loginok.html", result = result)

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

if __name__ == "__main__":
    app.run(host='0.0.0.0',debug=True)