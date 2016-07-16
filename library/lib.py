import web,json,locale
from datetime import date,datetime
locale.setlocale(locale.LC_ALL,'id_ID.UTF-8')

def base_url():
	return web.ctx.homedomain+web.ctx.homepath

def encode_json(dict):
	web.header('Content-Type', 'application/json')
	return json.dumps(dict)

def titik(val):
	if not val:
		return ""
	tipe = float(val).is_integer()
	format = '%d' if tipe else  '%.2f'
	val = int(val) if tipe else  float(val) 
	return locale.format(format,val,True)

def hilang_titik(val):
	if not val:
		return ""
	return str(locale.atof(val))

def encode_date(val):
	tgl = val.split('-')
	if len(tgl)!=3: raise Exception()
	return datetime(int(tgl[0]),int(tgl[1]),int(tgl[2]))

def bulan(i):
	return date(day=1,month=int(i),year=2010).strftime('%B')

def random_string(size=30):
	import string,random
	chars = string.ascii_lowercase + string.digits
	return ''.join(random.choice(chars) for _ in range(size))