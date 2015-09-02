import web
from core.model import model
import paho.mqtt.publish as publish

class quick_count(model):
	def __init__(self):
		model.__init__(self);
		self.topic = "GUEST/qc"
		self.auth = {"username":"guest","password":""}
		
	def input(self,data):
		nomor = data['nomor'];
		content = data['content'];
		
		try:	
			isi = self.parse(content);
			if len(isi)<4: raise Exception("dibawah 4");
			
			sql = "insert into perolehan_suara values(NULL,%s,%s,%s,%s,%s)";
			suara = (isi['suara1'],isi['suara2'],isi['suara3'],isi['suara4']);
			#self.query(sql,(nomor,)+suara);
			isi = '{"suara1":"%s","suara2":"%s","suara3":"%s","suara4":"%s"}'% suara;
			publish.single(self.topic, str(isi),auth=self.auth,client_id="qc_server");
		except Exception as e:
			tipe = str(type(e));
			self.log(tipe+" nomor : "+nomor+" sms : "+content);
			#return type(e)
		
	def parse(self,isi):
		isi = isi.split("#");
		new_isi = {};
		for i in isi:
			i = i.split("=");
			new_isi[i[0]] = i[1];
		return new_isi; 
	
	def log(self,txt):
		q = "insert into log_qc(txt) value(%s)";
		self.query(q,(txt,));