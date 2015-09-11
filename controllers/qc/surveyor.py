from core.crud import crud

class surveyor(crud):
	active_menu = "qc"
	active_sub = "surveyor"
	title = "Surveyor"
	def __init__(self):
		crud.__init__(self)
		self.model = m_surveyor()
		self.fields = [
					{'field':'NIK','type':'text','required':1,'search':1},
					{'field':'nama','type':'text','required':1,'search':1},
					
					{'field':'nomor_HP','type':'text'},
					{'field':'alamat','type':'text_area','search':1},
					
					{'field':'nik_surveyor','type':'text','required':1,'search':1},
					{'field':'nama_surveyor','type':'text','search':1},
					{'field':'HP_surveyor','type':'text'}
					]
	
	def p(self,p):
		self.fields = [
					{'field':'NIK','type':'text','required':1,'search':1},
					{'field':'nama','type':'text','required':1,'search':1},
					{'field':'nama_surveyor','type':'text','search':1},
					{'field':'alamat','type':'text_area','search':1},
					{'field':'nomor_HP','type':'text'},
					{'field':'nik_surveyor','type':'text','required':1,'search':1},
					{'field':'HP_surveyor','type':'text'}
					]
		return crud.p(self,p)
	def add(self,data=None):
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
		try:
			return crud.add(self,id,data)
		except SurveyException as e:
			self.content += self.get_warning(str(e))
			self.content += self.get_sukses('Data Berhasil Disimpan')
			return crud.edit(self,id)
		except DPTException as e:
			self.content += self.get_sukses(str(e))
			self.content += self.get_sukses('Data Berhasil Disimpan')
			return crud.edit(self,id)



from models.m_crud import m_crud

class m_surveyor(m_crud):
	def __init__(self):
		m_crud.__init__(self,"qc_surveyor")
	
	
	def insert(self,value):
		res = m_crud.insert(self,value)
		sql = "insert into qc_verifikasi_survey values(%s)"
		self.query(sql,(res['id'],))
		
		nik = value['NIK']
		sql = "select NIK from qc_surveyor where NIK=%s"
		res = self.get_query(sql,(nik,))
		if len(res)>1:
			raise SurveyException('Warning : NIK '+nik+' sudah pernah terdaftar');
		
		sql = "select NIK from qc_dpt where NIK=%s"
		res = self.get_query(sql,(nik,))
		if len(res)>0:
			raise DPTException('NIK : '+nik+' terdaftar pada DPT');
		return res
	
	def update(self,id,value):
		res = m_crud.update(self,id,value)
		nik = value['NIK']
		sql = "select NIK from qc_surveyor where NIK=%s"
		res = self.get_query(sql,(nik,))
		if len(res)>0:
			raise SurveyException('NIK : '+nik+' sudah dimasukkan');
		
		sql = "select NIK from qc_dpt where NIK=%s"
		res = self.get_query(sql,(nik,))
		if len(res)>0:
			raise DPTException('NIK : '+nik+' terdaftar pada DPT');
		return res
		
class SurveyException(Exception):
	def __init__(self, message):
		Exception.__init__(self,message)

class DPTException(Exception):
	def __init__(self, message):
		Exception.__init__(self,message)
