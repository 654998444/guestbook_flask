# -*- encoding: utf-8 -*-

import os
import config
from flask import Flask, render_template, request, flash
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import SubmitField
from flask_uploads import UploadSet, configure_uploads, IMAGES,\
	patch_request_class
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import MetaData, Table, Column, String,\
			 Integer, Unicode, DateTime, Text
from sqlalchemy.orm import sessionmaker, mapper, clear_mappers
from datetime import datetime

Base = declarative_base()

app = Flask(__name__)
app.config.from_object(config.BaseConfig)
photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)
patch_request_class(app)
bootstrap = Bootstrap(app)


def DBconnect(Guest_object):
	engine = create_engine('mysql+pymysql://root:123456@localhost:3306\
			/guestbook?charset=utf8mb4', echo=True)  
	# engine add sql data with default charset utf8

	# initial table guestbook if not exist 
	# !! need to drop table guestbook in mysql if not as same as follows
	metadata = MetaData(bind=engine)
	guest_table = Table(
		'guestbook', metadata,
		Column('id', Integer, primary_key=True),
		Column('name', Text, nullable=False),
		Column('message', Text, nullable=False),
		Column('image', String(64), nullable=True),
		Column('time', DateTime, default=datetime.now),
		mysql_default_charset='utf8mb4')  # very very very important in create a table supporting utf8

	metadata.create_all()  
	# guest_table = Table('guestbook', metadata, autoload=True)  
	# for guest_table already exists in metadata
	clear_mappers()  # clear original mapper in pymysql? or somthing else?
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
		if request.method == 'POST' and 'image' in request.files:
			
			data = request.values
			_ = Guest()
			_.name=data['name'].encode('utf-8')  # with question if it is essential or not
			_.message=data['message'].encode('utf-8')
			filename = photos.save(request.files['image'])
			file_url = photos.url(filename)
			_.image=filename
			dbsession.add(_)
			dbsession.commit()
			flash('submit successfully!', 'success') 
			# flash(message, category) into template			

		items = dbsession.query(Guest).all()
		return render_template('treehole.html', 
			length=len(items), items=items[::-1]) 

if __name__ == '__main__':
		app.run(host='0.0.0.0', port=8080, debug=True, threaded=True)
