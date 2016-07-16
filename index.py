#!/usr/bin/python
import sys, os, signal
import web
abspath = os.path.dirname(__file__)
sys.path.append(abspath)
os.chdir(abspath)



import config

web.config.db_host = config.db_host;
web.config.db_user = config.db_user;
web.config.db_password = config.db_password;
web.config.db_name = config.db_name;

web.config.debug = config.debug
if web.config.debug:
	os.kill(os.getpid(), signal.SIGINT)

from route import *

class MyApp(web.application):
	def handle(self):
		if web.config.debug:
			return web.application.handle(self)
		else:
			try:
				return web.application.handle(self)
			except (KeyError,TypeError) as e: #jika parameter yang diharapkan tidak dikirimkan maka notfound
				return web.notfound()

app = MyApp(urls, globals())
if web.config.get('_session') is None:
	db = web.database(dbn='mysql', db=web.config.db_name, user=web.config.db_user, pw=web.config.db_password)
	store = web.session.DBStore(db, 'sessions')
	session = web.session.Session(app, store)
	web.config._session = session

application = app.wsgifunc()