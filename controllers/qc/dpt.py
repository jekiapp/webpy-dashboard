from core.crud import crud

class dpt(crud):
	active_menu = "qc"
	active_sub = "dpt"
	
	title = "Daftar Pemilih Tetap"
	def __init__(self):
		crud.__init__(self)
		
		self.css.append("qc/qc");
		self.fields = [
					{'field':'NIK','type':'text','required':1,'search':1},
					{'field':'nama','type':'text','required':1,'search':1},
					{'field':'alamat','type':'text_area','search':1}
					]
		
		self.model = mo_dpt({'NIK':'','nama':'','alamat':''})
	
	def list(self,row,count,page,search=None):
		self.view = "qc/dpt_list"
		surveystr = " " 
		if not search:
			surveyed,jml_dpt = self.model.get_suara();
			surveystr = "Suara Tersurvey "+str(surveyed)+\
				" dari "+str(jml_dpt)+" ("+str(round(float(surveyed)/float(jml_dpt)*100,2))+")%" 
		self.param.update({"surveyed":surveystr});
		
		self.js.append("list")
		
		pages = [x for x in range(1,(count/self.limit)+(1 if count%self.limit==0 else 2)) if count!= 0]
		if pages and page>len(pages) : raise
		
		list_content = self.get_list(self.fields, row,self.hak_akses==2)
		if self.transaksi: self.param.update({"tanggal":self.tanggal});
		self.param.update({"page":page,"pages":pages,"search":search})
		self.content += list_content
		return self.render(self.view, self.param)
	
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
			className = "class='surveyed'" if rw['surveyed']==1 else "" 
			c += "<tr "+className+" id='"+id+"'>"
			if write:
				c += "<td class='action'><a title='Edit' href='"+self.base_url()+"edit/%(id)s/' class='edit'></a>"\
					"<a title='Hapus' href='javascript:void(0)' onclick='del(this,\"%(id)s\")' class='delete'></a></td>"\
					 % {'id':id}
			for field in fields:
				c += "<td>"+self.get_cell(rw[field['field']],field['type'])+"</td>"
			
			c += "</tr>"
		return c

from models.mo_crud import mo_crud

class mo_dpt(mo_crud):
	def __init__(self,structure):
		mo_crud.__init__(self,"dpt",structure)
	
	def get_suara(self):
		jml = self.db.surveyed.count()
		return jml,self.count
	
	def select(self,limit,page=1):
		result,count = mo_crud.select(self,limit,page)
		for i,res in zip(range(len(result)),result):
			s = self.db.surveyed.find_one({'NIK':res['NIK']})
			res['surveyed'] = 1 if s else 0
			result[i] = res
		self.count = count
		return result,count
	
	def search(self,cols,txt,limit,page=1):
		result,count = mo_crud.search(self,cols,txt,limit,page)
		for i,res in zip(range(len(result)),result):
			s = self.db.surveyed.find_one({'NIK':res['NIK']})
			res['surveyed'] = 1 if s else 0
			result[i] = res
		return result,count
