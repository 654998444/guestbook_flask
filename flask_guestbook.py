# -*- encoding: utf-8 -*-

from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import MetaData, Table, Column, String,\
			 Integer, Unicode, DateTime, Text
from sqlalchemy.orm import sessionmaker, mapper, clear_mappers
from datetime import datetime

Base = declarative_base()

app = Flask(__name__)
bootstrap = Bootstrap(app)

def DBconnect(Guest_object):
	engine = create_engine('mysql+pymysql://root:123456@localhost:3306\
			/guestbook?charset=utf8', echo=True)

	# initial table guestbook if not exist
	metadata = MetaData(bind=engine)
	guest_table = Table(
		'guestbook', metadata,
		Column('id', Integer, primary_key=True),
		Column('name', Text, nullable=False),
		Column('message', Text, nullable=False),
		Column('time', DateTime, default=datetime.now),
		mysql_default_charset='utf8')  # very very very important in create a table supporting utf8

	metadata.create_all()
	clear_mappers()
	mapper(Guest_object, guest_table)  # build mapper

	DBSession = sessionmaker(bind=engine)
	session = DBSession()
	return session

class Guest(object):
	pass

@app.route('/')
def hello_world():
		return render_template('index.html')

@app.route('/treehole', methods=['GET', 'POST'])
def tree_hole():
		dbsession = DBconnect(Guest)
		if request.method == 'POST':
			data = request.values
			_ = Guest()
			_.name=data['name'].encode('utf-8')  # with question if it is essential or not
			_.message=data['message'].encode('utf-8')
			dbsession.add(_)
			dbsession.commit()
		items = dbsession.query(Guest).all()
		return render_template('treehole.html', 
			length=len(items), items=items[::-1]) 

if __name__ == '__main__':
		app.run(host='0.0.0.0', port=8080, debug=True, threaded=True)
