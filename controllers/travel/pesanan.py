from core.crud import crud

class pesanan(crud):
	table_name = "test"
	active_menu = "travel"
	active_sub = "pesanan"
	title = "Pesanan"

	def __init__(self):
		crud.__init__(self,self.table_name,transaksi=True)
		
		planet = ['mercury',"earth",'mars','uranus','venus','pluto']
		self.fields = [
					{'field':'nama','type':'text','required':1,'search':1},
					{'field':'alamat','type':'text_area','search':1},
					{'field':'planet','type':'combo','rule':'required','value':planet,'search':1},
					{'field':'tanggal','type':'date','required':1},
					{'field':'jumlah','type':'numeric'},
					{'field':'total','type':'currency'},
					{'field':'foto','type':'foto'}
					]
	def p(self,*data):
		self.fields.pop(1)
		return crud.p(self,*data)
	