from models.m_crud import m_crud

class m_user(m_crud):
	def __init__(self):
		m_crud.__init__(self,'user') 
	
	def insert(self,value):
		res = m_crud.insert(self,value)
		id = res['id']
		admin = value['admin']
		return self.insert_menu(id,admin)
	
	def insert_menu(self,id,admin):
		q = "select id,admin from sub_menu"
		menu = self.get_query(q)
		
		q_insert = "insert into	hak_akses_submenu values(%s,%s,%s)"
		values = []
		for m in menu:
			id_menu = m['id']
			admin_menu = m['admin']
			hak = 2 if admin=='1' or admin_menu==0 else 0
			values.append((id,id_menu,hak))
		
		return self.query(q_insert,values)

	def get_menu(self,id_user):
		query = "select id,menu from menu"
		menu =  self.get_query(query)
		res = {}
		for m in menu:
			id = m['id']
			menu = m['menu']
			sub = self.get_submenu(id_user,id)
			res[menu] = sub
		return res
			
	def get_submenu(self,id_user,parent):
		query= "select s.id,s.sub_menu,h.hak from sub_menu s \
			join hak_akses_submenu h on s.id=h.id_menu \
			where s.parent=%s and h.id_user=%s"
		return self.get_query(query,(parent,id_user))

	def update_hak(self,id_user,id_menu,hak):
		query = "update hak_akses_submenu set hak=%s where id_user=%s and id_menu=%s"
		self.query(query,(hak,id_user,id_menu))
	
		
	def update_password(self,id,password):
		query = "update user set password=%s where id=%s"
		self.query(query,(password,id))