import web
from library.globals import *
from models.m_menu import m_menu as m1

class controller():
	view = "index"
	action = ""
	image_url = "/image/"
	m_menu = m1()
	
	def __init__(self):
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
			raise notfound()

	def cekHak(self):	
		hak_akses = 0
		for sm in self.sub_menu:
			if sm['url']==self.active_sub:
				hak_akses = int(sm['hak']);
				break
		return hak_akses

	def render(self,template,param={}):
		
		template += ".html"
		view = web.template.frender("views/"+template,globals=self.globals())
		param.update({'content':self.content});
		content = view(**param)
		layout = web.template.frender("views/template.html",globals=self.globals())
		
		return layout(
			js=self.js,
			css=self.css,
			active_menu=self.active_menu,
			active_sub = self.active_sub,
			title=self.title,
			action=self.action,
			content=content,
			menu=self.menu,
			sub_menu = self.sub_menu,
			username=self.username
		)
	
	def get_menu(self):
		username = self.session.get("nama")
		return self.m_menu.get_menu(username)
	
	def setattr(self):
		setattr(self,'globals',get_global)
		setattr(self,'notfound',notfound)
		setattr(self,'base_url',base_url)
		setattr(self,'redirect',redirect)
		
