from core.crud import crud
import web

class surveyor(crud):
	active_menu = "qc"
	active_sub = "surveyor"
	title = "Surveyor"
	def __init__(self):
		crud.__init__(self)
		self.model = m_surveyor()
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
	
	def blacklist(self,data):
		id = data['id']
		return self.model.blacklist(id)
	
	def aktif(self,data):
		id = data['id']
		return self.model.aktif(id)
	
	def printing(self,id):
		surveyor = self.model.get_surveyor(id)
		pemilih = self.model.get_pemilih(id)
		return web.template.frender("views/qc/print.html")(surveyor,pemilih)
	
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
			id = str(rw['id'])
			className = "class='blacklist'" if rw['blacklist'] else ""
			 
			c += "<tr "+className+" id='"+id+"'>"
			if write:
				c += "<td class='action'><a title='Edit' href='"+self.base_url()+"edit/%(id)s/' class='edit'></a>"\
					 "<a title='Hapus' href='javascript:void(0)' onclick='del(this,%(id)s)' class='delete'></a>"\
					 % {'id':id}
				if not rw['blacklist']:
					c+= "<a title='Blacklist' href='javascript:void(0)' onclick='blacklist(this,%(id)s)'  class='btn_blacklist'></a>"\
						"<a title='Print' target='_blank' href='%(base)sprinting/%(id)s/' class='btn_print'></a>"\
						% {'id':id,'base':self.base_url()}
				else:
					c+= "<a title='Aktifkan' href='javascript:void(0)' onclick='aktif(this,%(id)s)' class='btn_aktif'></a>"\
						"<a title='Print' style='visibility:hidden;'class='btn_print'></a>" % {'id':id}
				c +="</td>"
			for field in fields:
				c += "<td>"+self.get_cell(rw[field['field']],field['type'])+"</td>"
			
			c += "</tr>"
		return c
	

from models.m_crud import m_crud
class m_surveyor(m_crud):
	def __init__(self):
		m_crud.__init__(self,"qc_surveyor")
	
	def blacklist(self,id):
		sql = "update qc_surveyor set blacklist=1 where id=%s;"
		self.query(sql,(id,))
		
		sql = "delete from qc_survey where surveyor=%s"
		self.query(sql,(id,))
	
	def aktif(self,id):
		sql = "update qc_surveyor set blacklist=0 where id=%s"
		self.query(sql,(id,))
	
	def get_surveyor(self,id):
		sql = "select NIK,nama,alamat from qc_surveyor where id=%s"
		return self.get_query(sql,(id,))[0]
	
	def get_pemilih(self,id):
		sql = "select * from qc_survey where surveyor=%s"
		return self.get_query(sql,(id,))
	
	def select(self,limit,page=1,orderby=None):
		page -= 1
		page *= limit
		orderby = "order by "+orderby if orderby else "order by a.id desc"
		query = "select a.*,count(b.id) as jml_pemilih from "+self.table_name+" "\
			"a left join qc_survey b on a.id=b.surveyor group by a.id "\
			+orderby+" limit "+str(page)+","+str(limit)
		result = self.get_query(query)
		query = "select count(*) as count from "+self.table_name
		count = self.get_query(query)
		return result,count[0]['count']
	
	def search(self,cols,txt,limit,page=1,orderby=None,join=''):
		txt = "%%"+txt.replace(' ','%%')+"%%"
		field = "concat("
		for col in cols:
			field += "coalesce(a.`"+col+"`,''),"
		field = field[:-1]
		field +=")"
		
		orderby = "order by "+orderby if orderby else  "order by id desc"
		page -= 1
		page *= limit
		query = "select a.*,count(b.id) as jml_pemilih from "+self.table_name+" "\
			"a left join qc_survey b on a.id=b.surveyor  "\
			+" where "+field+" like %s group by a.id "+orderby+" limit "+str(page)+","+str(limit)
		
		result = self.get_query(query,(txt,))
		query = "select count(*) as count from "+self.table_name\
			+" a where "+field+" like %s"
		count = self.get_query(query,(txt,))
		return result,count[0]['count']
	