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
	helper.initialize_table()
	return render_template('index.html')

@app.route('/data', methods=["post"])
def select():
	word = request.form["word"]
	result = helper.read_names(word)
	result = json.dumps(result)
	return result

@app.route('/insert')
def insert_func():
	return render_template('insert.html')
	
@app.route('/update')
def update_func():
	return render_template('update.html')
	
@app.route('/delete')
def delete_func():
	return render_template('delete.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0',debug=True)
