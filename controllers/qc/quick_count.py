import web
from core.model import model

class quick_count(model):
	def __init__(self):
		model.__init__(self);
		
	def input(self,data):
		nomor = data['nomor'];
		isi = data['content'];
		try:
			isi = self.parse(isi);
			if len(isi)<4: raise;
		except:
			self.log("nomor : "+nomor+" sms : "+isi);
		
	def parse(self,isi):
		isi = isi.split("#");
		new_isi = {};
		for i in isi:
			i = i.split("=");
			new_isi[i[0]] += i[1];
		return new_isi; 
	
	def log(self,txt):
		q = "insert into log_qc(txt) value(%s)";
		self.query(q,(txt,));