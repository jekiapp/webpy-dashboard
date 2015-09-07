from core.crud import crud
from library.globals import base_url

class dpt(crud):
	active_menu = "qc"
	active_sub = "dpt"
	
	title = "Daftar Pemilih Tetap"
	def __init__(self):
		crud.__init__(self)
		self.model = m_dpt()
		self.css.append("qc");
		jenis_kelamin = ['Laki-laki',"Perempuan"]
		self.fields = [
					{'field':'NIK','type':'text','required':1,'search':1},
					{'field':'nama','type':'text','required':1,'search':1},
					{'field':'alamat','type':'text_area','search':1},
					{'field':'jenis_kelamin','type':'combo','rule':'required','value':jenis_kelamin}
					]
		surveyed,jml_dpt = self.model.get_suara();
		surveystr = "Suara Tersurvey "+str(surveyed)+\
			" dari "+str(jml_dpt)+" ("+str(round(float(surveyed)/float(jml_dpt)*100,2))+")%" 
		self.param.update({"surveyed":surveystr});
	
	def list(self,row,count,page,search=None):
		self.view = "dpt_list" 
		
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
			c += "<th class='add'><a href='"+base_url()+"add/'></a></th>"
		
		for field in fields:
			c += "<th>"+self.colName(field)+"</th>"
		
		if not data:
			return c+"<tr><td style='font-weight:bolder; text-align:center; background:#D5E4FC;'  colspan='"\
				+str(len(fields)+1)+"'>Data Kosong</td></tr>"
		
		for i,rw in enumerate(data):
			id = str(rw['id'])
			className = "class='surveyed'" if rw['surveyed']==1 else "" 
			c += "<tr "+className+" id='"+id+"'>"
			if write:
				c += "<td class='action'><a title='Edit' href='"+base_url()+"edit/%(id)s/' class='edit'></a>"\
					"<a title='Hapus' href='javascript:void(0)' onclick='del(this,%(id)s)' class='delete'></a></td>"\
					 % {'id':id}
			for field in fields:
				c += "<td>"+self.get_cell(rw[field['field']],field['type'])+"</td>"
			
			c += "</tr>"
		return c

from models.m_crud import m_crud
class m_dpt(m_crud):
	def __init__(self):
		m_crud.__init__(self,"qc_dpt")
	def get_suara(self):
		sql = "select (select count(*) from (select a.NIK from qc_surveyor a join"\
				" qc_dpt b on a.NIK=b.NIK group by a.NIK) c) as surveyed,"\
				"(select count(*) from qc_dpt) as jml_dpt"
		res = self.get_query(sql);
		return res[0]['surveyed'],res[0]['jml_dpt']
	def select(self,limit,page=1):
		page -= 1
		page *= limit
		query = "select a.*,not isnull(b.NIK) as surveyed from qc_dpt a "\
			"left join qc_surveyor b on a.NIK = b.NIK "\
			" group by a.NIK order by a.id limit "+str(page)+","+str(limit)
		
		result = self.get_query(query)
		query = "select count(*) as count from "+self.table_name
		count = self.get_query(query)
		return result,count[0]['count']
	
	def search(self,cols,txt,limit,page=1):
		txt = "%%"+txt.replace(' ','%%')+"%%"
		field = "concat("
		for col in cols:
			field += "coalesce(a."+col+",''),"
		field = field[:-1]
		field +=")"
		
		page -= 1
		page *= limit
		query = "select a.*,not isnull(b.NIK) as surveyed from qc_dpt a "\
			"left join qc_surveyor b on a.NIK = b.NIK "\
			" where "+field+" like %s group by a.NIK limit "+str(page)+","+str(limit)
		
		result = self.get_query(query,(txt,))
		query = "select count(*) as count from "+self.table_name\
			+" a where "+field+" like %s"
		
		count = self.get_query(query,(txt,))
		
		return result,count[0]['count']
	