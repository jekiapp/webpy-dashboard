import web
from core.model import model
import paho.mqtt.publish as publish

class quick_count(model):
	
	def __init__(self):
		model.__init__(self);
		self.topic = "GUEST/qc"
		self.auth = {"username":"guest","password":""}
	
	def index(self,data):
		try:
			self.nomor = data['sender'];
			self.receiver = data['receiver'];
			self.content = data['content'];
		except Exception:
			self.log("param tidak cocok")
			return web.notfound()
		
		try:
			keyword =  self.content.split(" ")[0].lower();
			self.value = self.content.split(" ")[1].lower()
			self.parse_key(keyword,self.value);
		except Exception as e:
			tipe = str(type(e))
			self.log(tipe+self.receiver+" nomor : "+self.nomor+" sms : "+self.content)

	def parse_key(self,kw,value):
		if kw=="qc":
			self.qc(value)
			
	def qc(self,data):
		""" keyword QC<spasi>suara1#suara2#suara3#suara4"""
		try:
			suara = self.parse(self.value);
			if len(suara)<4: raise Exception("dibawah 4");
			
			sql = "insert into qc_perolehan_suara values(NULL,%s,%s,%s,%s,%s)";
			self.query(sql,(self.nomor,)+suara);
			isi = '{"suara1":"%s","suara2":"%s","suara3":"%s","suara4":"%s"}'% suara;
			publish.single(self.topic, str(isi),auth=self.auth,client_id="qc_server");
		except Exception as e:
			tipe = str(type(e))
			self.log(tipe+self.receiver+" nomor : "+self.nomor+" sms : "+self.content)
			
	
	def parse(self,isi):
		isi = isi.split("#");
		return tuple([i for i in isi]) 
	
	def log(self,txt):
		q = "insert into qc_log(txt) value(%s)";
		self.query(q,(txt,));