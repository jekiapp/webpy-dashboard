import web
from hashlib import sha224
from models.m_login import m_login as m

class login():
    
    def __init__(self):
        if web.config._session.get("nama") != None:
            raise web.seeother("/")
    
    def GET(self):
        view = web.template.frender("views/login.html")
        return view(error=False)
    
    def POST(self):
    	data = web.input()
        if not hasattr(data,"login"): return web.notfound()
        
        username = data.username
        password = data.password
        h = sha224()
        h.update(password)
        password = h.hexdigest()
        
        if m().auth(username,password):
            web.config._session.nama = username
            web.redirect("/")
        else:
            web.redirect("/login/error/")
    
    def error(self):
        view = web.template.frender("views/login.html")
        return view(error=True)
    
    def reset(self):
        self.session.nama = None
        web.seeother("/")
        