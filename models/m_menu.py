from core.model import model

class m_menu(model):
	def __init__(self):
		model.__init__(self) 
	
	def get_menu(self,nama):
		query = """select m.* from user u
			join hak_akses_submenu hm
			on u.id = hm.id_user
			join sub_menu s
			on s.id = hm.id_menu
			join menu m
			on s.parent=m.id
			where u.username='"""+self.escape(nama)+"""'  and hm.hak!=0
			group by m.id order by m.id"""
		return self.get_query(query)
	
	def get_submenu(self,nama,menu):
		query = """SELECT s.sub_menu,s.url,hs.hak FROM user u 
			join hak_akses_submenu hs
			on u.id=hs.id_user
			join sub_menu s
			on s.id = hs.id_menu
			join menu m
			on m.id=s.parent
			where u.username='"""+self.escape(nama)+"""' and m.url='"""+menu+"""' and hs.hak!=0
			order by s.order
			"""
		return self.get_query(query)
	