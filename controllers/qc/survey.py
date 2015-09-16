from core.crud import crud

class survey(crud):
	active_menu = "qc"
	active_sub = "surveyor"
	title = "Survey Pemilih"
	def __init__(self):
		crud.__init__(self)
		self.model = m_surveyor()
		self.fields = [
					{'field':'surveyor','type':'text_area','required':1},
					{'field':'NIK','type':'text','required':1,'search':1},
					{'field':'nama','type':'text','search':1},
					{'field':'alamat','type':'text_area'},
					{'field':'nomor_HP','type':'text'},
					]
	
	def add(self,data=None):
		surveyor = self.model.get_surveyor()
		surveyor = [{"key":str(x['id']),"val":x["surveyor"]} for x in surveyor]
		
		self.fields[0].update({'type':'combo','value':surveyor})
		
		if data: self.fields[0].update({"default":data['surveyor']}) 
		try:
			return crud.add(self,data)
		except SurveyException as e:
			self.content += self.get_warning(str(e))
			self.content += self.get_sukses('Data Berhasil Disimpan')
			return crud.add(self)
		except DPTException as e:
			self.content += self.get_sukses(str(e))
			self.content += self.get_sukses('Data Berhasil Disimpan')
			return crud.add(self)
		
	def edit(self,id,data=None):
		surveyor = self.model.get_surveyor()
		surveyor = [{"key":str(x['id']),"val":x["surveyor"]} for x in surveyor]
		self.fields[0].update({'attr':'disabled=1','type':'combo','value':surveyor})
		self.fields[1].update({'attr':'disabled=1'})
		
		
		try:
			return crud.edit(self,id,data)
		except SurveyException as e:
			self.content += self.get_warning(str(e))
			self.content += self.get_sukses('Data Berhasil Disimpan')
			return crud.edit(self,id)
		except DPTException as e:
			self.content += self.get_sukses(str(e))
			self.content += self.get_sukses('Data Berhasil Disimpan')
			return crud.edit(self,id)
	
	def update(self,id,fields,data):
		fields.pop(0);fields.pop(0)
		crud.update(self,id,fields,data)

from models.m_crud import m_crud

class m_surveyor(m_crud):
	def __init__(self):
		m_crud.__init__(self,"qc_survey")
	
	def insert(self,value):
		res = m_crud.insert(self,value)
		
		nik = value['NIK']
		sql = "select NIK from qc_survey where NIK=%s"
		res = self.get_query(sql,(nik,))
		if len(res)>1:
			raise SurveyException('Warning : NIK '+nik+' sudah pernah terdaftar');
		
		sql = "select NIK from qc_dpt where NIK=%s"
		res = self.get_query(sql,(nik,))
		if len(res)>0:
			raise DPTException('NIK : '+nik+' terdaftar pada DPT');
		return res
	
	def get_surveyor(self):
		sql = "select id,concat(nama,' (',NIK,')') as surveyor from qc_surveyor where not blacklist"
		return self.get_query(sql)

	def select(self,limit,page=1):
		page -= 1
		page *= limit
		
		query = "select a.*,concat(b.nama,' (',b.nik,')') as surveyor from "+self.table_name\
		+" a join qc_surveyor b on a.surveyor=b.id "\
		"order by b.id desc,a.id desc limit "+str(page)+","+str(limit)
		result = self.get_query(query)
		query = "select count(*) as count from "+self.table_name
		count = self.get_query(query)
		return result,count[0]['count']
	
	def search(self,cols,txt,limit,page=1,orderby=None,join=''):
		txt = "%%"+txt.replace(' ','%%')+"%%"
		field = "concat("
		for col in cols:
			field += "coalesce(a.`"+col+"`,''),"
		field += "coalesce(b.`NIK`,''),"
		field += "coalesce(b.`nama`,'')"
		#field = field[:-1]
		field +=")"
		
		orderby = "order by "+orderby if orderby else  "order by id desc"
		page -= 1
		page *= limit
		query = "select a.*,concat(b.nama,' (',b.nik,')') as surveyor from "\
			+self.table_name+" a join qc_surveyor b on a.surveyor=b.id "\
			+" where "+field+" like %s "+orderby+" limit "+str(page)+","+str(limit)
		
		result = self.get_query(query,(txt,))
		query = "select count(*) as count from "+self.table_name\
			+" a join qc_surveyor b on a.surveyor=b.id where "+field+" like %s"
		count = self.get_query(query,(txt,))
		return result,count[0]['count']
	
class SurveyException(Exception):
	def __init__(self, message):
		Exception.__init__(self,message)

class DPTException(Exception):
	def __init__(self, message):
		Exception.__init__(self,message)