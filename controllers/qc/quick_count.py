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
		isi = data['content'];
		try:	
			isi = self.parse(isi);
			if len(isi)<4: raise;
			
			sql = "insert into perolehan_suara values(%s,%s,%s,%s,%s)";
			self.query(sql,(nomor,isi['1'],isi['2'],isi['3'],isi['4']));
			isi = '{"suara_1":"%s","suara_2":"%s","suara_3":"%s","suara_4":"%s"}'% (isi['1'],isi['2'],isi['3'],isi['4']);
			publish.single(self.topic, str(isi),auth=self.auth,client_id="qc_server");
		except Exception as e:
			self.log(str(e)+" nomor : "+nomor+" sms : "+isi);
		
		
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