#-*- encoding:utf-8 -*-

from flask import Flask, render_template
import pandas as pd

app = Flask(__name__)

@app.route('/')
def hello_world():
		return render_template('testEcharts.html')

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=8090, debug=True)