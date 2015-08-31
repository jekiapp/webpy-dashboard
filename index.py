#!/usr/bin/python
import sys, os, exceptions, traceback,signal
import web

web.config.debug = True
if web.config.debug:
	os.kill(os.getpid(), signal.SIGINT)
abspath = os.path.dirname(__file__)
sys.path.append(abspath)
os.chdir(abspath)

web.config.db_host = 'localhost';
web.config.db_user = 'root';
web.config.db_password = 'jaki';
web.config.db_database = 'radiaranai';

import controllers.index as con
urls = (
	'/(.*)', 'index',
) 

class index:
	def GET(self,url=""):
		
		if not url:
			return con.index().index()
		routes = url.split('/')
		
		module_name = "controllers."
		for route in routes:
			if not route :
				continue
			module_name += route+"."
		module_name = module_name[:-1]
		
		args = []
		not_found = True
		controller_module = None
		class_name = ""
		while not_found :
			try:
				class_name = str(module_name.split(".")[-1])
				controller_module = __import__(module_name.lower(), globals(), locals(),class_name)
			except ImportError:
				split = module_name.split(".")
				args.append(split.pop())
				if len(split)==1: return web.notfound()
				module_name = ".".join(split)
			except Exception as e: return e
			else:
				not_found = False
				
		web.ctx.homepath = "/"+"".join([module_name.split('.')[x]+"/" for x in range(1,len(module_name.split('.')))])
		
		controller_instance = getattr(controller_module, class_name)()
		if not args:
			func_name = "index"
		else:
			func_name = args.pop()
		
		args.reverse()
		try:
			return getattr(controller_instance,func_name)(*args)
		except Exception:
			if web.config.debug:
				return str(traceback.format_exc())
			else:
				return web.notfound()
	
	def POST(self,url):
		if not url:
			return web.notfound()
		
		routes = url.split('/')
		module_name = "controllers."
		for route in routes:
			if not route :
				continue
			module_name += route+"."
		module_name = module_name[:-1]
		
		args = []
		not_found = True
		controller_module = None
		class_name = ""
		while not_found :
			try:
				class_name = str(module_name.split(".")[-1])
				controller_module = __import__(module_name.lower(), globals(), locals(),class_name)
			except ImportError:
				split = module_name.split(".")
				args.append(split.pop())
				if len(split)==1: return web.notfound()
				module_name = ".".join(split)
			else:
				not_found = False
		web.ctx.homepath = "/"+"".join([module_name.split('.')[x]+"/" for x in range(1,len(module_name.split('.')))])
		controller_instance = getattr(controller_module, class_name)()
		if not args:
			func_name = "index"
		else:
			func_name = args.pop()
		
		args.reverse()
		data = web.input()
		args.append(data)
		try:
			return getattr(controller_instance,func_name)(*args)
		except Exception:
			if web.config.debug:
				return str(traceback.format_exc())
			else:
				return web.notfound()


app = web.application(urls, globals())


if web.config.get('_session') is None:
	curdir = os.path.dirname(__file__)
	session = web.session.Session(app, web.session.DiskStore(os.path.join(curdir,'sessions')),)
	web.config._session = session

application = app.wsgifunc()
