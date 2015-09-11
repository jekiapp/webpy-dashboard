from core.crud import crud

class verifikasi(crud):
	active_menu = "qc"
	active_sub = "surveyor"
	title = "Verifikasi Survey"
	def __init__(self):
		crud.__init__(self)
		self.model = m_verify()
		self.fields = [
					{'field':'NIK','type':'text','required':1,'search':1},
					{'field':'nama','type':'text','required':1,'search':1},
					{'field':'nama_surveyor','type':'text','search':1},
					{'field':'alamat','type':'text_area','search':1},
					{'field':'nomor_HP','type':'text'},
					{'field':'nik_surveyor','type':'text','required':1,'search':1},
					{'field':'HP_surveyor','type':'text'}
					]
	def add(self,data=None):
		self.transaksi = True
		deleted = self.model.get_deleted()
		deleted = [{'key':str(i['id']),'val':i['NIK']} for i in deleted]
		if not deleted: deleted = ['Tidak ada data']
		self.fields = [{'field':'id','type':'combo','value':deleted,'title':'NIK'}]
		try:
			return crud.add(self,data)
		except:
			return crud.add(self)
	
	def edit(self,*p):
		self.hak_akses = 1
		return crud.edit(self,*p)
	
	def delete(self,id):
		return self.model.delete(id)
		
	def get_list(self,fields,data,write=True):
		c = "<th class='add'><a href='"+self.base_url()+"add/'></a></th>"
		
		for field in fields:
			c += "<th>"+self.colName(field)+"</th>"
		
		if not data:
			return c+"<tr><td style='font-weight:bolder; text-align:center; background:#D5E4FC;'  colspan='"\
				+str(len(fields)+1)+"'>Data Kosong</td></tr>"
		
		for i,rw in enumerate(data):
			id = str(rw['id'])
			className = "class='odd'" if (i+1)%2==0 else "" 
			c += "<tr "+className+" id='"+id+"'>"
			
			c += "<td class='action'><a title='Hapus' href='javascript:void(0)' onclick='del(this,%(id)s)' class='delete'></a></td>"\
					 % {'id':id}
			for field in fields:
				c += "<td>"+self.get_cell(rw[field['field']],field['type'])+"</td>"
			
			c += "</tr>"
		return c
	

from models.m_crud import m_crud
class m_verify(m_crud):
	def __init__(self):
		m_crud.__init__(self,'qc_surveyor')
	
	def select(self,limit,page=1,orderby=None):
		page -= 1
		page *= limit
		orderby = "order by "+orderby if orderby else "order by id desc"
		query = "select * from "+self.table_name+" natural join qc_verifikasi_survey "\
			+orderby+" limit "+str(page)+","+str(limit)
		result = self.get_query(query)
		query = "select count(*) as count from "+self.table_name
		count = self.get_query(query)
		return result,count[0]['count']
	
	def search(self,cols,txt,limit,page=1,orderby=None):
		txt = "%%"+txt.replace(' ','%%')+"%%"
		field = "concat("
		for col in cols:
			field += "coalesce(`"+col+"`,''),"
		field = field[:-1]
		field +=")"
		
		orderby = "order by "+orderby if orderby else  "order by id desc"
		
		page -= 1
		page *= limit
		query = "select * from "+self.table_name+" natural join qc_verifikasi_survey " \
			+" where "+field+" "+orderby+" like %s limit "+str(page)+","+str(limit)
		
		result = self.get_query(query,(txt,))
		query = "select count(*) as count from "+self.table_name\
			+" where "+field+" like %s"
		count = self.get_query(query,(txt,))
		return result,count[0]['count']
	
	def insert(self,value):
		col,val = self.get_val(value)
		sql = "insert into qc_verifikasi_survey("+col+") values("+val+")"
		
		res = self.query(sql)
		return res
	
	
	def get_deleted(self):
		sql = "SELECT a.id,a.NIK FROM qc_surveyor a natural left join qc_verifikasi_survey b where b.id is NULL"
		return self.get_query(sql)
	
	def delete(self,id):
		query = "delete from qc_verifikasi_survey where id=%s"
		res = self.query(query,(id,))
		if res['error']:
				raise Exception(res['error']+" "+query)
		return res