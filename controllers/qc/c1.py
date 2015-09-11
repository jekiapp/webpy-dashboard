from core.controller import controller
class c1(controller):
	view = "qc/laporan_c1"
	active_menu = "qc"
	active_sub = "c1"
	title = "Laporan C1"
	def __init__(self):
		controller.__init__(self)
		self.css.append("qc/c1");
	
	def index(self):
		data = m_c1().get_c1()
		
		return self.render(self.view,data) 

from core.model import model
class m_c1(model):
	def __init__(self):
		model.__init__(self)
	
	def get_c1(self):
		sql = "select coalesce(sum(total1),0) as dptlk1,coalesce(sum(total2),0) as dptlk2, coalesce(sum(total3),0) as dptlk3,"\
			"coalesce(sum(total4),0) as dptlk4 from c1_dpt_LK"
		dptlk= self.get_query(sql)[0]
		
		
		sql = "select coalesce(sum(total1),0) as dptpr1,coalesce(sum(total2),0) as dptpr2, coalesce(sum(total3),0) as dptpr3,"\
			"coalesce(sum(total4),0) as dptpr4 from c1_dpt_PR"
		dptpr= self.get_query(sql)[0]
		
		
		sql = "select coalesce(sum(total1),0) as phplk1,coalesce(sum(total2),0) as phplk2, coalesce(sum(total3),0) as phplk3,"\
			"coalesce(sum(total4),0) as phplk4 from c1_php_LK"
		phplk= self.get_query(sql)[0]
		
		sql = "select coalesce(sum(total1),0) as phppr1,coalesce(sum(total2),0) as phppr2, coalesce(sum(total3),0) as phppr3,"\
			"coalesce(sum(total4),0) as phppr4 from c1_php_PR"
		phppr= self.get_query(sql)[0]
		
		sql = "select coalesce(sum(total1),0) as surat1,coalesce(sum(total2),0) as surat2, coalesce(sum(total3),0) as surat3,"\
			"coalesce(sum(total4),0) as surat4 from c1_suratsuara"
		surat= self.get_query(sql)[0]
		
		sql = "select coalesce(sum(total1),0) as sah1,coalesce(sum(total2),0) as sah2 from c1_sah"
		sah= self.get_query(sql)[0]
		
		sql = "select coalesce(sum(total1),0) as disablelk1,coalesce(sum(total2),0) as disablelk2 from c1_disable_LK"
		disablelk= self.get_query(sql)[0]
		
		sql = "select coalesce(sum(total1),0) as disablepr1,coalesce(sum(total2),0) as disablepr2 from c1_disable_PR"
		disablepr= self.get_query(sql)[0]
		
		return {"dptlk":dptlk,"dptpr":dptpr,"phplk":phplk,"phppr":phppr,"surat":surat,"sah":sah,\
			"disablelk":disablelk,"disablepr":disablepr}
		