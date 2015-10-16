from core.crud import crud
from MySQLdb import IntegrityError

class nomor(crud):
	table_name = "qc_daftar_nomor"
	active_menu = "qc"
	active_sub = "nomor"
	title = "Daftar Saksi"
	def __init__(self):
		crud.__init__(self)
		
		self.model = m_nomor({'nama':'',
							'nomor':'','keterangan':'','foto':'',
							'c1_1':'','c1_2':'','c1_3':'',
							'disable_LK':{ 'total1':0,'total2':0},'disable_PR':{'total1':0,'total2':0},
							'dpt_LK':{'total1':0,'total2':0,'total3':0,'total4':0},
							'dpt_PR':{'total1':0,'total2':0,'total3':0,'total4':0},
							'php_LK':{'total1':0,'total2':0,'total3':0,'total4':0},
							'php_PR':{'total1':0,'total2':0,'total3':0,'total4':0},
							'sah':{'total1':0,'total2':0},
							'suara':{'total1':0,'total2':0,'total3':0,'total4':0},
							'suratsuara':{'total1':0,'total2':0,'total3':0,'total4':0}
							})
		self.fields = [
					{'field':'nama','type':'text','required':1,'search':1},
					{'field':'nomor','type':'text','required':1,'search':1},
					{'field':'keterangan','type':'text_area','search':1},
					{'field':'foto','type':'foto'}
					]
		
	
	def p(self,*p):
		self.fields.append({'field':'c1_1','type':'text'})
		self.fields.append({'field':'c1_2','type':'text'})
		return crud.p(self,*p)
	
	def get_list(self,fields,data,write=True):
		c = ""
		if write:
			c += "<th class='add'><a href='"+self.base_url()+"add/'></a></th>"
		
		for field in fields:
			kol = field['field']
			if kol=='c1_1' or kol=='c1_2' or kol=='c1_3': continue
			c += "<th>"+self.colName(field)+"</th>"
		
		c+="<th>SMS</th>"\
			"<th>C1</th>"\
			"<th>Plano</th>"\
			"<th>Daftar Hadir</th>"
		
		if not data:
			return c+"<tr><td style='font-weight:bolder; text-align:center; background:#D5E4FC;'  colspan='"\
				+str(len(fields)+1)+"'>Data Kosong</td></tr>"
		
		for i,rw in enumerate(data):
			id = str(rw['_id'])
			className = "class='odd'" if (i+1)%2==0 else "" 
			c += "<tr "+className+" id='"+id+"'>"
			if write:
				c += "<td class='action'><a title='Edit' href='"+self.base_url()+"edit/%(id)s/' class='edit'></a>"\
					"<a title='Hapus' href='javascript:void(0)' onclick='del(this,\"%(id)s\")' class='delete'></a></td>"\
					 % {'id':id}
			for field in fields:
				if field['field']=='c1_1' or field['field']=='c1_2': continue
				c += "<td>"+self.get_cell(rw[field['field']],field['type'])+"</td>"
			sms  = self.model.get_sms(rw)
			c += "<td style='min-width: 250px; white-space:normal;'>"+sms+"</td>"
			
			c += "<td><a href='/image/f/"+rw['c1_1']+"' target='_blank'>Sudah Ada</a></td>" if rw['c1_1'] else "<td></td>"  
			c += "<td><a href='/image/f/"+rw['c1_2']+"' target='_blank'>Sudah Ada</a></td>" if rw['c1_2'] else "<td></td>"
			c += "<td><a href='/image/f/"+rw['c1_3']+"' target='_blank'>Sudah Ada</a></td>" if rw['c1_3'] else "<td></td>"
			
			c += "</tr>"
		return c
	

from models.mo_crud import mo_crud
class m_nomor(mo_crud):
	def __init__(self,structure):
		mo_crud.__init__(self,'saksi',structure)
	
	def get_sms(self,res):
		ret = ''
		if res['dpt_LK']['sent']==1:
			ret+=' datapemilihlakilaki'
		if res['dpt_PR']['sent']==1:
			ret+=' datapemilihperempuan'
		if res['php_LK']['sent']==1:
			ret+=' penggunahakpilihlakilaki'
		if res['php_PR']['sent']==1:
			ret+=' penggunahakpilihperempuan'
		if res['sah']['sent']==1:
			ret+=' sah'
		if res['suratsuara']['sent']==1:
			ret+=' suratsuara'
		if res['suara']['sent']==1:
			ret+=' suara'
		if res['disable_LK']['sent']==1:
			ret+=' pemilihdisabellakilaki'
		if res['disable_PR']['sent']==1:
			ret+=' pemilihdisabelperempuan'
		
			 
		return ret
	