# -*- encoding: utf-8 -*-

from flask import Flask, render_template
from flask_bootstrap import Bootstrap

app = Flask(__name__)
bootstrap = Bootstrap(app)

@app.route('/')
def hello_world():
		return render_template('index.html')

@app.route('/treehole')
def tree_hole():
		return render_template('treehole.html') 

if __name__ == '__main__':
		app.run(host='0.0.0.0', port=8080, debug=True)
