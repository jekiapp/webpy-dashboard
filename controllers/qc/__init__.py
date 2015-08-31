import web
from core.controller import controller
class qc(controller):
	def __init__(self):
		controller.__init__(self);
	def index(self):
		web.seeother("nomor/")
