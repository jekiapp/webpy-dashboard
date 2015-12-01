from core.crud import crud

class survey(crud):
	active_menu = "qc"
	active_sub = "surveyor"
	title = "Survey Pemilih"
	def __init__(self):
		crud.__init__(self)
		self.structure = {'NIK':'','nama':'','alamat':'','nomor_HP':''}
		self.model = m_surveyor(self.structure)
		self.fields = [
					{'field':'surveyor','type':'text_area','required':1,'parent':1},
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
		
	def edit(self,_id,data=None):
		surveyor = self.model.get_surveyor()
		surveyor = [{"key":str(x['id']),"val":x["surveyor"]} for x in surveyor]
		self.fields[0].update({'attr':'disabled=1','type':'combo','value':surveyor})
		self.fields[1].update({'attr':'disabled=1'})
		
		
		try:
			return crud.edit(self,_id,data)
		except SurveyException as e:
			self.content += self.get_warning(str(e))
			self.content += self.get_sukses('Data Berhasil Disimpan')
			return crud.edit(self,_id)
		except DPTException as e:
			self.content += self.get_sukses(str(e))
			self.content += self.get_sukses('Data Berhasil Disimpan')
			return crud.edit(self,_id)
	
	def update(self,_id,fields,data):
		fields.pop(0);fields.pop(0)
		crud.update(self,_id,fields,data)

from models.mo_crud import mo_crud

class m_surveyor(mo_crud):
	def __init__(self,structure):
		mo_crud.__init__(self,"surveyor",structure,'survey','surveyor')
	
	def select_by_id(self,id):
		result = mo_crud.select_by_id(self,id)
		result['surveyor'] = result['parent']['_id']
		return result
	
	def insert(self,value):
		nik = value['NIK']
		c = self.cl.find({self.embed+'.NIK':nik}).count()
		
		result = mo_crud.insert(self,value)
		
		if c>0:
			raise SurveyException('Warning : NIK '+nik+' sudah pernah terdaftar');
		
		c = self.db.dpt.find({'NIK':nik}).count()
		if c>0:
			raise DPTException('NIK : '+nik+' terdaftar pada DPT');
		return result
	
	def get_surveyor(self):
		result = self.cl.find({'blacklist':0},{'nama':1,'NIK':1})
		res = []
		for r in result:
			res.append({'id':r['_id'],'surveyor':r['nama']+' ('+r['NIK']+')'})
		return res
	
	def select(self,*p):
		result,count = mo_crud.select(self,*p)
		i = -1
		for r in result:
			i+=1
			result[i]['surveyor'] = r['parent']['nama']+" ("+r['parent']['NIK']+")"
		return result,count
	
	def search_embed(self,cols,txt,limit,page=1):
		search=['$nama','$NIK']
		for c in cols:
			search.append('$'+self.embed+'.'+c)
			search.append(' ')
		
		result = self.cl.aggregate([
			{'$unwind':'$survey'},
			{'$project':{
				'_id':1,
				'survey._id':1,
				'fields':'$$ROOT',
				'surveyor':{'$concat':['$nama',' (','$NIK',')']},
				'search':{'$concat':search}
			}},
			{'$match':{
				'search':{'$regex':'.*'+txt+'.*','$options':'i'}
			}},
			{'$sort':self.SON([('_id',-1),(self.embed+'._id',-1)])},
			{'$skip':page},								
			{'$limit':limit},
			
		])
		
		count = list(self.cl.aggregate([
			{'$unwind':'$survey'},
			{'$project':{
				'search':{'$concat':search}
			}},
			{'$match':{
				'search':{'$regex':'.*'+txt+'.*','$options':'i'}
			}},
			{'$group':{'_id':None,'count':{'$sum':1}}}
		]))
		
		c = 0 if not len(count) else count[0]['count']
		result = [dict(x['fields'],surveyor=x['surveyor']) for x in result]
		result = [dict(x[self.embed],surveyor=x['surveyor']) for x in result]
		return result,c
	
class SurveyException(Exception):
	def __init__(self, message):
		Exception.__init__(self,message)

class DPTException(Exception):
	def __init__(self, message):
		Exception.__init__(self,message)