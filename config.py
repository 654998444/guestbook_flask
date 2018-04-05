# -*- encoding:utf-8 -*-

import os

#basedir = os.path.abspath(os.path.dirname(__file__))
basedir = os.getcwd()

class BaseConfig(object):
	UPLOADED_PHOTOS_DEST = basedir + '/uploads'
	DEBUG = True
	SECRET_KEY = 'my secret key'