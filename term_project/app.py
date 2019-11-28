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
	return render_template('login.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0',debug=True)
