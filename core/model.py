import traceback
import MySQLdb as db
import sys

from warnings import filterwarnings

class model():
	host = 'localhost'
	user = 'root'
	password = 'asmarahadi123'
	database = 'radiaranai'
	
	def __init__(self):
		filterwarnings('ignore', category = db.Warning)
	
	def open(self):
		self.con = db.connect(self.host, self.user,self.password,self.database)
		self.cursor = self.con.cursor()
	
	def close(self):
		if self.con.open:
			self.cursor.close()
			self.con.close()
	
	def set_table(self,table):
		self.table_name = table
	
	
	def get_query(self,query,data=()):
		self.open()
		
		try:
			if data:
				self.cursor.execute(query,data)
			else:
				self.cursor.execute(query)
			cols = [i[0] for i in self.cursor.description]
			results = self.cursor.fetchall()
			
			res = []
			for row in results:
				rw = {}
				for j in range(len(cols)):
					val = row[j]
					val = str.decode(val, errors="ignore") if isinstance(val,str) else val
					rw[cols[j]] = val
				res.append(rw)
			return res
		finally:
			self.close()
	
	def query(self,query,data=None):
		self.open()
		
		try:
			if isinstance(data,tuple):
				self.cursor.execute(query,data)
			elif isinstance(data,list):
				self.cursor.executemany(query,data)
			else:
				self.cursor.execute(query)
			
			self.con.commit()
			return {"id":self.cursor.lastrowid,"affected":self.cursor.rowcount,"error":False}
		except Exception as e:
			self.con.rollback();
			raise e
		finally:
			self.close()
	
	
	def get_val(self,values):
		col = ""
		val = ""
		for key,vals in values.iteritems():
			tmp = db.escape_string(vals);
			if tmp:
				col += "`"+db.escape_string(key)+"`,"
				val += "'"+tmp+"',"
		col = col[:-1]
		val = val[:-1]
		return col,val
	
	def get_val_update(self,values):
		val = ""
		for key,vals in values.iteritems():
			tmp = "'"+db.escape_string(vals)+"'" if vals else "NULL"
			val += "`"+db.escape_string(key)+"`="+tmp+","
		return val[:-1]
	
	def escape(self,val):
		return db.escape_string(val)
	
