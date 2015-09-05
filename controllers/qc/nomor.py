from core.crud import crud
from MySQLdb import IntegrityError

class nomor(crud):
	table_name = "qc_daftar_nomor"
	active_menu = "qc"
	active_sub = "nomor"
	title = "Daftar Nomor"
	def __init__(self):
		crud.__init__(self,self.table_name)
		
		self.fields = (
					{'field':'nama','type':'text','required':1},
					{'field':'nomor','type':'text','required':1},
					{'field':'keterangan','type':'text_area'},
					{'field':'foto','type':'foto'}
					)
		self.model.set_table(self.table_name)
	
	def add(self,data=None):
		try:
			return crud.add(self,data)
		except IntegrityError as i:
			cont = self.get_error("Error : Nomor sudah ada")
			self.content += cont
			return crud.add(self,data)
	
	def edit(self,id,data=None):
		try:
			return crud.edit(self,id,data)
		except IntegrityError as i:
			cont = self.get_error("Error : Nomor sudah ada")
			self.content += cont
			return crud.edit(self,id)