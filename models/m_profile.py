from core.model import model

class m_profile(model):
	def __init__(self):
		model.__init__(self)
	
	def get_data(self,user):
		query = "select * from user where username=%s"
		res =  self.get_query(query,(user,))
		return res[0]
	
	def update_password(self,user,password):
		query = "update user set password=%s where username=%s"
		self.query(query,(password,user))
		