from core.crud import crud
from models.mo_crud import mo_crud
from library.globals import base_url

class lap_surveyor(crud):
	active_menu = "qc"
	active_sub = "surveyor"
	title = "Data Survey Dobel"
	def __init__(self):
		crud.__init__(self)
		self.hak_akses = 1
		self.css.append("qc/qc");
		self.model = m_lapsurveyor()
		self.fields = [
					{'field':'surveyor','type':'text','required':1},
					{'field':'NIK','type':'text','search':1},
					{'field':'nama','type':'text','required':1,'search':1},
					{'field':'alamat','type':'text_area','search':1},
					]
	
	def get_list(self,fields,data,write=True):
		c = ""
		for field in fields:
			c += "<th>"+self.colName(field)+"</th>"
		
		if not data:
			return c+"<tr><td style='font-weight:bolder; text-align:center; background:#D5E4FC;'  colspan='"\
				+str(len(fields)+1)+"'>Data Kosong</td></tr>"
		nik = ""
		group = 1
		for i,rw in enumerate(data):
			id = str(rw['_id'])
			
			if nik!=rw['NIK']:
				nik = rw['NIK']
				group= 2 if group==1 else 1
			c += "<tr class='group"+str(group)+"' id='"+id+"'>"
			if write:
				c += "<td class='action'><a title='View' href='"+base_url()+"view/%(id)s/' class='edit'></a></td>"\
					 % {'id':id}
			for field in fields:
				c += "<td>"+self.get_cell(rw[field['field']],field['type'])+"</td>"
			c += "</tr>"
		return c

class m_lapsurveyor(mo_crud):
	def __init__(self):
		mo_crud.__init__(self,"surveyor",embed='survey');
	
	def insert(self,*p):
		return
	def update(self,*p):
		return
	
	def select(self,limit,page=1):
		page -= 1
		page *= limit
		
		result = self.cl.aggregate([
					{'$unwind':'$survey'},
					{'$group':{
						'_id':'$survey.NIK',					
						'fields':{'$push':{'_id':'$survey._id','snama':'$nama','sNIK':'$NIK'
							,'NIK':'$survey.NIK','nama':'$survey.nama',
							'alamat':'$survey.alamat'
							}},
						'count':{'$sum':1}
					}},
					{'$match':{'count':{'$gt':1}}},
					{'$unwind':'$fields'},
					{'$skip':page},
					{'$limit':limit}
				])
		result = [x['fields'] for x in result]
		result = [dict(x,surveyor=x['snama']+' ('+x['sNIK']+')') for x in result]
		count = list(self.cl.aggregate([
					{'$unwind':'$survey'},
					{'$group':{
						'_id':'$survey.NIK',
						'fields':{'$push':{'nama':'$nama'}},		
						'count':{'$sum':1}
					}},
					{'$match':{'count':{'$gt':1}}},
					{'$unwind':'$fields'},
					{'$group':{'_id':None,'count':{'$sum':1}}}
				]))
		c = count[0]['count'] if count else 0 
		return result,c
	
	def search_embed(self,cols,txt,limit,page):
		
		result = self.cl.aggregate([
					{'$unwind':'$survey'},
					{'$group':{
						'_id':'$survey.NIK',					
						'fields':{'$push':{'_id':'$survey._id','snama':'$nama','sNIK':'$NIK'
							,'NIK':'$survey.NIK','nama':'$survey.nama',
							'alamat':'$survey.alamat'
							}},
						'count':{'$sum':1}
					}},
					{'$match':{'count':{'$gt':1}}},
					{'$unwind':'$fields'},
					{'$match':{'$or':[{'fields.snama':{'$regex':txt,'$options':'i'}},{'fields.sNIK':txt}]}},
					{'$skip':page},
					{'$limit':limit}
				])
		result = [x['fields'] for x in result]
		result = [dict(x,surveyor=x['snama']+' ('+x['sNIK']+')') for x in result]
		count = list(self.cl.aggregate([
					{'$unwind':'$survey'},
					{'$group':{
						'_id':'$survey.NIK',
						'fields':{'$push':{'snama':'$nama','sNIK':'$NIK'}},		
						'count':{'$sum':1}
					}},
					{'$match':{'count':{'$gt':1}}},
					{'$unwind':'$fields'},
					{'$match':{'$or':[{'fields.snama':{'$regex':txt,'$options':'i'}},{'fields.sNIK':txt}]}},
					{'$group':{'_id':None,'count':{'$sum':1}}}
				]))
		c = count[0]['count'] if count else 0 
		return result,c
	
	