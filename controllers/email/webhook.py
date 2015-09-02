import web
import hashlib,hmac

class webhook:
	def index(self,data=None):
		return 'OK'
	def indexs(self,data=None):
		if not data: return
		signed_data = 'https://app.radiaranai.com/email/webhook/'
		mandrill_key = 'XV0LPnOQxNcaH-gBrIdDCw'
		
		sorted_key = sorted(data)
		for k in sorted_key:
			signed_data += k
			signed_data += data[k]
		expected_signature = self._calc_signature(signed_data, mandrill_key)
		
		f = open('upload/post', 'w+')
		
		for h in web.ctx.headers:
			f.write(h[0]+" "+h[1]+"\n")
		f.write(str(expected_signature)+"\n")
		f.close()
		#expected_signature
	
	def _calc_signature(self, raw, key):
		hashed = hmac.new(key, raw, hashlib.sha1)
		return hashed.digest().encode("base64").rstrip('\n')