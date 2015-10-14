import web
from pymongo import MongoClient
from bson.son import SON
from bson.objectid import ObjectId

class mo_del:
	
	password = web.config.db_password;
	def __init__(self):
		client = MongoClient('mongodb://root:'+self.password+'@localhost:27017/')
		self.db = client.pilkada
		self.Id = ObjectId
		self.SON = SON
	
	def set_collection(self,collection):
		self.cl = self.db[collection]
	