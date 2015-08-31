import web
from core.controller import controller
from core.model import model

class setting(controller):
	active_menu='qc'
	active_sub = 'setting'
	title = 'Setting'
	view = 'qc_setting'
	def __init__(self):
		controller.__init__(self)
		self.model = m_setting()
	
	def index(self,data=None):
		if data and 'update' in data:
			self.model.update_setting(data)
		param = {"data":self.model.get_setting()}
		return self.render('qc_setting',param)
		
	
class m_setting(model):
	def __init__(self):
		model.__init__(self)
	
	def get_setting(self):
		query = "select * from setting_qc"
		return self.get_query(query)[0]
		
	def update_setting(self,data):
		sql = "update setting_qc set total_suara=%s"
		self.query(sql,(data['total_suara'],))