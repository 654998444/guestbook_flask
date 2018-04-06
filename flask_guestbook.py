# -*- encoding: utf-8 -*-

import os
import config
from flask import Flask, render_template, request,\
				 flash, redirect, url_for
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, \
					FileAllowed
from wtforms import SubmitField, StringField, TextAreaField
					 #MultipleFileField
from wtforms.validators import DataRequired, Length
from flask_uploads import UploadSet, configure_uploads, IMAGES,\
	patch_request_class
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import MetaData, Table, Column, String,\
			 Integer, Unicode, DateTime, Text, ForeignKey
from sqlalchemy.orm import sessionmaker, mapper, clear_mappers,\
						relationship
from datetime import datetime

Base = declarative_base()

app = Flask(__name__)
app.config.from_object(config.BaseConfig)
photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)
patch_request_class(app)
bootstrap = Bootstrap(app)


def DBconnect(Guest_object, Photo_object):
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
		Column('time', DateTime, default=datetime.now),
		mysql_default_charset='utf8mb4')  # very very very important in create a table supporting utf8

	photo_table = Table(
		'photo', metadata,
		Column('id', Integer, primary_key=True),
		Column('guestbook_id', Integer, ForeignKey('guestbook.id')),
		Column('image', String(128), nullable=True),
		Column('url', String(256), nullable=True),
		mysql_default_charset='utf8')

#	guest_photo_table = Table(
#		'guestbook_photo', metadata,
#		Column('guestbook_id', None, ForeignKey('guestbook.id'), \
#			primary_key=True),
#		Column('photo_id', None, ForeignKey('photo.id'), \
#			primary_key=True))

	metadata.create_all()  
	# guest_table = Table('guestbook', metadata, autoload=True)  
	# for guest_table already exists in metadata
	clear_mappers()  # clear original mapper in pymysql? or somthing else?
	# build mapper
	mapper(Photo_object, photo_table)
	mapper(Guest_object, guest_table, properties=dict(\
		photos=relationship(Photo, \
			backref='guestbook'))) 

	DBSession = sessionmaker(bind=engine)
	session = DBSession()
	return session

class Guest(object):
	pass

class Photo(object):
	pass

class MessageForm(FlaskForm):
	name = StringField('Name', Length(1,64))
	message = TextAreaField('Message')
	image = FileField('image')
	submit = SubmitField('Submit')


@app.route('/')
def hello_world():
		return render_template('index.html')

@app.route('/manage')
def manage_file():
	files_list = os.listdir(app.config['UPLOADED_PHOTOS_DEST'])
	return render_template('manage.html', files_list=files_list)

@app.route('/open/<filename>')
def open_file(filename):
	file_url = photos.url(filename)
	return render_template('browser.html', file_url=file_url)

@app.route('/delete/<filename>')
def delete_file(filename):
	file_path = photos.path(filename)
	os.remove(file_path)
	return redirect(url_for('manage_file'))

@app.route('/treehole', methods=['GET', 'POST'])
def tree_hole():
	dbsession = DBconnect(Guest, Photo)
	if request.method == 'POST':
		
		data = request.values
		_ = Guest()
		_.name=data['name'].encode('utf-8')  # with question if it is essential or not
		_.message=data['message'].encode('utf-8')
		dbsession.add(_)

		if request.method == 'POST' and 'image' in request.files:
			for filename in request.files.getlist('image'):
				__ = Photo()
				filename = photos.save(filename, \
					name=str(datetime.now()).replace(' ','')+'.')
				file_url = photos.url(filename)
				i = dbsession.query(Guest).count()
				__.guestbook_id = i
				__.image=filename
				__.url=file_url
				dbsession.add(__)

		dbsession.commit()
		flash('submit successfully!', 'success') 
		# flash(message, category) into template			

	items = dbsession.query(Guest.id, Guest.name, Guest.message, \
			Guest.time, Photo.image, Photo.url).outerjoin(Photo).all()
	length = dbsession.query(Guest).count()
	return render_template('treehole.html', 
		length=length, items=items[::-1]) 

if __name__ == '__main__':
		app.run(host='0.0.0.0', port=8000, debug=True, threaded=True)
