from core.model import model

class m_crud(model):
	
	def __init__(self,table_name):
		model.__init__(self)
		self.set_table(table_name)
	
	def select(self,limit,page=1,orderby=None):
		page -= 1
		page *= limit
		orderby = "order by "+orderby if orderby else "order by id desc"
		query = "select * from "+self.table_name+" "+orderby+" limit "+str(page)+","+str(limit)
		result = self.get_query(query)
		query = "select count(*) as count from "+self.table_name
		count = self.get_query(query)
		return result,count[0]['count']
	
	def select_by_id(self,id):
		query = "select * from "+self.table_name+" where id=%s"
		result = self.get_query(query,(id,))
		return result[0] if len(result)>0 else False
	
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
		query = "select * from "+self.table_name \
			+" where "+field+" "+orderby+" like %s limit "+str(page)+","+str(limit)
		
		result = self.get_query(query,(txt,))
		query = "select count(*) as count from "+self.table_name\
			+" where "+field+" like %s"
		count = self.get_query(query,(txt,))
		return result,count[0]['count']
	
	def insert(self,value):
		col,val = self.get_val(value)
		sql = "insert into "+self.table_name+"("+col+") values("+val+")"
		
		res = self.query(sql)
		return res
	
	def update(self,id,value):
		val = self.get_val_update(value)
		sql = "update "+self.table_name+" set "+val+" where id=%s"
		
		res = self.query(sql,(id,))
		return res
	
	def delete(self,id):
		query = "delete from "+self.table_name+" where id=%s"
		res = self.query(query,(id,))
		if res['error']:
				raise Exception(res['error']+" "+query)
		return res

class m_transaksi(m_crud):
	bulan = ""
	tahun = ""
	
	def __init__(self,table_name,col='tanggal'):
		m_crud.__init__(self,table_name)
		self.tgl = col
	
	def set_tgl(self,bulan,tahun):
		self.bulan = str(bulan)
		self.tahun = str(tahun)
	
	def select(self,limit,page=1):
		page -= 1
		page *= limit
		query = "select * from "+self.table_name \
		+" where month("+self.tgl+")='"+self.bulan+"' and year("+self.tgl+")='"+self.tahun+"'"\
		+" limit "+str(page)+","+str(limit)
		
		result = self.get_query(query)
		query = "select count(*) as count from "+self.table_name\
			+" where month("+self.tgl+")='"+self.bulan+"' and year("+self.tgl+")='"+self.tahun+"'"
		count = self.get_query(query)
		return result,count[0]['count']
	
	def search(self,cols,txt,limit,page=1):
		txt = "%%"+txt.replace(' ','%%')+"%%"
		field = "concat("
		for col in cols:
			field += "coalesce(`"+col+"`,''),"
		field = field[:-1]
		field +=")"
		
		page -= 1
		page *= limit
		query = "select * from "+self.table_name \
			+" where month("+self.tgl+")='"+self.bulan+"' and year("+self.tgl+")='"+self.tahun+"' "\
			+" and "+field+" like %s limit "+str(page)+","+str(limit)
		
		result = self.get_query(query,(txt,))
		query = "select count(*) as count from "+self.table_name\
			+" where month("+self.tgl+")='"+self.bulan+"' and year("+self.tgl+")='"+self.tahun+"' "\
			+" and "+field+" like %s"
		count = self.get_query(query,(txt,))
		return result,count[0]['count']
	