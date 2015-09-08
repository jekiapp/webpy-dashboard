import web
from library.globals import get_global
from models.m_menu import m_menu as m1
from models.m_profile import m_profile as m2
from hashlib import sha224

class profile():
	m_menu = m1()
	m_profile = m2()
	def __init__(self):
		self.session = web.config._session
		if self.session.get("nama") == None: 
			raise web.seeother("/login/")
		self.nama = self.session.get("nama")
		self.menu = self.m_menu.get_menu(self.nama)
	
	def index(self,data=None):
		if data and 'update_password' in data:
			data = self.update_password(data)
		view = web.template.frender("views/profile.html")
		res = self.m_profile.get_data(self.nama)
		res['admin'] = 'Ya' if res['admin']==1 else 'Tidak'
		
		content = view(res,data)
		layout = web.template.frender("views/template.html",globals=get_global())
		
		return layout(
			js=[],
			css=['profile'],
			active_menu='profile',
			active_sub = None,
			title=self.nama,
			
			content=content,
			menu=self.menu,
			sub_menu = [],
			username=self.nama
			
		)
	
	def update_password(self,data):
		password = data['password']
		ulangi_password = data['ulangi_password']
		if password!=ulangi_password:
			return "Error Password tidak sama"
		else:
			h = sha224()
			h.update(password)
			passwordhex = h.hexdigest()
			self.m_profile.update_password(self.nama,passwordhex)
			return "Berhasil mengubah password"