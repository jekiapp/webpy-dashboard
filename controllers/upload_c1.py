import time,datetime,string,random
import web,StringIO
from PIL import Image
from core.model import model
class upload_c1(model):
	m = model()
	def __init__(self):
		model.__init__(self)
	
	def index(self,data):
		domain = web.ctx.env['HTTP_ORIGIN']
		
		if not domain=="http://www.radiaranai.com" and\
		 not domain=="http://radiaranai.com":
			return web.notfound()
		return self.upload(data)
	
	def upload(self,data):
		try:
			nomor = data['nomor']

			filedir = './upload'
			filename= self.get_filename()
			buff = StringIO.StringIO()
			buff.write(data['c1_1'])
			buff.seek(0)
			im = Image.open(buff)
			im.save(filedir+"/"+filename,'JPEG')
			c1_1 = filename
		
		
			filename= self.get_filename()
			buff = StringIO.StringIO()
			buff.write(data['c1_2'])
			buff.seek(0)
			im = Image.open(buff)
			im.save(filedir+"/"+filename,'JPEG')
			c1_2 = filename
		
			sql = "update qc_daftar_nomor set c1_1=%s, c1_2=%s where nomor=%s"
			self.query(sql,(c1_1,c1_2,nomor))
			return "<html><body><h3>Upload C1 Model 1 dan 2 berhasil!! </h3><br/>Klik untuk <a href='http://www.radiaranai.com'>[kembali]</a></body></html>"
		except Exception as e:	return str(e)
	def get_filename(self,N=15):
		st = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d_%H_%M_%S')
		s =  ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(N))
		return s+"_"+st
	
