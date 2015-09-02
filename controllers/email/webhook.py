import web

class webhook:
	def index(self,data):
		for d in data:
			yield d
	