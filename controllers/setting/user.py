from core.crud import crud
from models.m_user import m_user
from hashlib import sha224

class user(crud):
	table_name = "user"
	active_menu = "setting"
	title = "User"
	
	def __init__(self):
		crud.__init__(self,self.table_name,transaksi=False)
		self.model = m_user()
		self.fields = [
					{'field':'username','type':'text','required':1,'search':1},
					{'field':'nama','type':'text','required':1,'search':1},
					{'field':'password','type':'password','required':1},
					{'field':'ulangi_password','type':'password','required':1},
					{'field':'admin','type':'admin','value':[{'key':'0','val':'Tidak'},{'key':'1','val':'Ya'}]},
					{'field':'foto','type':'foto'}
					]
	
	def p(self,*par):
		self.fields.append({'field':'last-seen','type':'datetime','title':'Terakhir Login'})
		del self.fields[2]
		del self.fields[2]
		
		return crud.p(self,*par)
	
	def add(self,*par):
		self.add_state = True
		return crud.add(self,*par)
	
	def edit(self,id,data=None):
		self.add_state = False
		self.view = 'setting/user'
		self.css.append('user')
		self.js.append('user')
		self.fields.pop(2)
		self.fields.pop(2)

		if data and 'reset_password' in data:
			return self.reset_password()
		elif data and 'simpan_hak' in data:
			self.simpan_hak(id,data)
			self.redirect(self.base_url()+"edit/"+id+"/")
		menu = self.model.get_menu(id)
		self.param.update({"menu":menu})
		return crud.edit(self,id,data)
	
	def simpan_hak(self,id,data):
		menu = self.model.get_menu(id)
		hak = {}
		for m in menu:
			for s in menu[m]:
				hak = data[str(s['id'])]
				self.model.update_hak(id,s['id'],hak)
	
	def reset_password(self):
		import random,string
		from library.globals import encode_json
		
		password = ''.join(random.SystemRandom().choice(string.ascii_uppercase) for _ in range(5))
		h = sha224()
		h.update(password)
		passwordhex = h.hexdigest()
		self.model.update_password(id,passwordhex)
		return encode_json({"password":password})
	
	def validate(self,data):
		valid_value,error = crud.validate(self,data)
		
		if self.add_state and data['password'] != data['ulangi_password']:
			error.append("Error : Password tidak sama")
		elif self.add_state:
			h = sha224()
			h.update(valid_value['password'])
			valid_value['password'] = h.hexdigest()
		
		if not error and self.add_state: self.fields.pop(3)
		return valid_value,error 
	
	def get_cell(self,val,tipe):
		if tipe == 'admin':
			return 'Ya' if val==1 else 'Tidak'
		else: return crud.get_cell(self,val,tipe)
	
	def form_admin(self,*p):
		return crud.form_combo(self,*p)
	
	def form_password(self,field,val):
		return "<div><div class='label'>"+self.colName(field)+self.get_required(field)+" :</div>"+\
			"<div><input id='f_"+field['field']+"' name='"+field['field']+"' type='password' class='text-medium' /></div></div>"
	