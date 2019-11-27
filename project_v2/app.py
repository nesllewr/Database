import psycopg2
from flask import Flask
from flask import request, session, g, redirect, url_for, abort, render_template, flash
from pypg import helper
import json

# create our little application :)
app = Flask(__name__)
app.config.from_object(__name__)

@app.route('/')
def index():
	helper.initialize()
	return render_template('index.html')

@app.route('/data', methods=["POST"])
def select():
	word = request.form["word"]
	result = helper.read_names(word)
	result = json.dumps(result)
	return result

@app.route('/insert')
def insert_func():
	return render_template('insert.html')

@app.route('/save', methods=["POST"])
def insert_rest():
	name = request.form["name"]
	phone = request.form["phone"]
	print(request.form)
	helper.insert_data(name,phone)

	return "ok"
	
@app.route('/update', methods=["GET"])
def update_func():
	id = request.form.get("idx")
	return render_template('update.html')

@app.route('/selectData', methods=["POST"])
def select_data():
	id = request.form["idx"]
	result = helper.select_data(id)
	result = json.dumps(result)
	return result

@app.route('/modify', methods=["POST"])
def update():
	id = request.form["idx"]
	name = request.form["name"]
	phone = request.form["phone"]
	helper.update_data(id,name,phone)

	return "ok"


@app.route('/del',methods=["POST"])
def delete_func():
	id = request.form["id"]
	helper.delete_data(id)
	return "ok"

if __name__ == "__main__":
    app.run(host='0.0.0.0',debug=True)
