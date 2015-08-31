import web
class logout(object):

    def index(self):
        web.config._session.kill()
        web.redirect("/")