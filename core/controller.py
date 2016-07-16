import web
from library.globals import get_global
from library.lib import base_url
from models.m_menu import m_menu as m1
import time
from json import dumps as jsondumps,loads
from jinja2 import Environment, FileSystemLoader
class controller():
	view = "index"
	action = ""
	image_url = "/image/"
	m_menu = m1()
	
	def __init__(self):
		self.start_time = time.time()
		self.js = []
		self.css = []
		self.param = {}
		self.content = ""
		self.session = web.config._session
		if self.session.get("nama") == None: 
			raise web.seeother("/login/")
		self.username = self.session.get("nama")
		self.setattr()
		self.menu = self.m_menu.get_menu(self.username)
		self.sub_menu = self.m_menu.get_submenu(self.username,self.active_menu)
		self.hak_akses = self.cekHak() 
		if self.hak_akses == 0:
			raise self.notfound()

	def cekHak(self):	
		hak_akses = 0
		for sm in self.sub_menu:
			if sm['url']==self.active_sub:
				hak_akses = int(sm['hak']);
				break
		return hak_akses
	
	
	def render(self,view,param={}):
		view += ".html"
		
		env = Environment(loader=FileSystemLoader('views/'),trim_blocks=True,lstrip_blocks=True)
		env.globals.update(get_global())
		param.update({
					'username':self.username,
					'title':self.title,'action':self.action,'content':self.content,
					'active_menu':self.active_menu,'active_sub':self.active_sub,
					'menu':self.menu,'sub_menu':self.sub_menu,
					'js':self.js,'css':self.css})
		
		full_page = env.get_template(view)\
		.render(
			**param
			)
		elapsed = "<!--"+str(time.time() - self.start_time)+"--!>"
		return full_page+elapsed
	
	def get_elapsed(self):
		return time.time() - self.start_time
	
	def get_menu(self):
		username = self.session.get("nama")
		return self.m_menu.get_menu(username)
	
	def setattr(self):
		setattr(self,'globals',get_global)
		setattr(self,'notfound',web.notfound)
		setattr(self,'base_url',base_url)
		setattr(self,'input',web.input())
		setattr(self,'redirect',web.seeother)
		web.ctx.homepath = "/"+self.active_menu+"/"+self.active_sub+"/"
