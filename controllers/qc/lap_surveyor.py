from core.crud import crud
from models.m_crud import m_crud
from library.globals import base_url

class lap_surveyor(crud):
	active_menu = "qc"
	active_sub = "surveyor"
	title = "Laporan Surveyor"
	view = "qc_lapsurveyor"
	def __init__(self):
		crud.__init__(self)
		self.hak_akses = 1
		self.css.append("qc");
		self.model = m_lapsurveyor()
		self.fields = [
					{'field':'NIK','type':'text','search':1},
					{'field':'nama','type':'text','required':1,'search':1},
					{'field':'alamat','type':'text_area','search':1},
					{'field':'nik_surveyor','type':'text','required':1,'search':1},
					{'field':'nama_surveyor','type':'text','search':1},
					{'field':'TPS','type':'text','search':1},
					]
		surveyed,jml_dpt = self.model.get_suara();
		surveystr = "Suara Tersurvey "+str(surveyed)+\
			" dari "+str(jml_dpt)+" ("+str(round(float(surveyed)/float(jml_dpt)*100,2))+")%" 
		self.param.update({"surveyed":surveystr});
		
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
			id = str(rw['id'])
			
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
class m_lapsurveyor(m_crud):
	def __init__(self):
		m_crud.__init__(self,"qc_surveyor");
	
	def get_suara(self):
		sql = "select (select count(*) from (select a.NIK from qc_surveyor a join"\
				" qc_dpt b on a.NIK=b.NIK group by a.NIK) c) as surveyed,"\
				"(select count(*) from qc_dpt) as jml_dpt"
		res = self.get_query(sql);
		return res[0]['surveyed'],res[0]['jml_dpt']
	def select(self,limit,page=1):
		page -= 1
		page *= limit
		query = "select * from qc_surveyor a join "\
			"(select NIK from qc_surveyor group by NIK having count(*)>1) b on a.NIK=b.NIK"\
			" order by a.NIK limit "+str(page)+","+str(limit)
		result = self.get_query(query)
		query = "select count(*) as count from qc_surveyor a join "\
			"(select NIK from qc_surveyor group by NIK having count(*)>1) b on a.NIK=b.NIK"
		count = self.get_query(query)
		return result,count[0]['count']
	
	def select_by_id(self,id):
		query = "select * from "+self.table_name+" where id=%s"
		result = self.get_query(query,(id,))
		return result[0] if len(result)>0 else False
	
	def search(self,cols,txt,limit,page=1):
		txt = "%%"+txt.replace(' ','%%')+"%%"
		field = "concat("
		for col in cols:
			field += "coalesce(a.`"+col+"`,''),"
		field = field[:-1]
		field +=")"
		
		
		page -= 1
		page *= limit
		query = "select * from qc_surveyor a join "\
			"(select NIK from qc_surveyor group by NIK having count(*)>1) b on a.NIK=b.NIK"\
			"  where "+field+" like %s order by a.NIK "\
			" limit "+str(page)+","+str(limit)
		
		result = self.get_query(query,(txt,))
		query = "select count(*) as count from qc_surveyor a join "\
			"(select NIK from qc_surveyor group by NIK having count(*)>1) b on a.NIK=b.NIK"\
			"  where "+field+" like %s "
		count = self.get_query(query,(txt,))
		return result,count[0]['count']
	