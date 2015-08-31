from core.model import model

class m_login(model):

	def __init__(self):
		model.__init__(self)

	def auth(self,username,password):
		username = self.escape(username)
		password = self.escape(password)
		query = "select id from user where username=%s and password=%s"
		res = self.get_query(query,(username,password))
		authed = len(res)>0
		if authed:
			self.last_login(username)
		return authed
	
	def last_login(self,username):
		query = "update user set `last-seen`=now() where username=%s"
		self.query(query,(username,))
	