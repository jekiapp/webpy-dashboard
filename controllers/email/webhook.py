import web

class webhook:
	def index(self,data):
		yield web.ctx.headers
		for d in data:
			yield d,data[d]
	