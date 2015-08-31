from controller import controller
from models.m_crud import m_crud,m_transaksi
from library.globals import hilang_titik,encode_date,redirect,dict_val,base_url,img_url
from datetime import date
import web,traceback,sys


class crud(controller):
	decimalpoint = '%.0f' #tanpa desimal
	limit = 10
	transaksi = False
	tanggal = None
	
	def __init__(self,table_name,transaksi=False):
		self.transaksi = transaksi
		
		self.CN = self.active_sub = self.__class__.__name__ 
		if not hasattr(web.config._session,self.CN): setattr(web.config._session,self.CN,{})
		if not hasattr(self,'model'):
			if not transaksi:
				try:
					del getattr(web.config._session,self.CN)['bulan'] 
					del getattr(web.config._session,self.CN)['tahun']
				except: pass
				self.model = m_crud(table_name)
			else:
				if not 'bulan' in getattr(web.config._session,self.CN):
					getattr(web.config._session,self.CN)['bulan'] = date.today().month
					getattr(web.config._session,self.CN)['tahun'] = date.today().year
				self.tanggal=(getattr(web.config._session,self.CN)['bulan'],\
							getattr(web.config._session,self.CN)['tahun'])
				self.model = m_transaksi(table_name)
			
		controller.__init__(self)
		self.css.extend(["lib/apprise","crud"])
		self.js.append("lib/apprise")
	
	def index(self,data=None):
		page = 1 if 'page' not in getattr(web.config._session,self.CN) else getattr(web.config._session,self.CN)['page']
		
		return self.p(page)
	
	def p(self,page=1):
		try:
			if self.transaksi:
				self.tanggal=(getattr(web.config._session,self.CN)['bulan'],\
							getattr(web.config._session,self.CN)['tahun'])
				self.model.set_tgl(*self.tanggal)
			getattr(web.config._session,self.CN)['page'] = page
			
			page = int(page)
			if page==0: raise
			result,count = self.model.select(self.fields,self.limit,page)
			
			return self.list(result,count,page)
		except: 
			del getattr(web.config._session,self.CN)['page']
			if web.config.debug:
				return traceback.format_exception(*sys.exc_info())
			else:
				return web.notfound()#raise web.seeother(base_url())

	def search(self,cari=None,p=None,page=1):
		try:
			if not cari: raise Exception()
			cols = []
			for field in self.fields:
				if 'search' in field:
					cols.append(field['field'])
			
			if self.transaksi:
				self.tanggal=(getattr(web.config._session,self.CN)['bulan'],\
							getattr(web.config._session,self.CN)['tahun'])
				self.model.set_tgl(*self.tanggal)
			getattr(web.config._session,self.CN)['page'] = page
			
			page = int(page)
			result,count = self.model.search(cols,cari,self.limit,page)
			
			return self.list(result,count,page,cari)
		except: 
			del getattr(web.config._session,self.CN)['page']
			raise web.seeother(base_url())
	
	def nav(self,data):
		try:
			if not self.transaksi: raise
			nav = data['nav']
			bulan = int(self.tanggal[0])
			tahun = int(self.tanggal[1])
			if nav=="0":
				bulan -= 1
				if bulan==0: 
					bulan = 12
					tahun -= 1
			elif nav=="1":
				bulan += 1
				if bulan==13:
					bulan = 1
					tahun += 1
			getattr(web.config._session,self.CN)['bulan'] = bulan
			getattr(web.config._session,self.CN)['tahun'] = tahun
		finally: 
			del getattr(web.config._session,self.CN)['page']
			raise web.seeother(base_url())
	
	def list(self,row,count,page,search=None):
		self.view = "crud_list"
		self.js = ["list"]
		
		pages = [x for x in range(1,(count/self.limit)+(1 if count%self.limit==0 else 2)) if count!= 0]
		if pages and page>len(pages) : raise
		
		list_content = self.get_list(self.fields, row,self.hak_akses==2)
		self.param.update({"content":list_content,"tanggal":self.tanggal,"page":page,"pages":pages,"search":search})
		return self.render(self.view, self.param)
	
	def add(self,data=None):
		if self.hak_akses !=2: return web.notfound()
		self.js = ["form"]
		self.action = "Tambah"
		
		if data and 'simpan' in data:
			self.insert(data)
		else:
			cont = self.form(self.fields)
			self.param.update({'content':cont})
		return self.render(self.view,self.param)
	
	def insert(self,data):
		valid_value,error = self.validate(data)
		
		if error:
			cont = ""
			for m in error:
				cont += self.get_error(m)
			cont += self.form(self.fields,data)
			
			self.param.update({'content':cont})
		else:
			value = dict_val(self.fields,valid_value)
			
			self.model.insert(value)
			raise redirect(base_url())
	
	def validate(self,data):
		error = []
		new_val = {}
		for field in self.fields:
			tipe = field['type']
			
			val = data[field['field']]
			if 'required' in field\
				and val=="":
				error.append("Error : "+self.colName(field)+" tidak boleh kosong")
			if tipe=="numeric":
				try:
					int(val)
					long(val)
				except: error.append("Error : "+self.colName(field)+" harus berupa angka")
			if tipe=="currency":
				new_val[field['field']] = hilang_titik(val)
			if tipe=="date":
				new_val[field['field']] = encode_date(val)
			
			else:
				new_val[field['field']] = val
		
		return new_val,error
	
	def edit(self,id,data=None):
		if self.hak_akses !=2: return web.notfound()
		self.js.append("form")
		self.action = "Edit"
		
		if data and 'simpan' in data:
			self.update(id,data)
		else:
			result = self.model.select_by_id(self.fields,id)
			if not result:
				return web.notfound()
			data = {field['field']:self.get_val(result[field['field']] ,field['type']) for field in self.fields }
			
			cont = self.form(self.fields,data)
			self.param.update({'content':cont})
		return self.render(self.view,self.param)
	
	def update(self,id,data):
		valid_value,error = self.validate(data)
		if error:
			cont = ""
			for m in error:
				cont += self.get_error(m)
			cont += self.form(self.fields,data)
			
			self.param.update({'content':cont})
		else:
			value = dict_val(self.fields,valid_value)
			
			self.model.update(id,value)
			cont = self.get_sukses('Data Berhasil Disimpan')+self.form(self.fields,data)
			self.param.update({'content':cont})
			#raise redirect(base_url())
	
	def delete(self,id):
		return self.model.delete(id)
	
	""" LIST """
	
	def get_list(self,fields,data,write=True):
		c = ""
		if write:
			c += "<th class='add'><a href='"+base_url()+"add/'></a></th>"
		
		for field in fields:
			c += "<th>"+self.colName(field)+"</th>"
		
		if not data:
			return c+"<tr><td style='font-weight:bolder; text-align:center; background:#D5E4FC;'  colspan='"\
				+str(len(fields)+1)+"'>Data Kosong</td></tr>"
		
		for i,rw in enumerate(data):
			id = str(rw['id'])
			className = "class='odd'" if (i+1)%2==0 else "" 
			c += "<tr "+className+" id='"+id+"'>"
			if write:
				c += "<td class='action'><a title='Edit' href='"+base_url()+"edit/%(id)s/' class='edit'></a>"\
					"<a title='Hapus' href='javascript:void(0)' onclick='del(this,%(id)s)' class='delete'></a></td>"\
					 % {'id':id}
			for field in fields:
				c += "<td>"+self.get_cell(rw[field['field']],field['type'])+"</td>"
			
			c += "</tr>"
		return c
	
	def colName(self,field):
		if 'title' in field:
			return field['title']
		col = field['field']
		col = col.replace("_"," ")
		col = col.title()
		return col
	
	def get_val(self,val,tipe):
		if val is None:	return ""
		
		if tipe=="date":
			val = val.strftime("%d/%m/%Y")
		if tipe == "datetime":
			val = val.strftime("%H:%M %d/%m/%Y")
		elif tipe=="numeric":
			val = 0 if val is None else val
		elif tipe=="currency":
			val = 0 if val is None else val
			val = self.decimalpoint % float(val)
		
		return str(val)
	
	def get_cell(self,val,tipe):
		if val is None:	return ""
		
		if tipe=="date":
			return "<p style='text-align:center;'>"+self.get_val(val,tipe)+"</p>"
		elif tipe=="numeric":
			return "<p style='text-align:right;'>"+self.get_val(val,tipe)+"</p>"
		elif tipe=="currency":
			return "<p style='text-align:right;'>"+self.get_val(val,tipe)+"</p>"
		elif tipe=="foto":
			return "<div style='text-align:center; margin:10px 0;'><image src='"+self.image_url+"f/"+val+"_thumb'/></div>"
		else:
			return self.get_val(val,tipe)
	
	def get_error(self,str):
		return "<div class='error'>"+str+"</div>"
	
	def get_sukses(self,str):
		return "<div class='sukses'>"+str+"</div>"
	
	
	############## ADD #####################
	
	def get_required(self,field):
		return "<span style='color:red;'>*</span>" if 'required' in field else ""
	
	""" FORM """
	
	def form(self,fields,data=None):
		
		c = "<form method='post' >"+\
			"<fieldset>"
		for field in fields:
			tipe = field['type']
			val = str(data[field['field']]) if data else ''
			func = getattr(self, "form_"+tipe)
			c += func(field,val)
		c += "<div class='pDiv'><input type='submit' name='simpan' value='Simpan' />"+\
			 "<input type='reset' value='Clear' /></div>"
		c += "</fieldset></form>"+\
			"""<script>
				$(function(){
					$('input:submit').button()
					$('input:reset').button()
				});
			</script>"""
		return c
	
	def form_text(self,field,val):
		tipe = "medium" if not "text-type" in field else field['text-type']
		return "<div><div class='label'>"+self.colName(field)+self.get_required(field)+" :</div>"+\
			"<div><input id='f_"+field['field']+"' name='"+field['field']+"' value='"+val+"' type='text' class='text-"+tipe+"' /></div></div>"
	
	def form_currency(self,field,val):
		return "<div><div class='label'>"+self.colName(field)+self.get_required(field)+" :</div>"+\
			"<div><input id='f_"+field['field']+"' value='"+val+"'  name='"+field['field']+"' type='text' class='text-medium' "+\
			"style='text-align:right; font-weight:bolder; color:red;' "+\
			"onfocus='fokus(this)' onblur='fokus_out(this)'/></div></div>"
	
	def form_text_area(self,field,val):
		return "<div><div class='label'>"+self.colName(field)+self.get_required(field)+" :</div>"+\
			"<div><textarea id='f_"+field['field']+"'  name='"+field['field']+"' rows='1' cols='1'>"+val+"</textarea></div></div>"
	
	def form_combo(self,field,selected_val):
		value = field['value']
		c = "<div><div class='label'>"+self.colName(field)+self.get_required(field)+" :</div>"+\
			"<div><select id='f_"+field['field']+"' name='"+field['field']+"' >"
		for v in value:
			key = val = v
			if isinstance(v,dict):
				key = v['key']
				val = v['val']
			
			selected = 'selected="y"' if selected_val==key else '' 
			c += "<option value='"+key+"' "+selected+">"+val+"</option>"
		c +="</select></div></div>"
		
		return c
	
	def form_date(self,field,val):
		c = "<div><div class='label'>"+self.colName(field)+self.get_required(field)+" :</div>"+\
			"<div><input id='f_"+field['field']+"'  value='"+val+"' name='"+field['field']+"' type='text' class='text-medium'  onblur='isDate(this)' maxlength='10' />"+\
			"<a id='f_"+field['field']+"_clear' style='font: 11px Arial, Helvetica, sans-serif;'>Clear</a> (dd/mm/yyyy)"+\
			"</div></div>"
		
		c += """<script>
				  $(function() {
					$( "#%(id)s" ).datepicker({ dateFormat: 'dd/mm/yy' });
					$("#%(id)s_clear").button().click(function(){
						$("#%(id)s").val("");
					});
				  });
			  </script>""" % {'id':'f_'+field['field']}
		return c
		
	def form_numeric(self,field,val):
		return "<div><div class='label'>"+self.colName(field)+self.get_required(field)+" :</div>"+\
			"<div><input id='f_"+field['field']+"' value='"+val+"' name='"+field['field']+"' type='text' class='text-medium' "+\
			"style='text-align:right; font-weight:bolder;' /></div></div>"
	
	def form_foto(self,field,val):
		name= field['field']
		img = img_url()+"f/"+val if val else "/static/images/broken.png"
		rem = "block" if val else "none"
		file = "none" if val else "block"
		return """<div>
				<div class='label'>%(label)s :</div>
				<div class="foto">
					<input type="hidden" value="%(img_url)s"/>
					<input type="hidden" id="f_%(name)s"  name='%(name)s' class="foto_name" value="%(val)s">
					<div class="preview">
						<div><img src="%(img)s" /></div>
						<div title="Remove" style="display:%(rem)s;" class="close" onclick="remove_file(this)"></div>
						<div class="fileUpload" style="display:%(file)s;">
							<span>upload</span>
							<input type="file" name="file" class="upload" onchange="sendFile(this)"/>
						</div>
					</div>
					<div class="loading">
						<div class="progressbar"></div>
						<div class="cancel"></div>
					</div><br>
				</div>
				</div>
				<script>
					$(function(){
						$(".fileUpload span").button()
						$(".progressbar").progressbar({value:false});
					});
					var image_url = "%(img_url)s"
				</script>
				""" % {'label':self.colName(field)+self.get_required(field),'val':val,'name':name,\
					'img_url':img_url(),'img':img,'rem':rem,'file':file,'img_url':self.image_url}	
	
	"""
	def form_checkbox(self,field,val):
		req = "<span style='color:red;'>*</span>" if 'required' in field else ""
		checked = "checked='y'" if val==1 else "" 
		return "<div ><div style='display:inline-block; width:auto;' class='label'>"+self.colName(field)+req+" :</div>"+\
			"<div style='display:inline-block; margin-left:10px;'><input id='f_"+field['field']+"' value='1' name='"+field['field']+"' "+checked+" type='checkbox' "+\
			"style='text-align:right; font-weight:bolder;' /></div></div>"
	"""	