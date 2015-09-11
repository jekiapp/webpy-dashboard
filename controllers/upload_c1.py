import time,datetime,string,random
import web,StringIO
from PIL import Image

class upload_c1:
	
	def index(self,data):
		web.header('Access-Control-Allow-Origin',      '*')
		web.header('Access-Control-Allow-Credentials', 'true')
		
		return "OK!"
	
	def upload(self,data=None):
		if not data and not 'file' in data \
		and not 'nomor' in data: return web.notfound();
		
		
		filedir = './upload'
		filename= self.get_filename()			
		
		buff = StringIO.StringIO()
		buff.write(data['file'])
		buff.seek(0)
		im = Image.open(buff)
		
		im.save(filedir+"/"+filename,'JPEG')
		
	def get_filename(self,N=15):
		st = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d_%H_%M_%S')
		s =  ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(N))
		return s+"_"+st
	