import web, json,locale
from datetime import date

locale.setlocale(locale.LC_ALL,'id_ID.UTF-8')

def cond(condition,res1,res2=""):
	if condition :
		return res1
	else:
		return res2

def get_global():
	func = {
		'cond':cond,
		'base_url':base_url,
		'bulan':bulan
	}
	return func

def base_url():
	return web.ctx.homedomain+web.ctx.homepath

def notfound():
	return web.notfound()

def redirect(url):
	web.seeother(url);

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
	val = val.split("/")
	if len(val) < 3:
		return ""
	return val[2]+"-"+val[1]+"-"+val[0]

def dict_val(fields,data):
		return dict((field['field'],data[field['field']]) for field in fields)

def bulan(i):
	return date(day=1,month=int(i),year=2010).strftime('%B')

def img_url():
	return "/image/"
	
"""
def decode_date(val):
	val = val.split(" ")
	time =""
	if len(val)>1:
		time = val[1]
		val = val[0].split("-")
		return time+" "+val[2]+"/"+val[1]+"/"+val[0]
	else:
		return val[2]+"/"+val[1]+"/"+val[0]
"""