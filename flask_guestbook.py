# -*- encoding: utf-8 -*-

from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, Unicode, DateTime, Text
from sqlalchemy.orm import sessionmaker
from datetime import datetime

Base = declarative_base()

app = Flask(__name__)
bootstrap = Bootstrap(app)

def DBconnect():
	engine = create_engine('mysql+pymysql://root:123456@localhost:3306/guestbook?charset=utf8',
		 echo=True)
	DBSession = sessionmaker(bind=engine)
	session = DBSession()
	return session

class guestbook(Base):
	
	__tablename__ = 'guestbook'

	id = Column(Integer, primary_key=True)
	name = Column(Unicode(64), nullable=False)
	message = Column(Text, nullable=False)
	time = Column(DateTime(), default=datetime.now)	
	

@app.route('/')
def hello_world():
		return render_template('index.html')

@app.route('/treehole', methods=['GET', 'POST'])
def tree_hole():
		dbsession = DBconnect()
		if request.method == 'POST':
			data = request.values
			_ = guestbook()
			_.name=data['name']
			_.message=data['message']
			dbsession.add(_)
			dbsession.commit()
		items = dbsession.query(guestbook).all()
		return render_template('treehole.html', 
			length=len(items), items=items[::-1]) 

if __name__ == '__main__':
		app.run(host='0.0.0.0', port=8080, debug=True)
