from core.mo_del import mo_del

class mo_crud(mo_del):
	structure = {}
	embed = ''
	def __init__(self,table_name,structure={},embed='',parent=''):
		mo_del.__init__(self)
		self.set_collection(table_name)
		self.structure = structure
		self.embed = embed
		self.parent = parent #needed for embed
	
	def select(self,limit,page=1,orderby=[('_id',-1)]):
		page -= 1
		page *= limit
		orderby.append((self.embed+'._id',-1))
		if self.embed:
			result = self.cl.aggregate([
							{'$unwind':'$'+self.embed},
							{'$sort':self.SON(orderby)},
							{'$skip':page},
							{'$limit':limit},
							])
			
			result = [dict(r[self.embed],parent={x:z for x,z in r.iteritems() if x!=self.embed}) for r in result]
			c = self.cl.aggregate([
						{'$unwind':'$'+self.embed},{'$group':{'_id':None,'count':{'$sum':1}}}
						])
			return result,list(c)[0]['count']
		else:
			result = self.cl.find(skip=page,limit=limit,sort=orderby)
			count = result.count()
		
		
		return list(result),count
	
	def search(self,cols,txt,limit,page=1,orderby=[('_id',-1)]):
		page -= 1
		page *= limit
		if self.embed: return self.search_embed(cols,txt,limit,page)
		
		result = self.cl.aggregate([
			{'$match':{
			'$text':{'$search':txt}
			}},
			{'$sort':self.SON(orderby)},
			{'$skip':page},
			{'$limit':limit}
		]);
		count = list(self.cl.aggregate([
			{'$match':{
			'$text':{'$search':txt}
			}},
			{'$group':{'_id':None,'count':{'$sum':1}}}
		]));
		
		c = 0 if not len(count) else count[0]['count']
		
		return list(result),c
	
	def search_embed(self,cols,txt,limit,page=1,orderby=[('_id',-1)]):
		search=[]
		for c in cols:
			search.append('$'+self.embed+'.'+c)
			search.append(' ')
		
		result = self.cl.aggregate([
			{'$unwind':'$survey'},
			
			{'$project':{
				'fields':'$$ROOT',
				'search':{'$concat':search}
			}},
			{'$match':{
				'search':{'$regex':'.*'+txt+'.*','$options':'i'}
			}},
			{'$sort':self.SON(orderby)},
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
		result = [x['fields'] for x in result]
		result = [dict(r[self.embed],parent={x:z for x,z in r.iteritems() if x!=self.embed}) for r in result]
		return list(result),c
	
	def insert(self,value):
		if self.embed:
			parent = value[self.parent]
			del value[self.parent]
			
			value = self.get_val_insert(value)
			
			new_id = self.Id()
			value['_id'] = new_id
			
			result = self.cl.update({'_id':self.Id(parent)},
						{
							'$push':{self.embed:value}
						}
						)
			return {"id":new_id,"affected":result['nModified'],"error":False}
		else:
			value = self.get_val_insert(value)
			new_id = self.cl.insert(value)
			return {"id":new_id,"affected":1,"error":False}
	
	def select_by_id(self,id):
		id = self.Id(id)
		if self.embed:
			result = list(self.cl.aggregate([
									{'$unwind':'$'+self.embed},
									{'$match':{self.embed+'._id':id}},{'$limit':1}
									]))
			if result:
				r = result[0]
				return dict(r[self.embed],parent={x:z for x,z in r.iteritems() if x!=self.embed})
			return False
		else:
			result = self.cl.find_one({'_id':id})
			return result if result else False
	
	def update(self,id,value):
		id = self.Id(id)
		value = self.get_val_update(value)
		
		if self.embed:
			upd = {self.embed+'.$.'+x:y for x,y in value.iteritems()}
			self.cl.update(
						{self.embed+'._id':id},
						{'$set':upd}
						)
		else:
			self.cl.update({'_id':id},{'$set':value})
	
	def delete(self,id):
		id = self.Id(id)
		if self.embed:
			self.cl.update(
						{self.embed+'._id':id},
						{'$pull':{self.embed:{'_id':id}}}
						)
		else:
			self.cl.remove({'_id':id})
	
	def get_val_insert(self,value):
		struct = self.structure
		for k,v in struct.iteritems():
			if k in value:
				struct[k] = value[k]
		return struct
	
	def get_val_update(self,value):
		new_val ={}
		struct = self.structure
		for k,v in struct.iteritems():
			if k in value:
				new_val[k] = value[k]
		return new_val