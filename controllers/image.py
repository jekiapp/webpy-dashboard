import time,datetime,string,random
import os,web,StringIO
from library.globals import encode_json
from PIL import Image, ImageOps

class image:
	maxsize = 300
	thumbsize = (64,64)

	
	def f(self,filename):
		web.header("Content-type","image/jpeg")
		filedir = './upload'
		fin = open(filedir +'/'+ filename,'r')
		return fin.read()
	
	def upload(self,data=None):
		if not data and not 'file' in data: return web.notfound();
		
		filedir = './upload'
		size = self.thumbsize

		filename= self.get_filename()			
		
		buff = StringIO.StringIO()
		buff.write(data['file'])
		buff.seek(0)
		im = Image.open(buff)
		width,height = im.size
		
		if width>self.maxsize or height>self.maxsize:
			ratio_x = float(format(float(500)/float(width),'.2f'))
			ratio_y = float(format(float(500)/float(height),'.2f'))
			ratio = min(ratio_x,ratio_y)
			width *= ratio
			height *= ratio
	
			im.resize((int(width),int(height)))

		thumb = ImageOps.fit(im, size, Image.ANTIALIAS)
		im.save(filedir+"/"+filename,'JPEG')
		thumb.save(filedir+"/"+filename+"_thumb",'JPEG')

		return encode_json({"url":"/image/f/"+filename,"foto_name":filename})
	
	def delete(self,data):
		filedir = './upload/'
		foto_name = data.foto_name
		try:
			os.remove(filedir+foto_name)
			os.remove(filedir+foto_name+"_thumb")
			return encode_json({"response":"berhasil"});
		except:
			return encode_json({"response":"gagal"});
	
	def get_filename(self,N=15):
		st = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d_%H_%M_%S')
		s =  ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(N))
		return s+"_"+st
	
