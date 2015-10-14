from core.crud import crud
import web

class surveyor(crud):
	active_menu = "qc"
	active_sub = "surveyor"
	title = "Surveyor"
	def __init__(self):
		crud.__init__(self)
		self.model = m_surveyor({'NIK':'','nama':'','nomor_HP':'',
								'alamat':'','foto':'',
								'survey':[],'blacklist':0})
		self.fields = [
					{'field':'NIK','type':'text','required':1,'search':1},
					{'field':'nama','type':'text','search':1},
					
					{'field':'nomor_HP','type':'text'},
					{'field':'alamat','type':'text_area','search':1},
					{'field':'foto','type':'foto'},
					]
		
		self.js.append("surveyor")
		self.css.append("qc/surveyor")
	
	def p(self,*p):
		self.fields.insert(2,{'field':'jml_pemilih','type':'numeric'})
		return crud.p(self,*p)
	
	def search(self,*p):
		self.fields.insert(2,{'field':'jml_pemilih','type':'numeric'})
		return crud.search(self,*p)
	
	def blacklist(self,data):
		id = data['id']
		return self.model.blacklist(id)
	
	def aktif(self,data):
		id = data['id']
		return self.model.aktif(id)
	
	def printing(self,id):
		surveyor = self.model.get_surveyor(id)
		return web.template.frender("views/qc/print.html")(surveyor,surveyor['survey'])
	
	def get_list(self,fields,data,write=True):
		c = ""
		if write:
			c += "<th class='add'><a href='"+self.base_url()+"add/'></a></th>"
		
		for field in fields:
			c += "<th>"+self.colName(field)+"</th>"
		
		if not data:
			return c+"<tr><td style='font-weight:bolder; text-align:center; background:#D5E4FC;'  colspan='"\
				+str(len(fields)+1)+"'>Data Kosong</td></tr>"
		
		for i,rw in enumerate(data):
			id = str(rw['_id'])
			className = "class='blacklist'" if rw['blacklist'] else ""
			 
			c += "<tr "+className+" id='"+id+"'>"
			if write:
				c += "<td class='action'><a title='Edit' href='%(base)sedit/%(id)s/' class='edit'></a>"\
					 "<a title='Hapus' href='javascript:void(0)' onclick='del(this,\"%(id)s\")' class='delete'></a>"\
					 "<a title='Excel' href='%(base)sexport/%(id)s/' class='export'></a>"\
					 % {'base':self.base_url(),'id':id}
				if not rw['blacklist']:
					c+= "<a title='Blacklist' href='javascript:void(0)' onclick='blacklist(this,\"%(id)s\")'  class='btn_blacklist'></a>"\
						"<a title='Print' target='_blank' href='%(base)sprinting/%(id)s/' class='btn_print'></a>"\
						% {'id':id,'base':self.base_url()}
				else:
					c+= "<a title='Aktifkan' href='javascript:void(0)' onclick='aktif(this,\"%(id)s\")' class='btn_aktif'></a>"\
						"<a title='Print' style='visibility:hidden;'class='btn_print'></a>" % {'id':id}
				c +="</td>"
			for field in fields:
				c += "<td>"+self.get_cell(rw[field['field']],field['type'])+"</td>"
			
			c += "</tr>"
		return c
	
	def export(self,id):
		import xlsxwriter,os
		res = self.model.get_export(id)
		filename = res['nama']+' '+res['NIK']
		workbook = xlsxwriter.Workbook('tmp/'+filename+'.xlsx')
		ws = workbook.add_worksheet()
		
		r=0
		c=0
		ws.write(r,c,'Surveyor :'+res['nama']);c+=1
		ws.write(r,c,'NIK :'+res['NIK']);
		r+=1;c=0
		sur = res['survey']
		order = ['NIK','nama','alamat','nomor_HP']
		for a in order:
			ws.write(r,c,a);c+=1
		r+=1;c=0
		for s in sur:
			for col in order:
				ws.write(r,c,str(s[col]));c+=1
			r+=1;c=0
		workbook.close()
		
		web.header('Content-Type','application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
		web.header('Content-disposition', 'attachment; filename='+filename+'.xlsx')
		with open('tmp/'+filename+'.xlsx', 'r') as f:
			data = f.read()
		os.remove('tmp/'+filename+'.xlsx')
		return data
	

from models.mo_crud import mo_crud
class m_surveyor(mo_crud):
	def __init__(self,structure):
		mo_crud.__init__(self,"surveyor",structure)

	def blacklist(self,id):
		self.cl.update({'_id':self.Id(id)},{'$set':{'blacklist':1,'survey':[]}})
	
	def aktif(self,id):
		self.cl.update({'_id':self.Id(id)},{'$set':{'blacklist':0}})
	
	def get_export(self,id):
		return self.cl.find_one({'_id':self.Id(id)})
	
	def get_surveyor(self,id):
		return self.cl.find_one({'_id':self.Id(id)})
	
	def select(self,*p):
		result,count = mo_crud.select(self,*p)
		i=-1
		for r in result:
			i+=1
			sur = self.cl.find_one({'_id':self.Id(r['_id'])},{'survey._id':1})
			jml = len(sur['survey'])
			result[i]['jml_pemilih'] = str(jml)
		return result,count
	
	def search(self,*p):
		result,count = mo_crud.search(self,*p)
		i=-1
		for r in result:
			i+=1
			sur = self.cl.find_one({'_id':self.Id(r['_id'])},{'survey._id':1})
			jml = len(sur['survey'])
			result[i]['jml_pemilih'] = jml
		return result,count
	