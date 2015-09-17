from core.crud import crud
from MySQLdb import IntegrityError

class nomor(crud):
	table_name = "qc_daftar_nomor"
	active_menu = "qc"
	active_sub = "nomor"
	title = "Daftar Saksi"
	def __init__(self):
		crud.__init__(self)
		self.model = m_nomor()
		self.fields = (
					{'field':'nama','type':'text','required':1,'search':1},
					{'field':'nomor','type':'text','required':1,'search':1},
					{'field':'keterangan','type':'text_area','search':1},
					{'field':'foto','type':'foto'}
					)
		self.model.set_table(self.table_name)
	def get_list(self,fields,data,write=True):
		c = ""
		if write:
			c += "<th class='add'><a href='"+self.base_url()+"add/'></a></th>"
		
		for field in fields:
			c += "<th>"+self.colName(field)+"</th>"
		c+="<th>SMS</th>"
		if not data:
			return c+"<tr><td style='font-weight:bolder; text-align:center; background:#D5E4FC;'  colspan='"\
				+str(len(fields)+1)+"'>Data Kosong</td></tr>"
		
		for i,rw in enumerate(data):
			id = str(rw['id'])
			className = "class='odd'" if (i+1)%2==0 else "" 
			c += "<tr "+className+" id='"+id+"'>"
			if write:
				c += "<td class='action'><a title='Edit' href='"+self.base_url()+"edit/%(id)s/' class='edit'></a>"\
					"<a title='Hapus' href='javascript:void(0)' onclick='del(this,%(id)s)' class='delete'></a></td>"\
					 % {'id':id}
			for field in fields:
				c += "<td>"+self.get_cell(rw[field['field']],field['type'])+"</td>"
			sms  = self.model.get_sms(rw['nomor'])
			c += "<td style='min-width: 250px; white-space:normal;'>"+sms+"</td>"
			
			c += "</tr>"
		return c
	
	def add(self,data=None):
		
		try:
			return crud.add(self,data)
		except IntegrityError as i:
			cont = self.get_error("Error : Nomor sudah ada")
			self.content += cont
			return crud.add(self,data)
	
	def edit(self,id,data=None):
		try:
			return crud.edit(self,id,data)
		except IntegrityError as i:
			cont = self.get_error("Error : Nomor sudah ada")
			self.content += cont
			return crud.edit(self,id)

from models.m_crud import m_crud
class m_nomor(m_crud):
	def __init__(self):
		m_crud.__init__(self,'qc_daftar_nomor')
	
	def get_sms(self,nomor):
		sql = """SELECT 
				concat(
				if(b.nomor,'datapemilihlakilaki ',''),
				if(c.nomor,'datapemilihperempuan ',''),
				if(d.nomor,'penggunahakpilihlakilaki ',''),
				if(e.nomor,'penggunahakpilihperempuan ',''),
				if(f.nomor,'sah ',''),
				if(g.nomor,'penggunaansuratsuara ',''),
				if(h.nomor,'suara ',''),
				if(i.nomor,'pemilihdisabellakilaki ',''),
				if(j.nomor,'pemilihdisabelperempuan ','')
				) as sms
				FROM qc_daftar_nomor a 
				left join c1_dpt_LK b on a.nomor=b.nomor
				left join c1_dpt_PR c on a.nomor=c.nomor
				left join c1_php_LK d on a.nomor=d.nomor
				left join c1_php_PR e on a.nomor=e.nomor
				left join c1_sah f on a.nomor=f.nomor
				left join c1_suratsuara g on a.nomor=g.nomor
				left join c1_suara h on a.nomor=h.nomor
				left join c1_disable_LK i on a.nomor=i.nomor
				left join c1_disable_PR j on a.nomor=j.nomor
				
				where a.nomor=%s"""
		return self.get_query(sql,(nomor,))[0]['sms']
	